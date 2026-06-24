from ordem import OrdemNode

#Nome da Classe Principal da Lista Encadeada
"""
class ListaDuplamenteEncadeada:
    def inserir_ordenado(self, ordem): ...  # insere mantendo a ordem correta
    def remover(self, id):             ...  # remove nó pelo ID
    def topo(self):                    ...  # retorna o primeiro nó sem remover
    def is_empty(self):                ...  # retorna True se vazia
    def exibir(self):                  ...  # printa a lista pra debug
"""
#Criando a Classe NoLista para representar cada nó da lista encadeada.
class NoLista:
    def __init__(self, ordem: OrdemNode):
        self.ordem = ordem
        self.next = None
        self.prev = None
#Criando a classe que define a Lista Duplamente Encadeada, que será utilizada para armazenar as ordens de compra e venda.
class ListaDuplamenteEncadeada:
    def __init__(self, ordem_crescente=True):
        self.cabeca = None
        self.ordem_crescente = ordem_crescente
    
    #Estabelecendo a lógica de comparação entre valores da lista baseada no seu tipo.
    def _comparar(self, preco_novo, preco_existente):
        if self.ordem_crescente:
            return preco_novo < preco_existente
        else:
            return preco_novo > preco_existente
    
    def inserir_ordenado(self,ordem):
        #Aqui, colocamos a ordem no Nó
        novo_no = NoLista(ordem)

        #Lista vazia: novo nó se torna a cabeça da lista
        if self.cabeca is None:
            self.cabeca = novo_no
            return 
        
        # Caso 2: Somente quando novo preço deve ficar antes de tudo (é a nova cabeça).
        if self._comparar(novo_no.ordem.preco, self.cabeca.ordem.preco):
            novo_no.next = self.cabeca
            self.cabeca.prev = novo_no
            self.cabeca = novo_no
            return
        
        # Caso 3: Percorre a lista até achar a posição correta
        atual = self.cabeca
        while atual.next is not None and not self._comparar(novo_no.ordem.preco, atual.next.ordem.preco):
            atual = atual.next

        # Insere o novo nó entre 'atual' e 'atual.next'
        novo_no.next = atual.next
        novo_no.prev = atual
        if atual.next is not None:
            atual.next.prev = novo_no
        atual.next = novo_no

    def remover_no(self, no):
        if no.prev is not None:
            no.prev.next = no.next
        else:
            self.cabeca = no.next

        if no.next is not None:
            no.next.prev = no.prev

        return no.ordem

    def remover(self, id):
        atual = self.cabeca

        while atual is not None and atual.ordem.id != id:
            atual = atual.next

        if atual is None:
            return None

        return self.remover_no(atual)
    
    def topo(self):
        if self.cabeca is None:
            return None
        return self.cabeca.ordem

    def is_empty(self):
        return self.cabeca is None

    def exibir(self):
        atual = self.cabeca
        while atual is not None:
            print(f"ID: {atual.ordem.id} | Preço: {atual.ordem.preco} | Quantidade: {atual.ordem.quantidade}")
            atual = atual.next