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