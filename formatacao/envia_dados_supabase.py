from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
import os
from pathlib import Path
from formatacao.formatar import pecas_csv, vendas_csv

caminho_env = Path(__file__).resolve().parent.parent / 'config' / '.env'

load_dotenv(dotenv_path=caminho_env)

DATABASE_URL = os.getenv("DATABASE_URL")

url_para_sqlalchemy = DATABASE_URL
if url_para_sqlalchemy.startswith("postgresql://") and "+psycopg2" not in url_para_sqlalchemy:
    url_para_sqlalchemy = url_para_sqlalchemy.replace("postgresql://", "postgresql+psycopg2://")

engine = create_engine(url_para_sqlalchemy)

def upsert_pecas_method(table, conn, keys, data_iter): ## Gerado por IA para garantir que os dados sejam inseridos ou atualizados corretamente
    insert_stmt = insert(table.table).values(list(data_iter))
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=[table.table.c.sku],
        set_={c.key: c for c in insert_stmt.excluded if c.key != 'sku'}
    )
    conn.execute(upsert_stmt)

def upsert_vendas_method(table, conn, keys, data_iter):
    insert_stmt = insert(table.table).values(list(data_iter))
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=[table.table.c.id_venda, table.table.c.sku],
        set_={c.key: c for c in insert_stmt.excluded if c.key not in ['id_venda', 'sku']}
    )
    conn.execute(upsert_stmt)

pecas_csv.to_sql("pecas", engine, if_exists="append", index=False, method=upsert_pecas_method)

vendas_csv.to_sql("vendas", engine, if_exists="append", index=False, method=upsert_vendas_method)