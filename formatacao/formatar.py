from datetime import datetime
from pathlib import Path
import unicodedata

import pandas

BASE_DIR = Path(__file__).resolve().parent.parent
PECAS_PATH = BASE_DIR / "pecas.csv"
VENDAS_PATH = BASE_DIR / "vendas.csv"
OUTPUT_DIR = Path(__file__).resolve().parent


def formatar_data(data):
    if pandas.isna(data):
        return None
    data = str(data).strip()
    try:
        if "/" in data:
            return datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        if "-" in data:
            formato = "%Y-%m-%d" if len(data.split("-")[0]) == 4 else "%d-%m-%Y"
            return datetime.strptime(data, formato).strftime("%Y-%m-%d")
    except ValueError:
        return "Data invalida"
    return "Data invalida"


def formatar_sku(sku):
    return None if pandas.isna(sku) else str(sku).strip().upper()


def formatar_valor(valor):
    if pandas.isna(valor):
        return 0.0
    try:
        valor = str(valor).replace("R$", "").strip()
        if "." in valor and "," in valor:
            valor = valor.replace(".", "").replace(",", ".")
        elif "," in valor:
            valor = valor.replace(",", ".")
        return f"{float(valor):.2f}"
    except ValueError:
        return 0.0


def formatar_quantidade(quantidade):
    if pandas.isna(quantidade):
        return 0
    try:
        return int(float(str(quantidade).strip().replace(",", ".")))
    except ValueError:
        return 0


def formatar_desconto(desconto):
    if pandas.isna(desconto):
        return 0.0
    try:
        return float(str(desconto).strip().replace("%", "").replace(",", "."))
    except ValueError:
        return 0.0


def formatar_textos(texto):
    if pandas.isna(texto):
        return ""
    texto = "".join(c for c in unicodedata.normalize("NFD", str(texto).strip().upper()) if unicodedata.category(c) != "Mn")
    return {"FREIO": "FREIOS", "FRENAGEM": "FREIOS", "FILTRO": "FILTROS"}.get(texto, texto)


def carregar_dados():
    pecas_csv = pandas.read_csv(PECAS_PATH, sep=";")
    vendas_csv = pandas.read_csv(VENDAS_PATH, sep=";")

    pecas_csv["sku"] = pecas_csv["sku"].apply(formatar_sku)
    pecas_csv["nome_peca"] = pecas_csv["nome_peca"].apply(formatar_textos)
    pecas_csv["categoria"] = pecas_csv["categoria"].apply(formatar_textos)
    pecas_csv["custo_unitario"] = pecas_csv["custo_unitario"].apply(formatar_valor)
    pecas_csv["fornecedor"] = pecas_csv["fornecedor"].apply(formatar_textos)
    pecas_csv["estoque_atual"] = pecas_csv["estoque_atual"].apply(formatar_quantidade)

    for coluna in ["id_venda", "sku"]:
        vendas_csv[coluna] = vendas_csv[coluna].apply(formatar_sku)
    for coluna in ["loja", "cliente", "status", "vendedor"]:
        vendas_csv[coluna] = vendas_csv[coluna].apply(formatar_textos)
    vendas_csv["data_venda"] = vendas_csv["data_venda"].apply(formatar_data)
    vendas_csv["quantidade"] = vendas_csv["quantidade"].apply(formatar_quantidade)
    vendas_csv["preco_unitario"] = vendas_csv["preco_unitario"].apply(formatar_valor)
    vendas_csv["desconto"] = vendas_csv["desconto"].apply(formatar_desconto)

    duplicatas = int(vendas_csv.duplicated(subset=["id_venda", "sku"]).sum())
    vendas_csv = vendas_csv.drop_duplicates(subset=["id_venda", "sku"])
    return pecas_csv, vendas_csv, duplicatas


def salvar_arquivos_formatados(pecas_csv, vendas_csv):
    pecas_csv.to_csv(OUTPUT_DIR / "pecas_formatadas.csv", index=False, sep=";")
    vendas_csv.to_csv(OUTPUT_DIR / "vendas_formatadas.csv", index=False, sep=";")


if __name__ == "__main__":
    pecas, vendas, duplicatas = carregar_dados()
    salvar_arquivos_formatados(pecas, vendas)
    print(f"Dados formatados. Duplicatas removidas: {duplicatas}")
