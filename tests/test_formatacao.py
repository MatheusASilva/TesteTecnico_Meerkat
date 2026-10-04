from formatacao.formatar import carregar_dados, formatar_data, formatar_desconto, formatar_valor


def test_formatar_valor_brasileiro():
    assert formatar_valor("1.234,56") == "1234.56"
    assert formatar_valor("R$ 764.634,37") == "764634.37"


def test_formatar_data_para_sql():
    assert formatar_data("02/06/2025") == "2025-06-02"
    assert formatar_data("2025-06-02") == "2025-06-02"


def test_formatar_desconto_com_virgula():
    assert formatar_desconto("10,5%") == 10.5


def test_deduplicacao_de_venda_e_peca():
    _, vendas, duplicatas = carregar_dados()
    assert duplicatas > 0
    assert not vendas.duplicated(subset=["id_venda", "sku"]).any()
