class TransacaoNode:
    # Nó para armazenar o histórico de transações 
    def __init__(self, id_compra, id_venda, preco, quantidade):
        self.id_compra = id_compra
        self.id_venda = id_venda
        self.preco = preco
        self.quantidade = quantidade
        self.next = None

    def __str__(self):
        return "Compra #%s x Venda #%s | %s acoes a R$%.2f" % (
            self.id_compra,
            self.id_venda,
            self.quantidade,
            self.preco
        )
    def __init__(self):
        self.historico_head = None 
        self.historico_tail = None

    def registrar_transacao(self, id_compra, id_venda, preco, quantidade): #registra uma transacao no historico
        # CORREÇÃO: método era chamado como _registrar_transacao (com underline) mas definido sem
        nova_transacao = TransacaoNode(id_compra, id_venda, preco, quantidade)

        if self.historico_tail:
            self.historico_tail.next = nova_transacao
        self.historico_tail = nova_transacao

        if not self.historico_head:
            self.historico_head = nova_transacao


    def pegar_primeira_ordem(self, lista_ordens): #pega o maior valor se for compra e o menor valor se for venda
        return lista_ordens.topo()

    def remover_ordem(self, lista_ordens, ordem): #remove a ordem caso ela chegue a quantidade 0
        lista_ordens.remover(ordem.id)

    def executar(self, lista_compras, lista_vendas):
        # 'class Fila' de outro arquivo para guardar as transacoes dessa rodada.
        # cria uma fila para armazenar as transações da rodada
        transacoes_da_rodada = Fila()

        while not lista_compras.is_empty() and not lista_vendas.is_empty():
            melhor_compra = self.pegar_primeira_ordem(lista_compras)
            melhor_venda = self.pegar_primeira_ordem(lista_vendas)

 
            if melhor_compra.preco < melhor_venda.preco:
                break  # não tem mais matches possíveis

            # Define a quantidade a ser negociada
            qtd_negociada = min(melhor_compra.quantidade, melhor_venda.quantidade)

            # Define o preço de execução baseado em quem chegou primeiro (maker) 
            if melhor_compra.timestamp <= melhor_venda.timestamp:
                preco_execucao = melhor_compra.preco
            else:
                preco_execucao = melhor_venda.preco

            # Atualiza as quantidades
            melhor_compra.quantidade -= qtd_negociada
            melhor_venda.quantidade -= qtd_negociada

            # CORREÇÃO: chamada sem underline, igual ao nome do método definido acima
            #Cria e salva a transação no histórico.
            transacao = self.registrar_transacao(
                melhor_compra.id,
                melhor_venda.id,
                preco_execucao,
                qtd_negociada
            )

            #Coloca a transação na fila da rodada.
            transacoes_da_rodada.enqueue(transacao)

            # Remove ordens que tiveram quantidade zerada
            if melhor_compra.quantidade == 0:
                lista_compras.remover_no(melhor_compra)
            if melhor_venda.quantidade == 0:
                lista_vendas.remover_no(melhor_venda)

        return transacoes_da_rodada
