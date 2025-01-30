import sqlite3
from tkinter import messagebox, ttk
import tkinter as tk
from utils.utils import validar_quantidade


# Função para agendar a verificação de código de barras (para saída ou devolução)
def agendar_verificacao_codigo_barras(tab_instance, event, entry_codigo_barras, modo_rapido, sistema_estoque, label_nome_produto, entry_quantidade, produtos, tree, label_preco_total, movimento_tipo):
    if tab_instance.agendamento_verificacao is not None:
        tab_instance.after_cancel(tab_instance.agendamento_verificacao)

    tab_instance.agendamento_verificacao = tab_instance.after(100, 
        lambda: mostrar_nome_produto(entry_codigo_barras=entry_codigo_barras, modo_rapido=modo_rapido, sistema_estoque=sistema_estoque, label_nome_produto=label_nome_produto, entry_quantidade=entry_quantidade, produtos=produtos, tree=tree, label_preco_total=label_preco_total, movimento_tipo=movimento_tipo))

def mostrar_nome_produto(event=None, entry_codigo_barras=None, modo_rapido=None, sistema_estoque=None, 
                          label_nome_produto=None, entry_quantidade=None, produtos=None, label_preco_total=None,
                          movimento_tipo=None, tree=None):
    codigo_barras = entry_codigo_barras.get().strip()
    if not codigo_barras:
        return
    if len(codigo_barras) < 4:
        label_nome_produto.configure(text="Código de barras inválido")
        return
    try:
        if modo_rapido and not codigo_barras.startswith("2") and 4 <= len(codigo_barras) <= 14:
            adicionar_produto_rapido(entry_codigo_barras, entry_quantidade, sistema_estoque, produtos, label_nome_produto, tree, label_preco_total, movimento_tipo)
            return
        # Consulta padrão de código de barras
        if not codigo_barras.startswith("2") and 4 <= len(codigo_barras) <= 14:
            produto = sistema_estoque.consultar_produto(codigo_barras)
            atualizar_interface_produto(produto, label_nome_produto, entry_quantidade)
            if produto:
                entry_quantidade.unbind("<Return>")
                entry_quantidade.bind("<Return>", lambda event: adicionar_produto_normal(entry_codigo_barras, entry_quantidade, sistema_estoque, produtos, label_nome_produto, tree, label_preco_total, movimento_tipo))  
        elif len(codigo_barras) == 20:
            codigo_item = codigo_barras[:7]
            peso = round(float(codigo_barras[7:]) / 100000000000, 3)
            produto = sistema_estoque.consultar_produto(codigo_item)
            atualizar_interface_produto(produto, label_nome_produto, entry_quantidade, peso)

        elif len(codigo_barras) == 13 and codigo_barras.startswith("2"):
            codigo_item = codigo_barras[:7]
            
            produto = sistema_estoque.consultar_produto(codigo_item)
            atualizar_interface_produto(produto, label_nome_produto, entry_quantidade)

        else:
            label_nome_produto.configure(text="Código de barras inválido")
    
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar nome do produto: {e}")
def atualizar_valor_total(label_preco_total, produtos):
    total = sum(item[4] for item in produtos)
    label_preco_total.configure(text=f"Valor Total: \nR${total:.2f}")
# Função para atualizar o Treeview com os produtos
def atualizar_treeview(tree, produtos):
    if isinstance(tree, ttk.Treeview):  # Verifica se 'tree' é realmente uma Treeview
        for item_id in tree.get_children():
            tree.delete(item_id)

        for i, produto in enumerate(produtos, start=1):
            tree.insert("", "end", text=str(i), values=produto)
    else:
        messagebox.showerror("Erro", "O widget fornecido não é uma Treeview válida.")
def atualizar_interface_produto(produto, label_nome_produto, entry_quantidade, peso=None):
    """Atualiza a interface com o nome do produto e a quantidade (ou peso)."""
    if produto:
        label_nome_produto.configure(text=produto[0])
        if peso:
            entry_quantidade.delete(0, tk.END)
            entry_quantidade.insert(0, peso)
        entry_quantidade.focus_set()
    else:
        label_nome_produto.configure(text="Produto não encontrado")
# Métodos de produto como buscar preço, nome, etc.
def adicionar_produto_normal(entry_codigo_barras, entry_quantidade, sistema_estoque, produtos, label_nome_produto, tree, label_preco_total, movimento_tipo):
    """Adiciona um produto no modo normal (não rápido) ao sistema de estoque e atualiza a interface."""
    codigo_barras = entry_codigo_barras.get().strip()
    quantidade = entry_quantidade.get().strip()

    # Verificação do código de barras
    if len(codigo_barras) == 20:
        codigo_barras = codigo_barras[:7]  # Pega apenas os 7 primeiros dígitos
    elif len(codigo_barras) == 13 and codigo_barras.startswith('2'):
        codigo_barras = codigo_barras[:7]  # Pega apenas os 7 primeiros dígitos

    # Valida a quantidade
    quantidade_valida = validar_quantidade(quantidade)
    if quantidade_valida is None:
        messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
        return

    # Consulta o produto no banco de dados
    produto = sistema_estoque.consultar_produto(codigo_barras)

    if produto:
        nome_produto, preco_unitario, grupo, sub_grupo = produto
        valor_total = quantidade_valida * preco_unitario

        # Adiciona o produto à lista de produtos
        produtos.append((nome_produto, codigo_barras, preco_unitario, quantidade_valida, valor_total, grupo, sub_grupo))

        # Atualiza a interface
        atualizar_treeview(tree, produtos)
        atualizar_valor_total(label_preco_total, produtos)

        # Limpa os campos de entrada e coloca o foco novamente no código de barras
        entry_codigo_barras.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        label_nome_produto.configure(text="")
        entry_codigo_barras.focus_set()
    else:
        messagebox.showinfo("Atenção", "Produto não encontrado.")


