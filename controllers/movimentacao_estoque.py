import threading
from tkinter import messagebox
from controllers.produtos import Produto
from controllers.interface import adicionar_produto_normal, adicionar_produto_rapido, atualizar_valor_total, atualizar_treeview, atualizar_interface_produto
from utils.loading_screen import mostrar_tela_carregamento
import time


loading_process = None
def validar_dados(label_data, produtos, movimento_tipo):
    """Valida os dados antes de registrar o movimento."""
    if not label_data.cget("text"):
        messagebox.showerror("Erro", "Por favor, selecione uma data antes de salvar.")
        return False
    if not produtos:
        messagebox.showerror("Erro", "Nenhum produto selecionado.")
        return False
    # Verifica se todos os produtos têm dados completos
    for produto in produtos:
        if len(produto) < 6:
            messagebox.showerror("Erro", "Os dados do produto estão incompletos.")
            return False
    if movimento_tipo not in ["saida", "devolucao", "entrada"]:
        messagebox.showerror("Erro", f"Tipo de movimento '{movimento_tipo}' desconhecido.")
        return False
    return True






def registrar_movimento(label_data, group_var, produtos, sistema_estoque, tree, label_preco_total, movimento_tipo):
    """Função principal para registrar a movimentação de produtos (saída, devolução, entrada)."""
    
    # Função para atualizar o progresso
    def atualizar_progresso(barra, label, progresso, tela):
        barra.set(progresso / 100)  # Atualiza a barra de progresso, normalizando para 0-1
        label.configure(text=f"{progresso}%")  # Atualiza o texto da porcentagem
        tela.update_idletasks()  # Atualiza a interface de carregamento

    def processar_movimento():
        """Função que processa o movimento dos produtos e atualiza a interface."""
        # Valida os dados antes de prosseguir
        if not validar_dados(label_data, produtos, movimento_tipo):
            tela.destroy()  # Certifique-se de destruir a tela quando terminar
            return
        
        # Exibe a tela de carregamento
        tela, barra_progresso, label_percentual = mostrar_tela_carregamento(tree.master, maximo=len(produtos))
        
        cliente_selecionado = group_var.get()
        data = label_data.cget("text")  # Obtém a data selecionada

        # Processa cada produto e registra o movimento
        for i, produto in enumerate(produtos):
            nome, codigo_barras, preco, quantidade, grupo, sub_grupo = produto[:6]
       
            produto_obj = Produto(None, nome, codigo_barras, preco, quantidade, grupo, sub_grupo)

            # Registra o movimento conforme o tipo
            if movimento_tipo == "saida":
                sistema_estoque.saida_produto(produto_obj, quantidade, data, cliente_selecionado)
            elif movimento_tipo == "devolucao":
                sistema_estoque.devolucao_produto(produto_obj, quantidade, data, cliente_selecionado)
            elif movimento_tipo == "entrada":
                sistema_estoque.entrada_produto(produto_obj, quantidade, data, cliente_selecionado)
            
            # Atualiza o progresso
            progresso = int((i + 1) / len(produtos) * 100)
            atualizar_progresso(barra_progresso, label_percentual, progresso, tela)

        # Limpa a lista de produtos e atualiza a interface
        produtos.clear()
        atualizar_treeview(tree, produtos)
        atualizar_valor_total(label_preco_total, produtos)
        
        # Fechar a tela de carregamento
        tela.destroy()
        
        # Exibe mensagem de sucesso após o processamento dos produtos
        message = f"{movimento_tipo.capitalize()} realizada com sucesso."
        messagebox.showinfo("Atenção", message)
    
    # Inicia o processamento em uma thread separada
    threading.Thread(target=processar_movimento, daemon=True).start()

def adicionar_produto(modo_rapido, entry_codigo_barras, sistema_estoque, produtos, entry_quantidade, label_nome_produto, label_preco_total, tree, movimento_tipo):
    if modo_rapido:
        adicionar_produto_rapido(entry_codigo_barras, sistema_estoque, produtos, entry_quantidade, label_nome_produto, label_preco_total, tree)
    else:
        adicionar_produto_normal(entry_codigo_barras, entry_quantidade, sistema_estoque, produtos, label_nome_produto, tree, label_preco_total, movimento_tipo)

