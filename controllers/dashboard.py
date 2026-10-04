from fastapi import APIRouter, HTTPException, status
from formatacao.formatar import carregar_dados
from model.pecas_model import PecaDAO
from model.vendas_model import VendaDAO

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/faturamento-total", status_code=status.HTTP_200_OK)
async def obter_faturamento_total():
    
    try:
        vendas = VendaDAO.listar()
        faturamento_liquido = 0.0
        
        for venda in vendas:
            if venda.status.strip().upper() == 'CONCLUIDA':
                
                valor_linha = venda.quantidade * venda.preco_unitario * (1 - (venda.desconto / 100.0))
                faturamento_liquido += valor_linha
                
        return {"faturamento_total": round(faturamento_liquido, 2)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular o faturamento total: {e}")


@router.get("/faturamento-por-categoria", status_code=status.HTTP_200_OK)
async def obter_faturamento_categoria():

    try:
        vendas = VendaDAO.listar()
        pecas = PecaDAO.listar()

        
        mapa_categorias = {peca.sku: peca.categoria for peca in pecas}
        faturamento_categoria = {}
        
        for venda in vendas:
            if venda.status.strip().upper() == 'CONCLUIDA':
                valor_linha = venda.quantidade * venda.preco_unitario * (1 - (venda.desconto / 100.0))
                categoria = mapa_categorias.get(venda.sku, "DESCONHECIDA")

                
                faturamento_categoria[categoria] = faturamento_categoria.get(categoria, 0.0) + valor_linha
                
        categorias_ordenadas = [{"categoria": k, "valor": round(v, 2)} 
                                for k, v in sorted(faturamento_categoria.items(), key=lambda item: item[1], reverse=True)]
        
        return {"categorias": categorias_ordenadas}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular faturamento por categoria: {e}")


@router.get("/estoque-parado", status_code=status.HTTP_200_OK)
async def obter_estoque_parado():
    
    try:
        vendas = VendaDAO.listar()
        pecas = PecaDAO.listar()

        
        skus_vendidos = {venda.sku for venda in vendas}
        
        pecas_paradas = []
        for peca in pecas:
            
            if peca.estoque_atual > 0 and peca.sku not in skus_vendidos:
                pecas_paradas.append({
                    "sku": peca.sku,
                    "nome_peca": peca.nome_peca,
                    "estoque_atual": peca.estoque_atual
                })
                
        return {
            "quantidade_total": len(pecas_paradas),
            "pecas": pecas_paradas
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar estoque parado: {e}")


@router.get("/qualidade-dados", status_code=status.HTTP_200_OK)
async def obter_qualidade_dados():
    try:
        pecas, vendas, duplicatas = carregar_dados()
        return {
            "linhas_pecas_lidas": len(pecas),
            "linhas_vendas_lidas": len(vendas) + duplicatas,
            "linhas_vendas_validas": len(vendas),
            "linhas_duplicadas_removidas": duplicatas,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao avaliar qualidade dos dados: {e}")