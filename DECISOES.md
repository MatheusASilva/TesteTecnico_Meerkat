# **Decisões:**

### 1- Após uma breve análise inicial dos dados fornecidos percebi que existem formatações não padronizadas, desse modo, antes de enviar os dados para um BD mais robusto em nuvem, decidi formatar e padronizar as entradas dos ".csv".

<details>
<summary><b>Erros de formatação encontrados e o que foi feito para corrigir:</b></summary>
<br>

**Datas fora de um padrão específico.**

-     Padronizar para o padrão de entradas de datas de SQL "ano-mes-dia"

**Falta de formatação nas strings de SKU em vendas.**

-     Padronizar para a forma "PC-número"

**Valores utilizando . ou ,**

-     Padronizar para a forma de entrada de float em SQL "XX.xx"

**Categorias, Lojas e Status fora de padrão**

-     Padronizar as strings de acordo com a informação dentro delas
-     Este passo exigiu pesquisa

**Espaço antes ou depois de números**

-     Retirar os espaços.

**Campos vazios**

-     Atribuir valores nulos aos campos

**Símbolos em números**

-     Remoção dos símbolos

**Categorias de produtos repetidas e misturadas para o mesmo item**

-     Alinhar as categorias escritas diferentes para uma única

</details>

### 2 - Decidi criar uma conta na Supabase e pesquisar um pouco sobre a plataforma, após isso importei os dados do csv para a nuvem.

- Atribui `sku` como chave primária da tabela de peças e como chave secundária da tabela de vendas;
- Atribui `id_vendas` e `sku` como chaves da tabela vendas.

### 3 - Decidi criar um ambiente virtual para utilizar as bibliotecas necessárias para manipulação do supabase e segurança das chaves de sistemas

- Permitindo no fim o uso do comando `pip freeze > requirements.txt` que facilitou a importação de bibliotecas no Render

### 4 - Adicionei um .env para guardar chaves de sistema, como o acesso ao Supabase

### 5 - Separei as camadas do projeto em modelos, controladores e visualizações e criei os arquivos iniciais da camada model.

<details>
<summary><b>Construção da camada Model:</b></summary>

- **Criei os Models de Pecas e Vendas usando o padrão de projeto DAO**

- **Inseri em VendasDAO a regra de negócio para manipular o estoque da peça diretamente vendida.**

-     Melhor formatei os models utilizando LLM, para garantir código limpo e padroes profissionais

- **Testei o funcionamento dos models num arquivo externo `teste.py`**

</details>

### 6 - Criei os arquivos de controllers para Peças e Vendas seguindo as rotas descritas no documento do Case Técnico.

**Inseri a criação das rotas baseadas no que foi pedido no case.**

### 7 - Criei um controller para o dashboard pensando em retornar os dados principais pedidos no Case Técnico.

<details>
<summary><b>Inseri algumas rotas próprias, segue a descrição de todas as rotas do sistema::</b></summary>

### ⚙️ Peças (`pecas_controller.py`)

| Método     | Rota          | O que faz                                        |
| ---------- | ------------- | ------------------------------------------------ |
| **GET**    | `/pecas`      | Lista todas as peças cadastradas                 |
| **GET**    | `/pecas/:sku` | Devolve uma peça específica através do seu SKU   |
| **POST**   | `/pecas`      | Cria uma nova peça no banco de dados             |
| **PUT**    | `/pecas/:sku` | Atualiza os dados de uma peça existente pelo SKU |
| **DELETE** | `/pecas/:sku` | Apaga uma peça do sistema pelo SKU               |

### 🛒 Vendas (`vendas_controller.py`)

| Método     | Rota                     | O que faz                                                    |
| ---------- | ------------------------ | ------------------------------------------------------------ |
| **GET**    | `/vendas`                | Lista todas as vendas registradas                            |
| **GET**    | `/vendas/:id_venda/:sku` | Devolve uma venda específica através da chave composta       |
| **POST**   | `/vendas`                | Cria o registro de uma nova venda                            |
| **PUT**    | `/vendas/:id_venda/:sku` | Atualiza os dados de uma venda existente pela chave composta |
| **DELETE** | `/vendas/:id_venda/:sku` | Cancela uma venda específica pela chave composta             |

### 📊 Dashboard (`dashboard.py`)

