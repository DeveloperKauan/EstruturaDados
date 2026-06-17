# Definir nome da classe

class MotorMatch:
    def __init__(self):
        self.transacoes = []   # armazena histórico de transações

    def executar(self, lista_compras, lista_vendas): ...  # executa o loop de match e retorna lista de transações geradas
    while not lista_compras.is_empty() and not lista_vendas.is_empty():
        melhor_compra = lista_compras.head
        melhor_venda = lista_vendas.head
 
        if melhor_compra.preco < melhor_venda.preco:
            break  #nao tem mais matches possiveis

        qtd_negociada = min(melhor_compra.quantidade, melhor_venda.quantidade)

        if melhor_compra.timestamp <= melhor_venda.timestamp:
            preco_execucao = melhor_compra.preco
        else:
            preco_execucao = melhor_venda.preco
    