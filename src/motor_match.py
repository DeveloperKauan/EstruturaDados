class TransacaoNode:
    #Nó para armazenar o histórico de transações 
    def __init__(self, id_compra, id_venda, preco, quantidade):
        self.id_compra = id_compra
        self.id_venda = id_venda
        self.preco = preco
        self.quantidade = quantidade
        self.next = None

class MotorMatch:
    def __init__(self):
        self.historico_head = None  
        self.historico_tail = None  

    def registrar_transacao(self, id_compra, id_venda, preco, quantidade): #junta todas as transacoes
        #adiciona uma transação a nossa lista ligada de histórico em O(1)
        nova_transacao = TransacaoNode(id_compra, id_venda, preco, quantidade)

        #conecta tail com a nova transacao e atualiza tail
        if self.historico_tail:
            self.historico_tail.next = nova_transacao
        self.historico_tail = nova_transacao

        #se for a primeira transação, atualiza o head do histórico
        if not self.historico_head:
            self.historico_head = nova_transacao


    def executar(self, lista_compras, lista_vendas): # executa o loop de match e retorna lista de transações geradas
        
        while not lista_compras.is_empty() and not lista_vendas.is_empty():
            melhor_compra = lista_compras.head
            melhor_venda = lista_vendas.head
 
            if melhor_compra.preco < melhor_venda.preco:
                break  #nao tem mais matches possiveis

            # Define a quantidade a ser negociada
            qtd_negociada = min(melhor_compra.quantidade, melhor_venda.quantidade)

            # define o preco de execucao baseado em maker e trader
            if melhor_compra.timestamp <= melhor_venda.timestamp:
                preco_execucao = melhor_compra.preco
            else:
                preco_execucao = melhor_venda.preco

            # Atualiza as quantidades
            melhor_compra.quantidade -= qtd_negociada
            melhor_venda.quantidade -= qtd_negociada

            # Registra a transação
            self._registrar_transacao(
                melhor_compra.id, 
                melhor_venda.id, 
                preco_execucao, 
                qtd_negociada
            )

            # Remove ordens que tiveram quantidade zerada
            if melhor_compra.quantidade == 0:
                lista_compras.remover_no(melhor_compra)
            if melhor_venda.quantidade == 0:
                lista_vendas.remover_no(melhor_venda)

        return self.historico_head 
