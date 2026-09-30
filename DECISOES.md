### **Decisões:**

### 1- Após uma breve análise inicial dos dados fornecidos percebi que existem formatações não padronizadas, desse modo, antes de enviar os dados para um BD mais robusto em nuvem, decidi formatar e padronizar as entradas dos ".csv".

Erros de formatação encontrados e o que foi feito para corrigir:
	
	- **Datas fora de um padrão específico.**
		Padronizar para o padrão de entradas de datas de SQL "ano-mes-dia"
	- **Falta de formatação nas strings de SKU em vendas.**
		Padronizar para a forma "PC-número"
	- **Valores utilizando . ou ,**
		Padronizar para a forma de entrada de float em SQL "XX.xx"
	- **Categorias, Lojas e Status fora de padrão**
		Padronizar as strings de acordo com a informação dentro delas
	- **Espaço antes ou depois de números**
		Retirar os espaços.
	- **Campos vazios**
		Atribuir valores nulos aos campos
	- **Símbolos em números**
		Remoção dos símbolos
	- **Categorias de produtos repetidas e misturadas para o mesmo item**
		Alinhar as categorias escritas diferentes para uma única