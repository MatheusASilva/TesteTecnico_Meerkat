from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from model.pecas_model import Peca, PecaDAO

router = APIRouter(
    prefix="/pecas",
    tags=["Pecas"]
)

class PecaRequest(BaseModel):
    sku: str
    nome_peca: str
    categoria: str
    custo_unitario: float
    fornecedor: str
    estoque_atual: int


@router.get("/", status_code=status.HTTP_200_OK)
async def listar_pecas():
    try:
        return PecaDAO.listar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar peças: {e}")

@router.get("/{sku}", status_code=status.HTTP_200_OK)
async def buscar_peca(sku: str):
    try:
        peca = PecaDAO.busca_por_sku(sku)
        if peca is None:
            raise HTTPException(status_code=404, detail="Peça não encontrada")
        return peca
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar peça: {e}")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_peca(peca: PecaRequest):
    try:
        PecaDAO.salva(peca)
        return {"message": "Peça criada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar peça: {e}")

@router.put("/{sku}", status_code=status.HTTP_200_OK)
async def atualiza_peca(sku: str, peca: PecaRequest):
    peca_existente = PecaDAO.busca_por_sku(sku)
    if not peca_existente:
        raise HTTPException(status_code=404, detail="Peça não encontrada para atualização.")
        
    if sku != peca.sku:
        raise HTTPException(status_code=400, detail="O SKU da URL deve ser igual ao SKU do corpo da requisição.")

    try:
        peca_atualizada = Peca(**peca.model_dump())
        PecaDAO.atualiza(peca_atualizada)
        return {"mensagem": "Peça atualizada com sucesso!", "peca": peca_atualizada}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar peça: {e}")

@router.delete("/{sku}", status_code=status.HTTP_200_OK)
async def deletar_peca(sku: str):
    peca_existente = PecaDAO.busca_por_sku(sku)
    if not peca_existente:
        raise HTTPException(status_code=404, detail="Peça não encontrada para exclusão.")
    try:
        PecaDAO.deleta(sku)
        return {"mensagem": "Peça deletada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar peça: {e}")
    