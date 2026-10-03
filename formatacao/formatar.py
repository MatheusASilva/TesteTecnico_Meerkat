import unicodedata

import pandas
from datetime import datetime

def formatar_data(data):
    if pandas.isna(data): return None
    data = str(data).strip()
    try:
        if "/" in data:
            data_corrigida = datetime.strptime(data, "%d/%m/%Y")
        elif "-" in data:
            if len(data.split("-")[0]) == 4: #tem data no formato ano-mes-dia e data no formato dia-mes-ano
                return datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
            else:
                return datetime.strptime(data, "%d-%m-%Y").strftime("%Y-%m-%d")
            
        return data_corrigida.strftime("%Y-%m-%d")
    except ValueError:
        return "Data invalida"

def formatar_sku(sku):
    if pandas.isna(sku): 
        return None
    
    return sku.strip().upper()

def formatar_valor(valor):
    if pandas.isna(valor):
        return 0.0
    
    try:
        valor = str(valor).replace("R$", "").strip()

        valor = str(valor).replace("R$", "").strip()
        
        if "." in valor and "," in valor:
            valor = valor.replace(".", "")
            valor = valor.replace(",", ".")
            
        elif "," in valor:
            valor = valor.replace(",", ".")

        valor = str(valor).replace(",", ".")
        valor_float = float(valor)

        return f"{valor_float:.2f}"
    except ValueError:
        return 0.0

def formatar_quantidade(quantidade):
    if pandas.isna(quantidade):
        return 0
    try:
        quantidade = str(quantidade).strip()
        quantidade = str(quantidade).replace(",", ".")
        quantidade_int = int(float(quantidade))
        return quantidade_int
    except ValueError:
        return 0

def formatar_desconto(desconto):
    if pandas.isna(desconto):
        return 0.0
    try:
        desconto = str(desconto).strip()
        desconto = desconto.replace(",", ".")
        desconto = str(desconto).replace("%", "")
        desconto_float = float(desconto)
        return desconto_float
    except ValueError:
        return 0.0

def formatar_textos(texto):
    if pandas.isna(texto):
        return ""
    try:
        texto = str(texto).strip().upper()
        texto = "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

        padronizacao = {
            "FREIO": "FREIOS",
            "FRENAGEM": "FREIOS",
            "FILTRO": "FILTROS"
        }

        texto = padronizacao.get(texto, texto)
        return texto
    except ValueError:
        return ""


pecas_csv = pandas.read_csv("pecas.csv", sep=";")
vendas_csv = pandas.read_csv("vendas.csv", sep=";")

# sku;nome_peca;categoria;custo_unitario;fornecedor;estoque_atual

pecas_csv["sku"] = pecas_csv["sku"].apply(formatar_sku)
pecas_csv["nome_peca"] = pecas_csv["nome_peca"].apply(formatar_textos)
pecas_csv["categoria"] = pecas_csv["categoria"].apply(formatar_textos)
pecas_csv["custo_unitario"] = pecas_csv["custo_unitario"].apply(formatar_valor)
pecas_csv["fornecedor"] = pecas_csv["fornecedor"].apply(formatar_textos)
pecas_csv["estoque_atual"] = pecas_csv["estoque_atual"].apply(formatar_quantidade)

#id_venda;data_venda;loja;cliente;sku;quantidade;preco_unitario;desconto;status;vendedor

vendas_csv["id_venda"] = vendas_csv["id_venda"].apply(formatar_sku)
vendas_csv["data_venda"] = vendas_csv["data_venda"].apply(formatar_data)
vendas_csv["loja"] = vendas_csv["loja"].apply(formatar_textos)
vendas_csv["cliente"] = vendas_csv["cliente"].apply(formatar_textos)
vendas_csv["sku"] = vendas_csv["sku"].apply(formatar_sku)
vendas_csv["quantidade"] = vendas_csv["quantidade"].apply(formatar_quantidade)
vendas_csv["preco_unitario"] = vendas_csv["preco_unitario"].apply(formatar_valor)
vendas_csv["desconto"] = vendas_csv["desconto"].apply(formatar_desconto)
vendas_csv["status"] = vendas_csv["status"].apply(formatar_textos)
vendas_csv["vendedor"] = vendas_csv["vendedor"].apply(formatar_textos)

qtd_duplicatas = vendas_csv.duplicated(subset=['id_venda', 'sku']).sum()

vendas_csv = vendas_csv.drop_duplicates(subset=['id_venda', 'sku'])

pecas_csv.to_csv("pecas_formatadas.csv", index=False, sep=";")
vendas_csv.to_csv("vendas_formatadas.csv", index=False, sep=";")