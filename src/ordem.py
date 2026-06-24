# Nome da classe principal
""" Classe OrdemNode:
```python
class OrdemNode:
    def __init__(self, id, tipo, preco, quantidade, timestamp):
        # tipo: 'C' para Compra, 'V' para Venda
```
"""

# importações:
from datetime import datetime

class OrdemNode:

  # as ordens de negociação que serão inseridas

  proximo_id = 1

  def __init__(self, tipo:str, preco:float, quantidade:int):

    self.id = OrdemNode.proximo_id
    OrdemNode.proximo_id += 1 
    self.tipo = tipo  # 'C' compra ou 'V' venda
    self.preco = preco
    self.quantidade = quantidade
    self.timestamp = datetime.now()
