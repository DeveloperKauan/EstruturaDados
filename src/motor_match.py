# Definir nome da classe

class MotorMatch:
    def executar(self, lista_compras, lista_vendas): # executa o loop de match e retorna lista de transações geradas
        transacoes = [] #histórico de transações

        while not lista_compras.is_empty() and not lista_vendas.is_empty():
            melhor_compra = lista_compras.head
            melhor_venda = lista_vendas.head
 
            if melhor_compra.preco < melhor_venda.preco:
                break  #nao tem mais matches possiveis

            # Define a quantidade a ser negociada
            qtd_negociada = min(melhor_compra.quantidade, melhor_venda.quantidade)

            if melhor_compra.timestamp <= melhor_venda.timestamp:
                preco_execucao = melhor_compra.preco
            else:
                preco_execucao = melhor_venda.preco

            # Atualiza as quantidades
            melhor_compra.quantidade -= qtd_negociada
            melhor_venda.quantidade -= qtd_negociada

            # Registra a transação
            transacoes.append({
                "id_compra": melhor_compra.id,
                "id_venda": melhor_venda.id,
                "preco": preco_execucao,
                "quantidade": qtd_negociada,
            })

            # Remove ordens que tiveram quantidade zerada
            if melhor_compra.quantidade == 0:
                lista_compras.remover_no(melhor_compra)
            if melhor_venda.quantidade == 0:
                lista_vendas.remover_no(melhor_venda)

        return transacoes