import tkinter.messagebox as messagebox

def adicionar_produto_code_bar(codigo_barras, peso, sistema_estoque, produtos, tree, total):
    # Consulta o produto no banco de dados
    produto = sistema_estoque.consultar_produto(codigo_barras)

    if produto:
        nome_produto, preco_unitario, grupo, sub_grupo = produto

        # Verificar se o peso e o preço unitário são valores válidos
        try:
            peso = float(peso)  # Garantir que o peso é numérico
            preco_unitario = float(preco_unitario)  # Garantir que o preço unitário é numérico
            if peso <= 0 or preco_unitario <= 0:
                raise ValueError("Peso e preço unitário devem ser valores positivos.")
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao processar os dados: {str(e)}")
            return

        # Calcular o valor total do produto
        valor_total = peso * preco_unitario

        # Adicionar o produto à lista de produtos
        produtos.append((nome_produto, codigo_barras, preco_unitario, peso, valor_total, grupo, sub_grupo))

        # Atualiza a interface
        atualizar_treeview(tree, produtos)
        atualizar_valor_total(total, produtos)
        

    else:
        # Caso o produto não seja encontrado no banco de dados
        messagebox.showinfo("Atenção", "Produto não encontrado.")









def pesquisar_item(self, entry_buscar, treeview, sistema_estoque):
    nome = entry_buscar.get().strip()
    treeview.delete(*treeview.get_children())  # Limpar resultados anteriores

    try:
        sistema_estoque.c.execute("SELECT id, nome, codigo_barras, preco_unitario FROM produtos WHERE nome LIKE ? AND LENGTH(codigo_barras) = 7", ('%' + nome + '%',))
        produtos = sistema_estoque.c.fetchall()

        for produto in produtos:
            treeview.insert("", "end", values=produto)
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar item no estoque: {e}")
def adicionar(self, tree, sistema_estoque, produtos, total, treeview, entry_peso):
    selected_item = treeview.selection()
    
    # Verificar se há um item selecionado
    if not selected_item:
        print("Nenhum produto selecionado na Treeview.")
        return

    # Obter o código de barras do item selecionado
    codigo_barras = treeview.item(selected_item[0], "values")[2]
    print(f"Código de barras selecionado: {codigo_barras}")
    
    # Obter o peso da entrada
    peso = entry_peso.get()
    
    # Verificar se o peso foi inserido corretamente
    if not peso:
        print("Peso não informado. Por favor, insira o peso.")
        return
    
    try:
        peso = float(peso)  # Verificar se o peso é um número válido
    except ValueError:
        print("Peso inválido. Por favor, insira um valor numérico válido para o peso.")
        return

    # Chamar a função para adicionar o produto ao sistema
    adicionar_produto_code_bar(codigo_barras, peso, sistema_estoque, produtos, tree, total)
    print(f"Produto {codigo_barras} adicionado com peso {peso} kg.")









# Função para adicionar produto no modo rápido
def adicionar_produto_rapido(entry_codigo_barras, entry_quantidade, sistema_estoque, produtos, label_nome_produto, tree, label_preco_total, movimento_tipo):
    codigo_barras = entry_codigo_barras.get().strip()
    quantidade_rapida = 1  # Definindo quantidade como 1 no modo rápido

    try:
        sistema_estoque.c.execute("SELECT nome, quantidade_estoque, preco_unitario, grupo, sub_grupo FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
        produto = sistema_estoque.c.fetchone()

        if produto:
            nome_produto = produto[0]
            quantidade_estoque = produto[1]
            preco_produto = float(produto[2])
            grupo = produto[3]
            sub_grupo = produto[4]

            if quantidade_rapida <= quantidade_estoque:
                valor_total = preco_produto * quantidade_rapida
                produtos.append((nome_produto, codigo_barras, preco_produto, quantidade_rapida, valor_total, grupo, sub_grupo))
                atualizar_treeview(tree, produtos)
                atualizar_valor_total(label_preco_total, produtos)
                entry_codigo_barras.delete(0, tk.END)
                entry_quantidade.delete(0, tk.END)
                label_nome_produto.configure(text="")
                entry_codigo_barras.focus_set()
            else:
                messagebox.showinfo("Atenção", f"Quantidade insuficiente em estoque para o produto '{nome_produto}'.")
        else:
            messagebox.showinfo("Atenção", "Produto não encontrado.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")    
def apagar_itens_selecionados(produtos, tree, label_preco_total):
    itens_selecionados = tree.selection()
    if not itens_selecionados:
        return messagebox.showerror("Erro", f"Nenhum item selecionado!")
    indices = sorted([int(tree.item(item_id, "text")) - 1 for item_id in itens_selecionados], reverse=True)
    for index in indices:
        if 0 <= index < len(produtos):  # Verifica se o índice está dentro do intervalo válido
            del produtos[index]
    for item_id in itens_selecionados:
        tree.delete(item_id)
    atualizar_valor_total(label_preco_total, produtos)
    atualizar_treeview(tree, produtos)
