
# main.py — Interface CLI
# Parte 5 — Kauan

from ordem import OrdemNode                           # Parte 1 — Moli
from fila  import Fila                                # Parte 1 — Moli
from pilha import Pilha                               # Parte 1 — Moli
from lista_encadeada import ListaDuplamenteEncadeada  # Parte 2 — Vini
from motor_match import MotorMatch                    # Parte 3 — Karen


# ESTADO GLOBAL DO SISTEMA
fila_entrada  = Fila()
pilha_undo    = Pilha()
lista_compras = ListaDuplamenteEncadeada(ordem_crescente=False)  # maior preço primeiro
lista_vendas  = ListaDuplamenteEncadeada(ordem_crescente=True)   # menor preço primeiro
motor         = MotorMatch()
transacoes    = []   # histórico de matches gerados
proximo_id    = 1    # contador auto-incremento de IDs

# FUNÇÕES DE INTERFACE

def cabecalho():
    print("\n" + "=" * 50)
    print("   SIMULADOR DE OFERTAS")
    print("=" * 50)

def menu():
    print("\n[1] Inserir nova ordem")
    print("[2] Processar fila de entrada")
    print("[3] Exibir livro de ofertas")
    print("[4] Exibir histórico de transações")
    print("[5] Desfazer última ordem (Undo)")
    print("[0] Sair")
    return input("\nEscolha uma opção: ").strip()

# AÇÕES DO SISTEMA

def inserir_ordem():
    """Recebe dados do usuário e enfileira uma nova ordem."""
    global proximo_id
    print("\n--- NOVA ORDEM ---")

    tipo = input("Tipo (C = Compra / V = Venda): ").strip().upper()
    if tipo not in ("C", "V"):
        print("Tipo inválido. Use C ou V.")
        return

    try:
        preco = float(input("Preço: "))
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("Valor inválido. Tente novamente.")
        return

    # OrdemNode gera o timestamp automaticamente
    ordem = OrdemNode(
        id=proximo_id,
        tipo=tipo,
        preco=preco,
        quantidade=quantidade
    )
    proximo_id += 1

    fila_entrada.enqueue(ordem)
    print(f"\n✔ Ordem #{ordem.id} ({tipo} | R${preco:.2f} | {quantidade} ações) adicionada à fila.")


def processar_fila():
    """Retira ordens da fila e insere no livro de ofertas. Executa o match."""
    if fila_entrada.is_empty():
        print("\nFila de entrada está vazia.")
        return

    processadas = 0
    while not fila_entrada.is_empty():
        ordem = fila_entrada.dequeue()
        if ordem is None:
            break

        # Insere na lista correta conforme tipo da ordem
        if ordem.tipo == "C":
            lista_compras.inserir_ordenado(ordem)
        else:
            lista_vendas.inserir_ordenado(ordem)

        # Salva o ID na pilha de undo para cancelamento futuro
        pilha_undo.push(ordem.id)
        processadas += 1

        # Executa o motor de match — retorna lista de strings da rodada
        novas_transacoes = motor.executar(lista_compras, lista_vendas)
        if novas_transacoes:
            transacoes.extend(novas_transacoes)
            for t in novas_transacoes:
                print(f"  ⚡ MATCH: {t}")

    print(f"\n✔ {processadas} ordem(ns) processada(s).")


def exibir_livro():
    """Mostra o estado atual das listas de compra e venda."""
    print("\n--- LIVRO DE OFERTAS ---")
    print("\n📗 COMPRAS (ordem decrescente de preço):")
    lista_compras.exibir()
    print("\n📕 VENDAS (ordem crescente de preço):")
    lista_vendas.exibir()


def exibir_transacoes():
    """Mostra o histórico de matches gerados."""
    print("\n--- HISTÓRICO DE TRANSAÇÕES ---")
    if not transacoes:
        print("  Nenhuma transação registrada ainda.")
        return
    for i, t in enumerate(transacoes, 1):
        print(f"  [{i}] {t}")


def desfazer_ultima():
    """Remove a última ordem inserida no livro via pilha de undo."""
    if pilha_undo.is_empty():
        print("\nNada para desfazer.")
        return

    id_cancelado = pilha_undo.pop()

    # Tenta remover de ambas as listas só vai achar em uma delas
    lista_compras.remover(id_cancelado)
    lista_vendas.remover(id_cancelado)

    print(f"\n↩ Ordem #{id_cancelado} removida do livro de ofertas.")
    print("⚠ Atenção: se essa ordem já foi executada em um match, ela não existe mais no livro.")


# LOOP PRINCIPAL


def main():
    cabecalho()
    print("Sistema iniciado. Aguardando ordens.\n")

    acoes = {
        "1": inserir_ordem,
        "2": processar_fila,
        "3": exibir_livro,
        "4": exibir_transacoes,
        "5": desfazer_ultima,
    }

    while True:
        opcao = menu()
        if opcao == "0":
            print("\nEncerrando sistema. Até logo!")
            break
        elif opcao in acoes:
            acoes[opcao]()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
