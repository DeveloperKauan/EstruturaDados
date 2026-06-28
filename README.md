# Simulador de Livro de Ofertas e Performance de Estruturas

Trabalho prático da disciplina **Estrutura de Dados-SME0827-101-2026**

Professor: **Marcos Mansano Furlan**

## Integrantes do grupo:
Vinícius Alves de Oliveira - 15498077

Karen Yukari Taira - 17426142 

Maria Olívia Meca de Siqueira - 17099902 

Fernanda Rubio de Mello - 17108710 

Kauan Yuri Garcia de Souza - 16832064

---

## 1. Objetivo

Este trabalho tem como objetivo aplicar conceitos de estruturas de dados lineares (Listas Encadeadas, Pilhas e Filas) no desenvolvimento de um motor de negociação financeira. O foco está na análise assintótica e na comparação prática da performance dessas estruturas em cenários de grande volume de dados.

O sistema simula um **Livro de Ofertas (Order Book)**: ele recebe ordens de compra e venda de ativos, organiza essas ordens em estruturas ordenadas e executa automaticamente o "casamento" (*match*) entre compradores e vendedores quando os preços são compatíveis.

Todas as estruturas de dados foram implementadas por meio de nós encadeados aprendidos no curso.

---

## 2. Visão Geral do Fluxo do Sistema

1. **Nova ordem chega** → é inserida no fim da **Fila de Entrada** (`ENQUEUE`).
2. O sistema retira a ordem do início da fila (`DEQUEUE`).
3. A ordem é inserida de forma ordenada no **Livro de Ofertas**:
   - Se for Compra (`'C'`) → Lista de Compras, em ordem **decrescente** de preço.
   - Se for Venda (`'V'`) → Lista de Vendas, em ordem **crescente** de preço.
4. O ID da ordem inserida é empilhado na **Pilha de Undo**.
5. O **Motor de Match** verifica se o preço do início da Lista de Compras é maior ou igual ao preço do início da Lista de Vendas. Enquanto essa condição for satisfeita:
   - Executa a transação;
   - Reduz a quantidade das ordens envolvidas;
   - Remove qualquer ordem cuja quantidade tenha chegado a zero.
6. O processo se repete enquanto houver ordens na Fila de Entrada.

---

## 3. Estrutura do Repositório

```
├── notebooks/
│   └── analise.ipynb        # Análise empírica de desempenho 
├── src/
│   ├── ordem.py             # Classe OrdemNode 
│   ├── fila.py              # Fila de Entrada
│   ├── pilha.py             # Pilha de Undo 
│   ├── lista_encadeada.py   # Livro de Ofertas 
│   ├── motor_match.py       # Motor de Match
│   └── main.py              # Interface CLI / integração 
└── README.md
```

---

## 4. Estruturas de Dados Implementadas

### 4.1 Ordem (`ordem.py`)

Classe `OrdemNode`, que representa cada ordem de negociação inserida no sistema. Atributos:

| Atributo | Tipo | Descrição |
|---|---|---|
| `id` | `int` | Identificador único da ordem, gerado automaticamente de forma incremental |
| `tipo` | `char` | `'C'` para Compra ou `'V'` para Venda |
| `preco` | `float` | Valor unitário que o investidor aceita pagar ou receber |
| `quantidade` | `int` | Volume de ações a serem negociadas |
| `timestamp` | `datetime` | Momento exato da entrada da ordem no sistema, gerado automaticamente |

### 4.2 Fila de Entrada (`fila.py`)

Implementa uma fila **FIFO** (*First In, First Out*) por meio de nós encadeados (`NoFila`), com ponteiros de frente e de trás.

- `enqueue(ordem)`: insere uma ordem no fim da fila — **O(1)**.
- `dequeue()`: remove e retorna a ordem do início da fila — **O(1)**.
- `is_empty()`: retorna `True` se a fila estiver vazia.

A fila de entrada existe para garantir que, mesmo com grandes volumes de ordens chegando em curto espaço de tempo, nenhuma ordem seja perdida: a inserção na fila é sempre O(1), independentemente do custo O(n) de inserção ordenada no livro de ofertas.

### 4.3 Pilha de Undo (`pilha.py`)

Implementa uma pilha **LIFO** (*Last In, First Out*) por meio de nós encadeados (`NoPilha`).

- `push(ordem_id)`: empilha o ID de uma ordem recém-inserida no livro — **O(1)**.
- `pop()`: desempilha e retorna o último ID inserido — **O(1)**.
- `is_empty()`: retorna `True` se a pilha estiver vazia.

Permite que a última ordem inserida no livro de ofertas seja cancelada rapidamente. Caso o ID recuperado já tenha sido removido do livro anteriormente (por exemplo, por ter sido totalmente executado em um match), a remoção simplesmente não localiza nenhum nó correspondente, esse caso é tratado sem gerar erro.

### 4.4 Livro de Ofertas (`lista_encadeada.py`)

Implementa uma lista **duplamente encadeada ordenada** (`ListaDuplamenteEncadeada`), usada tanto para a Lista de Compras quanto para a Lista de Vendas a mesma classe é instanciada duas vezes, com uma configuração diferente de ordenação:

