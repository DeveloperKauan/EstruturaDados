# Nome da classe principal
"""
Classe Fila:

python
class Fila:
    def enqueue(self, ordem): ...  # adiciona no fim
    def dequeue(self):        ...  # remove e retorna do início
    def is_empty(self):       ...  # retorna True se vazia
"""

class NoFila:

    def __init__(self, ordem):
        self.ordem = ordem
        self.next = None

class Fila:

  # onde as ordens ficam esperando para serem processadas

  def __init__(self):

    self.ponteiro_frente = None
    self.ponteiro_atras = None

  def enqueue(self, ordem): # método enqueue -> adiciona uma ordem no final; 

    novo_no = NoFila(ordem)

    if (self.ponteiro_atras is None):

      self.ponteiro_frente = novo_no
      self.ponteiro_atras = novo_no

    else:

      self.ponteiro_atras.next = novo_no
      self.ponteiro_atras = novo_no

  def dequeue(self): # método dequeue -> remove a primeira ordem; 

    if self.ponteiro_frente is None:
        return None

    no = self.ponteiro_frente
    self.ponteiro_frente = self.ponteiro_frente.next

    if self.ponteiro_frente is None:
        self.ponteiro_atras = None
    else:
        self.ponteiro_frente.prev = None

    return no.ordem
  
  def is_empty(self): # retorna True se vazia
     
    if self.ponteiro_frente is None and self.ponteiro_atras is None:
       return True
    
    return False

# fila = Fila()

# print("Fila vazia?", fila.is_empty())

# fila.enqueue("Ordem 1")
# fila.enqueue("Ordem 2")
# fila.enqueue("Ordem 3")

# print("Fila vazia?", fila.is_empty())

# print("Removendo:", fila.dequeue())
# print("Removendo:", fila.dequeue())
# print("Removendo:", fila.dequeue())

# print("Fila vazia?", fila.is_empty())