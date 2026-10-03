from model.conecta import connection
from dataclasses import dataclass, asdict

@dataclass
class Peca:
    sku: str
    nome_peca: str
    categoria: str
    custo_unitario: float
    fornecedor: str
    estoque_atual: int

    def to_dict(self):
        return asdict(self)


class PecaDAO:
    
    @staticmethod
    def salva(peca: Peca):
        try:
            with connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO pecas (sku, nome_peca, categoria, custo_unitario, fornecedor, estoque_atual)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    peca.sku, peca.nome_peca, peca.categoria,
                    peca.custo_unitario, peca.fornecedor, peca.estoque_atual
                ))
            connection.commit()
            
        except Exception as e:
            connection.rollback()
            print(f"Erro ao salvar peça no BD: {e}")
            raise e

    @staticmethod
    def busca_por_sku(sku: str) -> Peca | None:
        try:
            with connection.cursor() as cursor:
                select_query = """
                    SELECT sku, nome_peca, categoria, custo_unitario, fornecedor, estoque_atual 
                    FROM pecas WHERE sku = %s
                """
                cursor.execute(select_query, (sku,))
                result = cursor.fetchone()

            if result:
                return Peca(*result)
            return None
            
        except Exception as e:
            print(f"Erro ao buscar peça no BD: {e}")
            raise e

    @staticmethod
    def atualiza(peca: Peca):
        try:
            with connection.cursor() as cursor:
                update_query = """
                    UPDATE pecas
                    SET nome_peca = %s, categoria = %s, custo_unitario = %s, fornecedor = %s, estoque_atual = %s
                    WHERE sku = %s
                """
                cursor.execute(update_query, (
                    peca.nome_peca, peca.categoria, peca.custo_unitario,
                    peca.fornecedor, peca.estoque_atual, peca.sku
                ))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Erro ao atualizar peça no BD: {e}")
            raise e

    @staticmethod
    def listar() -> list[Peca]:
        try:
            with connection.cursor() as cursor:
                select_query = """
                    SELECT sku, nome_peca, categoria, custo_unitario, fornecedor, estoque_atual 
                    FROM pecas
                    order by sku
                """
                cursor.execute(select_query)
                results = cursor.fetchall()

            return [Peca(*row) for row in results]
            
        except Exception as e:
            print(f"Erro ao listar peças no BD: {e}")
            raise e

    @staticmethod
    def deleta(sku: str):
        try:
            with connection.cursor() as cursor:
                delete_query = "DELETE FROM pecas WHERE sku = %s"
                cursor.execute(delete_query, (sku,))
                linhas_afetadas = cursor.rowcount 
                
            connection.commit()

            return linhas_afetadas > 0
        
        except Exception as e:
            connection.rollback()
            print(f"Erro ao deletar peça no BD: {e}")
            raise e