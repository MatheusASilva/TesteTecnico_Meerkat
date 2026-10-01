import model.pecas_model as pecas_model
import model.vendas_model as vendas_model

for peca in pecas_model.PecaDAO.lista():
    print(peca)

for venda in vendas_model.VendaDAO.lista():
    print(venda)