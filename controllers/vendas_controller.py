from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from model.vendas_model import Venda, VendaDAO

router = APIRouter(
    prefix="/vendas",
    tags=["Vendas"]
)

class VendaRequest(BaseModel):
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

@router.get("/", status_code=status.HTTP_200_OK)
async def listar_vendas():
    try:
        return VendaDAO.listar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar vendas: {e}")


def obter_venda_unica(id_venda: str) -> Venda:
    vendas = [venda for venda in VendaDAO.listar() if venda.id_venda == id_venda]
    if not vendas:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    if len(vendas) > 1:
        raise HTTPException(status_code=409, detail="Venda possui mais de uma peça; informe o SKU")
    return vendas[0]


@router.get("/{id_venda}/{sku}", status_code=status.HTTP_200_OK)
async def buscar_venda_por_peca(id_venda: str, sku: str):
    try:
        venda = VendaDAO.busca_por_id(id_venda, sku)
        if venda is None:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return venda
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar venda: {e}")


@router.put("/{id_venda}/{sku}", status_code=status.HTTP_200_OK)
async def atualiza_venda_por_peca(id_venda: str, sku: str, venda: VendaRequest):
    if id_venda != venda.id_venda:
        raise HTTPException(status_code=400, detail="O ID da URL deve ser igual ao ID do corpo da requisição.")
    if VendaDAO.busca_por_id(id_venda, sku) is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    try:
        venda_atualizada = Venda(**venda.model_dump())
        VendaDAO.atualiza(venda_atualizada, sku_antigo=sku)
        return {"mensagem": "Venda atualizada com sucesso!", "venda": venda_atualizada}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar venda: {e}")


@router.delete("/{id_venda}/{sku}", status_code=status.HTTP_200_OK)
async def deletar_venda_por_peca(id_venda: str, sku: str):
    try:
        VendaDAO.cancela(id_venda, sku)
        return {"message": "Venda deletada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar venda: {e}")


@router.get("/{id_venda}", status_code=status.HTTP_200_OK)
async def buscar_venda(id_venda: str):
    try:
        return obter_venda_unica(id_venda)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar venda: {e}")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_venda(venda: VendaRequest):
    try:
        VendaDAO.salva(venda)
        return {"message": "Venda criada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar venda: {e}")

@router.put("/{id_venda}", status_code=status.HTTP_200_OK)
async def atualiza_venda(id_venda: str, venda: VendaRequest):
    venda_existente = obter_venda_unica(id_venda)
        
    if id_venda != venda.id_venda:
        raise HTTPException(status_code=400, detail="O ID da URL deve ser igual ao ID do corpo da requisição.")

    try:
        venda_atualizada = Venda(**venda.model_dump())
        VendaDAO.atualiza(venda_atualizada, sku_antigo=venda_existente.sku)
        return {"mensagem": "Venda atualizada com sucesso!", "venda": venda_atualizada}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar venda: {e}")

@router.delete("/{id_venda}", status_code=status.HTTP_200_OK)
async def deletar_venda(id_venda: str):
    try:
        venda = obter_venda_unica(id_venda)
        VendaDAO.cancela(id_venda, venda.sku)
        return {"message": "Venda deletada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar venda: {e}")