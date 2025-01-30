from controllers.produtos import Produto
import tkinter as tk

def adicionar_produto(self):
        nome = self.entry_nome.get()
        codigo_barras = self.entry_codigo_barras.get()
        preco_unitario = float(self.entry_preco.get())
        quantidade_estoque = float(self.entry_quantidade.get())
        grupo = self.btn_grupo.cget("text")  # Pega o texto do botão, que é o grupo selecionado
        sub_grupo = self.btn_subgrupo.cget("text")  # Pega o texto do botão, que é o subgrupo selecionado

        produto = Produto(nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo)
        self.sistema_estoque.adicionar_produto(produto)

        # Limpar os campos após adicionar
        self.entry_nome.delete(0, tk.END)
        self.entry_codigo_barras.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.btn_grupo.configure(text="Selecionar Grupo")  # Reseta o botão
        self.btn_subgrupo.configure(text="Selecionar Sub-Grupo")  # Reseta o botão

