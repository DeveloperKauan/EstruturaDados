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

    # CORREÇÃO: removida linha "self.ponteiro_frente.prev = None"
    # NoFila não possui atributo prev, causaria AttributeError

    return no.ordem
  
  def is_empty(self): # retorna True se vazia
     
    if self.ponteiro_frente is None and self.ponteiro_atras is None:
       return True
    
    return False
