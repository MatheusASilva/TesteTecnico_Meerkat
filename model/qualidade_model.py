from dataclasses import asdict, dataclass

from model.conecta import connection


@dataclass
class QualidadeDados:
    linhas_pecas_lidas: int
    linhas_vendas_lidas: int
    linhas_vendas_validas: int
    linhas_duplicadas_removidas: int

    def to_dict(self):
        return asdict(self)


class QualidadeDAO:
    @staticmethod
    def obter() -> QualidadeDados:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT linhas_pecas_lidas, linhas_vendas_lidas,
                       linhas_vendas_validas, linhas_duplicadas_removidas
                FROM qualidade_dados
                WHERE id = 1
                """
            )
            result = cursor.fetchone()

        if result is None:
            raise ValueError("Dados de qualidade ainda não foram carregados")
        return QualidadeDados(*result)