| Método  | Rota                                   | O que faz                                                                                     |
| ------- | -------------------------------------- | --------------------------------------------------------------------------------------------- |
| **GET** | `/dashboard/faturamento-total`         | Devolve o faturamento líquido total, calculando apenas vendas concluídas                      |
| **GET** | `/dashboard/faturamento-por-categoria` | Lista as categorias ordenadas pelo valor total faturado                                       |
| **GET** | `/dashboard/estoque-parado`            | Retorna a quantidade e a lista de peças que têm estoque maior que zero e nunca foram vendidas |
| **GET** | `/dashboard/qualidade-dados`           | Devolve estatísticas sobre a limpeza dos dados (linhas lidas, válidas e duplicatas removidas) |

</details>

### 8 - Criação da camada View

<details>
<summary><b>Construção da camada View:</b></summary>

- **Optei por uma construção simples, baseada em HTML, CSS e principalmente JavaScript.**
- **Optei pela utilização de Bootstrap**
- **Utilização de IA para codificação e estilização da página da maneira adequada para apresentar o site**
- **Criação de Filtros de busca nas páginas**

</details>

### 9 - Percepção de erros no tratamento de dados

- Percebi que ao tratar os dados da forma que fiz, acabei fazendo com que valores acima de 1000 que estivessem com um "." após as casas de milhar geraram campos de vendas com valores 0.
- Também percebi que uma falha de não remover "," em alguns valores transformou os descontos em itens nulos com valores 0.

**Solução:**

-     Gerei um novo script para formatar esses dados de forma correta e inserir no Supabase de forma automática, como pede o Case.

### 10 - Melhorias finais antes da publicação

- Percebi que o script de formatação dependia do local em que o comando era executado. Decidi usar o caminho do próprio arquivo para que a leitura dos CSVs não dependa de caminhos relativos ao terminal. O comando documentado continua sendo executado a partir da raiz do projeto.
- Separei a leitura e o tratamento dos CSVs em funções. Dessa forma, importar o módulo não executa a carga automaticamente e o processo fica mais fácil de testar.
- Adicionei à validação de edição de vendas o campo `sku` pois apenas `id_venda` poderia alterar mais de um registro por vez.
- Mantive o upsert no envio para o Supabase. As peças usam o SKU como conflito e as vendas usam a combinação do id da venda com o SKU, pois encontrei registros repetidos para a mesma combinação.
- Adicionei um README com as respostas do case e o passo a passo para executar o projeto. Também adicionei testes para os formatos de data, valor, desconto e deduplicação.
- Adicionei a View como arquivo estático da própria API. Assim, o dashboard pode ser acessado pela mesma aplicação através da rota `/`.
- Ao editar uma venda, decidi desfazer primeiro o impacto do registro antigo no estoque e aplicar o impacto do registro novo. Isso evita que alterações de quantidade, SKU ou status deixem o estoque inconsistente.
- Utilizei IA para validar o sistema e incrementar pontos soltos e criar partes do README.md.

### 11 - Informações extras no Dashboard

- Decidi colocar a qualidade dos dados em um bloco menor dentro da área de insights. Assim o Sr. Andrade consegue ver quantas linhas foram lidas, quantas ficaram válidas e quantas duplicidades foram removidas, mas essa informação não tira o foco das três respostas principais.
- Também adicionei um ranking com as cinco peças que mais faturaram. O ranking considera apenas vendas concluídas e acompanha os filtros de período, loja e categoria, para permitir uma leitura mais útil do resultado.
- Reutilizei o formulário de edição para cadastrar novas vendas. Quando não existe uma venda em edição, o formulário envia `POST`; quando existe, envia `PUT` usando a chave composta. Assim a tela continua simples e não cria uma etapa separada para uma operação parecida.
- Percebi que a rota de qualidade ainda lia os CSVs toda vez que o Dashboard era aberto. Para deixar a View independente dos arquivos de entrada, criei a tabela `qualidade_dados`, atualizada pela carga e consultada apenas pelo `QualidadeDAO` na camada model.

### 12 - Atualizei o arquivo "DECISOES.md"

### 13 - Enviei a aplicação para a plataforma Render.

# Autenticação e segurança

- Apesar de possuir experiência com implementação de sistemas de login e proteção de rotas, optei por não incluir uma camada de autenticação na solução deste Case, visando focar estritamente no escorpo e também em facilitar a avaliação para a banca avaliadora testar a aplicação e a API
