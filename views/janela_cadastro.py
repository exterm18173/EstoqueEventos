import queue
import threading
import time
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

import webview
from controllers.produtos import Produto
from db.database import SistemaEstoque
from views.janela_pesquisa_cadastro import JanelaPesquisa
from utils.loading_screen import mostrar_tela_carregamento

class JanelaCadastro(ctk.CTkToplevel):
    def __init__(self, db_file):
        super().__init__()
        # Inicializa o SistemaEstoque com a conexão ao banco de dados
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)

        self.title("Cadastro de produtos")
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        largura_janela = largura_tela * 0.7  # 71.5% da largura da tela
        altura_janela = altura_tela * 0.6  # 85.7% da altura da tela
        x_pos = largura_tela * 0.005  # Posição horizontal (0% da largura da tela)
        y_pos = altura_tela * 0.27  # Posição vertical (14.5% da altura da tela)
        self.geometry(f"{int(largura_janela)}x{int(altura_janela)}+{int(x_pos)}+{int(y_pos)}")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.resizable(width=False, height=False)

        # Adicionando frames
        self.frame_cadastro1 = ctk.CTkFrame(self, fg_color="#008000")
        self.frame_cadastro1.place(relwidth=1, relheight=0.15, relx=0, rely=0)
        self.frame_cadastro2 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_cadastro2.place(relwidth=1, relheight=0.85, relx=0, rely=0.15)

        # Labels
        self.label_cadastro1 = ctk.CTkLabel(self.frame_cadastro1, text="CADASTRAR NOVOS PRODUTOS", font=("Arial", 38), text_color="#FFFFFF")
        self.label_cadastro1.pack(pady=20)
        self.label_cadastro_nome = ctk.CTkLabel(self.frame_cadastro2, text="Nome:", font=("Arial", 18), text_color="black")
        self.label_cadastro_nome.place(relx=0.05, rely=0.1)
        self.label_cadastro_codigo_barras = ctk.CTkLabel(self.frame_cadastro2, text="Codigo de Barras:", font=("Arial", 18), text_color="black")
        self.label_cadastro_codigo_barras.place(relx=0.05, rely=0.27)
        self.label_cadastro_preco = ctk.CTkLabel(self.frame_cadastro2, text="Preço:", font=("Arial", 18), text_color="black")
        self.label_cadastro_preco.place(relx=0.05, rely=0.44)
        self.label_cadastro_quantidade = ctk.CTkLabel(self.frame_cadastro2, text="Quantidade:", font=("Arial", 18), text_color="black")
        self.label_cadastro_quantidade.place(relx=0.05, rely=0.61)
        self.label_cadastro_grupo = ctk.CTkLabel(self.frame_cadastro2, text="Grupo:", font=("Arial", 18), text_color="black")
        self.label_cadastro_grupo.place(relx=0.5, rely=0.32)
        self.label_cadastro_sub_grupo = ctk.CTkLabel(self.frame_cadastro2, text="Sub-Grupo:", font=("Arial", 18), text_color="black")
        self.label_cadastro_sub_grupo.place(relx=0.5, rely=0.52)

        # Botões
        self.btn_salvar_cadastro = ctk.CTkButton(self.frame_cadastro2, text="Salvar", width=200, height=50, font=("Arial", 20), command=self.adicionar_produto, fg_color="#5D9C59", hover_color="#4C8C48")
        self.btn_salvar_cadastro.place(relx=0.75, rely=0.85)
        self.btn_gerar_codigo = ctk.CTkButton(self.frame_cadastro2, text="Gerar Código", width=200, height=50, font=("Arial", 20), command=self.gerar_codigo_barras, fg_color="#FF9E2A", hover_color="#F5821F")
        self.btn_gerar_codigo.place(relx=0.5, rely=0.85)
        self.btn_gerar_codigo_kg = ctk.CTkButton(self.frame_cadastro2, text="Gerar Código (kg)", width=200, height=50, font=("Arial", 20), command=self.gerar_codigo_barras_kg, fg_color="#FF9E2A", hover_color="#F5821F")
        self.btn_gerar_codigo_kg.place(relx=0.1, rely=0.85)

        # Entradas de dados
        self.entry_nome = ctk.CTkEntry(self.frame_cadastro2, width=400, height=40, font=("Arial", 20), bg_color="#FFFFFF", fg_color="#FFFFFF", text_color="black")
        self.entry_nome.place(relx=0.05, rely=0.17)
        self.entry_codigo_barras = ctk.CTkEntry(self.frame_cadastro2, width=250, height=40, font=("Arial", 20), bg_color="#FFFFFF", fg_color="#FFFFFF", text_color="black")
        self.entry_codigo_barras.place(relx=0.05, rely=0.34)
        self.entry_preco = ctk.CTkEntry(self.frame_cadastro2, width=150, height=40, font=("Arial", 20), bg_color="#FFFFFF", fg_color="#FFFFFF", text_color="black")
        self.entry_preco.place(relx=0.05, rely=0.51)
        self.entry_quantidade = ctk.CTkEntry(self.frame_cadastro2, width=150, height=40, font=("Arial", 20), bg_color="#FFFFFF", fg_color="#FFFFFF", text_color="black")
        self.entry_quantidade.place(relx=0.05, rely=0.68)

        # Botões de seleção de grupo e subgrupo
        self.btn_grupo = ctk.CTkButton(self.frame_cadastro2, text="Selecionar Grupo", width=200, height=40, font=("Arial", 16), command=self.abrir_janela_grupo)
        self.btn_grupo.place(relx=0.45, rely=0.4)

        self.btn_subgrupo = ctk.CTkButton(self.frame_cadastro2, text="Selecionar Sub-Grupo", width=200, height=40, font=("Arial", 16), command=self.abrir_janela_subgrupo)
        self.btn_subgrupo.place(relx=0.45, rely=0.6)

    def abrir_janela_grupo(self):
        """Exibe a tela de carregamento enquanto carrega os grupos."""
        tela_carregamento, barra_progresso, label_percentual = mostrar_tela_carregamento(self)
        
        # Executa a função de obtenção dos grupos em uma thread separada
        def carregar_grupos():
            grupos = self.sistema_estoque.obter_grupos()  # Obtém os grupos
            for i in range(1, 101):
                barra_progresso.set(i / 100)  # Atualiza a barra de progresso
                label_percentual.configure(text=f"{i}%")  # Atualiza o texto da porcentagem
            tela_carregamento.destroy()  # Fecha a tela de carregamento
            self.abrir_pesquisa_grupo_interface(grupos)  # Abre a tela de pesquisa com os grupos

        # Cria e inicia a thread
        thread = threading.Thread(target=carregar_grupos)
        thread.start()

    def abrir_pesquisa_grupo_interface(self, itens):
        """Abre a interface de pesquisa de grupo com os grupos já fornecidos"""
        janela_pesquisa = JanelaPesquisa(self, "grupo", itens)
        janela_pesquisa.transient(self)  # Torna a janela filha e não bloqueia interação
        self.wait_window(janela_pesquisa)

    def abrir_janela_subgrupo(self):
        """Exibe a tela de carregamento enquanto carrega os subgrupos."""
        tela_carregamento, barra_progresso, label_percentual = mostrar_tela_carregamento(self)
        
        # Executa a função de obtenção dos subgrupos em uma thread separada
        def carregar_subgrupos():
            subgrupos = self.sistema_estoque.obter_subgrupos()  # Obtém os subgrupos
            for i in range(1, 101):
                barra_progresso.set(i / 100)  # Atualiza a barra de progresso
                label_percentual.configure(text=f"{i}%")  # Atualiza o texto da porcentagem
            tela_carregamento.destroy()  # Fecha a tela de carregamento
            self.abrir_pesquisa_subgrupo_interface(subgrupos)  # Abre a tela de pesquisa com os subgrupos

        # Cria e inicia a thread
        thread = threading.Thread(target=carregar_subgrupos)
        thread.start()

    def abrir_pesquisa_subgrupo_interface(self, itens):
        """Abre a interface de pesquisa de subgrupo com os subgrupos já fornecidos"""
        janela_pesquisa = JanelaPesquisa(self, "subgrupo", itens)
        janela_pesquisa.transient(self)  # Torna a janela filha e não bloqueia interação

        self.wait_window(janela_pesquisa)

    def fechar_janela(self):
        self.destroy()
    def adicionar_produto(self):
        # Recupera os dados dos campos
        nome = self.entry_nome.get()
        codigo_barras = self.entry_codigo_barras.get()
        preco_unitario_str = self.entry_preco.get()
        quantidade_estoque_str = self.entry_quantidade.get()
        grupo = self.btn_grupo.cget("text")  # Pega o texto do botão, que é o grupo selecionado
        sub_grupo = self.btn_subgrupo.cget("text")  # Pega o texto do botão, que é o subgrupo selecionado

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not nome or not codigo_barras or not preco_unitario_str or not quantidade_estoque_str or not grupo or not sub_grupo:
            messagebox.showinfo("Atenção", "Todos os campos devem ser preenchidos. Produto não adicionado.", parent=self)
            return

        try:
            preco_unitario = float(preco_unitario_str)  # Converte o preço para float
            quantidade_estoque = float(quantidade_estoque_str)  # Converte a quantidade para float
        except ValueError:
            # Caso haja erro na conversão de preço ou quantidade
            messagebox.showinfo("Atenção", "Preço ou Quantidade inválidos. Informe valores numéricos.", parent=self)
            return

        # Cria o objeto Produto com os dados coletados
        id = None  # O ID é sempre None no momento da criação
        produto = Produto(id, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo)

        # Adiciona o produto ao sistema de estoque
        self.sistema_estoque.adicionar_produto(produto)

        # Limpa os campos após adicionar o produto
        self.entry_nome.delete(0, tk.END)
        self.entry_codigo_barras.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.btn_grupo.configure(text="Selecionar Grupo")  # Reseta o botão de grupo
        self.btn_subgrupo.configure(text="Selecionar Sub-Grupo")  # Reseta o botão de subgrupo


    def gerar_codigo_barras(self):
        self.sistema_estoque.gerar_codigo_barras(self.entry_codigo_barras)

    def gerar_codigo_barras_kg(self):
        self.sistema_estoque.gerar_codigo_barras_kg(self.entry_codigo_barras)

