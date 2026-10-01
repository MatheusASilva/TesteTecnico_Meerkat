# **Decisões:**

## 1- Após uma breve análise inicial dos dados fornecidos percebi que existem formatações não padronizadas, desse modo, antes de enviar os dados para um BD mais robusto em nuvem, decidi formatar e padronizar as entradas dos ".csv".

Erros de formatação encontrados e o que foi feito para corrigir:
* 
	- **Datas fora de um padrão específico.**
*		Padronizar para o padrão de entradas de datas de SQL "ano-mes-dia"
	- **Falta de formatação nas strings de SKU em vendas.**
*		Padronizar para a forma "PC-número"
	- **Valores utilizando . ou ,**
*		Padronizar para a forma de entrada de float em SQL "XX.xx"
	- **Categorias, Lojas e Status fora de padrão**
*		Padronizar as strings de acordo com a informação dentro delas
*		Este passo exigiu pesquisa
	- **Espaço antes ou depois de números**
*		Retirar os espaços.
	- **Campos vazios**
*		Atribuir valores nulos aos campos
	- **Símbolos em números**
*		Remoção dos símbolos
	- **Categorias de produtos repetidas e misturadas para o mesmo item**
*		Alinhar as categorias escritas diferentes para uma única

## 2 - Decidi criar uma conta na Supabase e pesquisar um pouco sobre a plataforma, após isso importei os dados do csv para a nuvem.
### Atribui sku como chave primária da tabela de peças e como chave secundária da tabela de vendas;

## 3 - Decidi criar um ambiente virtual para utilizar as bibliotecas necessárias para manipulação do supabase e segurança das chaves de sistemas

## 4 - Adicionei um .env para guardar chaves de sistema, como o acesso ao Supabase

## 5 - Separei as camadas do projeto em modelos, controladores e visualizações e criei os arquivos iniciais dos models.

### Criei os Models de Pecas e Vendas usando o padrão de projeto DAO

**Inseri em VendasDAO a regra de negócio para manipular o estoque da peça diretamente vendida.**
* Melhor formatei os models utilizando LLM, para garantir código limpo e padroes profissionais

#### Testei o funcionamento dos models num arquivo esterno "teste.py"

## 6 - Criei os arquivos de controllers para Peças e Vendas seguindo as rotas descritas no documento do Case Técnico.

