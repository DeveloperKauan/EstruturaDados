class TransacaoNode:
    # Nó para armazenar o histórico de transações 
    def __init__(self, id_compra, id_venda, preco, quantidade):
        self.id_compra = id_compra
        self.id_venda = id_venda
        self.preco = preco
        self.quantidade = quantidade
        self.next = None

    def __str__(self):
        return f"Compra #{self.id_compra} x Venda #{self.id_venda} | {self.quantidade} ações a R${self.preco:.2f}"

class MotorMatch:
    def __init__(self):
        self.historico_head = None
        self.historico_tail = None

    def registrar_transacao(self, id_compra, id_venda, preco, quantidade):
        # CORREÇÃO: método era chamado como _registrar_transacao (com underline) mas definido sem
        nova_transacao = TransacaoNode(id_compra, id_venda, preco, quantidade)

        if self.historico_tail:
            self.historico_tail.next = nova_transacao
        self.historico_tail = nova_transacao

        if not self.historico_head:
            self.historico_head = nova_transacao

    def executar(self, lista_compras, lista_vendas):
        # CORREÇÃO: agora retorna lista Python com as transações geradas NESSA rodada
        # (antes retornava self.historico_head acumulado de todas as rodadas)
        transacoes_da_rodada = []

        while not lista_compras.is_empty() and not lista_vendas.is_empty():
            melhor_compra = lista_compras.topo()  # OO: acessa via método, não atributo interno
            melhor_venda = lista_vendas.topo()    # OO: acessa via método, não atributo interno

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
            self.registrar_transacao(
                melhor_compra.id,
                melhor_venda.id,
                preco_execucao,
                qtd_negociada
            )

            # Guarda na lista da rodada para retornar ao main.py
            transacoes_da_rodada.append(
                f"Compra #{melhor_compra.id} x Venda #{melhor_venda.id} | "
                f"{qtd_negociada} ações a R${preco_execucao:.2f}"
            )

            # Remove ordens que tiveram quantidade zerada
            if melhor_compra.quantidade == 0:
                lista_compras.remover_no(melhor_compra)
            if melhor_venda.quantidade == 0:
                lista_vendas.remover_no(melhor_venda)

        return transacoes_da_rodada
