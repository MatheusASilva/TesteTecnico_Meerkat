from model.conecta import connection
from model.pecas_model import PecaDAO
from dataclasses import dataclass, asdict

@dataclass
class Venda:
    id_venda: str
    data_venda: str
    loja: str
    cliente: str
    sku: str
    quantidade: int
    preco_unitario: float
    desconto: float
    status: str
    vendedor: str

    def to_dict(self):
        return asdict(self)

class VendaDAO:
    
    @staticmethod
    def salva(venda: Venda):
        try:
            with connection.cursor() as cursor:

                insert_query = """
                    INSERT INTO vendas (id_venda, data_venda, loja, cliente, sku, quantidade, preco_unitario, desconto, status, vendedor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    venda.id_venda, venda.data_venda, venda.loja,
                    venda.cliente, venda.sku, venda.quantidade,
                    venda.preco_unitario, venda.desconto,
                    venda.status, venda.vendedor
                ))

                if venda.status == "CONCLUIDA":
                    update_estoque = "UPDATE pecas SET estoque_atual = estoque_atual - %s WHERE sku = %s"
                    cursor.execute(update_estoque, (venda.quantidade, venda.sku))
                elif venda.status == "DEVOLVIDA":
                    update_estoque = "UPDATE pecas SET estoque_atual = estoque_atual + %s WHERE sku = %s"
                    cursor.execute(update_estoque, (venda.quantidade, venda.sku))

            connection.commit()
            
        except Exception as e:
            connection.rollback()
            print(f"Erro ao salvar venda no BD: {e}")
            raise e

    @staticmethod
    def busca_por_id(id_venda: str) -> Venda | None:
        try:
            with connection.cursor() as cursor:
                select_query = """
                    SELECT id_venda, data_venda, loja, cliente, sku, quantidade, preco_unitario, desconto, status, vendedor 
                    FROM vendas WHERE id_venda = %s
                """
                cursor.execute(select_query, (id_venda,))
                result = cursor.fetchone()

            if result:
                return Venda(*result)
            return None
            
        except Exception as e:
            print(f"Erro ao buscar venda no BD: {e}")
            raise e

    @staticmethod
    def atualiza(venda: Venda):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT status FROM vendas WHERE id_venda = %s", (venda.id_venda,))
                resultado = cursor.fetchone()
                
                if not resultado:
                    raise ValueError(f"Venda {venda.id_venda} não encontrada.")
                
                status_antigo = resultado[0]

                update_query = """
                    UPDATE vendas
                    SET data_venda = %s, loja = %s, cliente = %s, sku = %s, quantidade = %s,
                        preco_unitario = %s, desconto = %s, status = %s, vendedor = %s
                    WHERE id_venda = %s
                """
                cursor.execute(update_query, (
                    venda.data_venda, venda.loja, venda.cliente,
                    venda.sku, venda.quantidade, venda.preco_unitario,
                    venda.desconto, venda.status, venda.vendedor,
                    venda.id_venda
                ))

                if status_antigo != venda.status:
                    if venda.status == "CONCLUIDA":
                        cursor.execute("UPDATE pecas SET estoque_atual = estoque_atual - %s WHERE sku = %s", 
                                       (venda.quantidade, venda.sku))
                                       
                    elif status_antigo == "CONCLUIDA" and venda.status in ["DEVOLVIDA", "CANCELADA"]:
                        cursor.execute("UPDATE pecas SET estoque_atual = estoque_atual + %s WHERE sku = %s", 
                                       (venda.quantidade, venda.sku))

            connection.commit()
            
        except Exception as e:
            connection.rollback()
            print(f"Erro ao atualizar venda no BD: {e}")
            raise e

    @staticmethod
    def listar() -> list[Venda]:
        try:
            with connection.cursor() as cursor:
                select_query = """
                    SELECT id_venda, data_venda, loja, cliente, sku, quantidade, preco_unitario, desconto, status, vendedor 
                    FROM vendas
                    order by data_venda DESC, id_venda DESC
                """
                cursor.execute(select_query)
                results = cursor.fetchall()

            return [Venda(*result) for result in results]
            
        except Exception as e:
            print(f"Erro ao listar vendas no BD: {e}")
            raise e

    @staticmethod
    def cancela(id_venda: str) -> bool:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT status, sku, quantidade FROM vendas WHERE id_venda = %s", (id_venda,))
                resultado = cursor.fetchone()
                
                if not resultado:
                    raise ValueError(f"Venda {id_venda} não encontrada.")
                
                status_atual, sku, quantidade = resultado

                if status_atual == "CANCELADA":
                    return False
                
                update_query = "UPDATE vendas SET status = 'CANCELADA' WHERE id_venda = %s"
                cursor.execute(update_query, (id_venda,))

                if status_atual == "CONCLUIDA":
                    cursor.execute("UPDATE pecas SET estoque_atual = estoque_atual + %s WHERE sku = %s", 
                                   (quantidade, sku))

            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f"Erro ao cancelar venda no BD: {e}")
            raise e