```python
lista_compras = ListaDuplamenteEncadeada(ordem_crescente=False)  # maior preço primeiro
lista_vendas  = ListaDuplamenteEncadeada(ordem_crescente=True)   # menor preço primeiro
```

- `inserir_ordenado(ordem)`: insere uma ordem mantendo a lista ordenada, percorrendo os nós existentes até encontrar a posição correta **O(n)**.
- `remover(id)`: localiza e remove o nó correspondente a um ID, religando os ponteiros `next`/`prev` dos vizinhos. Retorna `None` se o ID não for encontrado (cenário esperado quando a ordem já foi finalizada por um match anterior).
- `remover_no(no)`: remove diretamente um nó já localizado, sem necessidade de busca usado internamente pelo Motor de Match, que já possui a referência ao nó por meio do `topo()`.
- `topo()`: retorna a ordem (`OrdemNode`) do primeiro nó da lista, sem removê-la.
- `is_empty()`: retorna `True` se a lista estiver vazia.
- `exibir()`: imprime o conteúdo da lista, nó a nó, para fins de depuração.

A inserção e a remoção são feitas inteiramente por manipulação de ponteiros (`next` e `prev`), sem apoio em estruturas nativas, cobrindo todos os casos de borda: lista vazia, inserção/remoção na cabeça, no meio, no fim, e lista com um único elemento — evitando a criação de nós órfãos.

### 4.5 Motor de Match (`motor_match.py`)

Responsável por executar o casamento de ordens. Enquanto o preço no início da Lista de Compras for maior ou igual ao preço no início da Lista de Vendas:

1. Recupera a melhor ordem de compra e a melhor ordem de venda (`topo()` de cada lista).
2. Calcula a quantidade negociada como o mínimo entre as quantidades das duas ordens.
3. Define o preço de execução com base em qual ordem chegou primeiro ao sistema (a ordem mais antiga, o *maker*, define o preço).
4. Reduz a quantidade das duas ordens envolvidas.
5. Remove do livro qualquer ordem cuja quantidade tenha chegado a zero.
6. Registra a transação em um histórico encadeado (`TransacaoNode`) para consulta posterior.

O laço se repete até que a condição de match deixe de ser satisfeita ou uma das listas fique vazia.

### 4.6 Interface e Integração (`main.py`)

Disponibiliza uma interface de linha de comando (CLI) que integra todas as estruturas acima:

| Opção | Ação |
|---|---|
| 1 | Inserir nova ordem (enfileira na Fila de Entrada) |
| 2 | Processar a Fila de Entrada (insere no livro, aciona o Motor de Match) |
| 3 | Exibir o estado atual do Livro de Ofertas (Compras e Vendas) |
| 4 | Exibir o histórico de transações já executadas |
| 5 | Desfazer a última ordem inserida (Undo, via Pilha) |
| 0 | Sair do sistema |

---

## 5. Análise de Desempenho (`notebooks/analise.ipynb`)

O notebook documenta:

- **Complexidade teórica** das operações de cada estrutura (Fila e Pilha em O(1); inserção ordenada na Lista Duplamente Encadeada em O(n)).
- **Análise empírica**, com testes de volume crescente de ordens, medindo o tempo médio de execução de cada estrutura e apresentando os resultados em gráficos comparativos.
- **Discussão dos resultados**, relacionando o comportamento observado experimentalmente com o esperado pela análise assintótica, e concluindo que a Lista Duplamente Encadeada apresenta maior custo computacional à medida que o volume de ordens cresce, devido à necessidade de percorrer os nós para manter a ordenação.

---

## 6. Requisitos Técnicos Atendidos

- ✅ Todas as estruturas (Fila, Pilha, Lista Duplamente Encadeada) foram implementadas manualmente, por meio de nós encadeados, sem uso de `list`, `deque` ou qualquer estrutura nativa do Python.
- ✅ Lógica de ponteiros (`next`/`prev`) corretamente manipulada, sem geração de nós órfãos.
- ✅ Organização em classes bem definidas (`OrdemNode`, `NoFila`/`Fila`, `NoPilha`/`Pilha`, `NoLista`/`ListaDuplamenteEncadeada`, `MotorMatch`).
- ✅ Inserção ordenada em O(n) e operações de fila/pilha em O(1), conforme exigido.
- ✅ Motor de Match implementado conforme a especificação: verifica a condição de preço, executa a transação, atualiza ou remove os nós envolvidos.
- ✅ Análise de desempenho documentada no notebook Jupyter, com gráficos comparativos.
- ✅ Versionamento incremental via GitHub, refletindo a divisão de tarefas entre os integrantes.

---


## 7. Como Executar

```bash
cd src
python main.py
```

O sistema abrirá um menu interativo no terminal, permitindo inserir ordens, processar a fila, visualizar o livro de ofertas e o histórico de transações, e desfazer a última ordem inserida.

Para reproduzir a análise de desempenho:

```bash
cd notebooks
jupyter notebook analise.ipynb
```
