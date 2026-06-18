# Nome da Classe Principal
"""
class Pilha:
    def push(self, id):  ...  # empilha o ID
    def pop(self):       ...  # desempilha e retorna o ID
    def is_empty(self):  ...  # retorna True se vazia
"""

class NoPilha:

    def __init__(self, ordem_id):

        self.ordem_id = ordem_id
        self.next = None


class Pilha:

    def __init__(self):

        self.topo = None

    def push(self, ordem_id):  # empilha o ID

        novo_no = NoPilha(ordem_id)

        novo_no.next = self.topo
        self.topo = novo_no

    def pop(self):  # remove o último ID inserido

        if self.topo is None:
            return None

        no = self.topo
        self.topo = self.topo.next

        return no.ordem_id

    def is_empty(self): # retorna True se vazia

        return self.topo is None
    
# pilha = Pilha()

# print("Pilha vazia?", pilha.is_empty())

# pilha.push(1)
# pilha.push(2)
# pilha.push(3)

# print("Pilha vazia?", pilha.is_empty())

# print("Removendo:", pilha.pop())
# print("Removendo:", pilha.pop())
# print("Removendo:", pilha.pop())

# print("Pilha vazia?", pilha.is_empty())

# print("Tentando remover novamente:", pilha.pop())