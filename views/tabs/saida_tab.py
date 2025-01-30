import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import OptionMenu, StringVar
from assets.icons import carregar_imagens
from tkcalendar import Calendar
from tkinter import font as tkFont
# No arquivo saida_tab.py
from utils.selecao_data import selecionar_data
from utils.treeview_utils import criar_treeview
from controllers.movimentacao_estoque import  adicionar_produto, registrar_movimento, adicionar_produto_normal
from controllers.interface import agendar_verificacao_codigo_barras, mostrar_nome_produto, apagar_itens_selecionados


class SaidaTab(ctk.CTkFrame):
    def __init__(self, master=None, sistema_estoque=None, **kwargs):
        super().__init__(master, **kwargs)
        # Agora você pode armazenar 'sistema_estoque' como um atributo da classe
        self.sistema_estoque = sistema_estoque
        self.produtos_saida = []
        self.modo_rapido_saida = False 
        self.icons = carregar_imagens()
        # Configurando ícones de saída
        self.icon_photo_adicionar = self.icons["adicionar"]
        self.icon_photo_salvar = self.icons["salvar"]
        self.icon_photo_excluir = self.icons["delete"]
        # Adicionando frames
        self.frame_saida1 = ctk.CTkFrame(master=self, fg_color="#ffffff")
        self.frame_saida1.place(relwidth=0.78, relheight=0.75, relx=0.208, rely=0.11)
        self.frame_saida2 = ctk.CTkFrame(master=self, fg_color="#01497C")
        self.frame_saida2.place(relwidth=0.78, relheight=0.1, relx=0.208, rely=0.015)
        self.frame_saida3 = ctk.CTkFrame(master=self, fg_color="#c2061d")
        self.frame_saida3.place(relwidth=0.2, relheight=0.14, relx=0.8, rely=0.87)
        self.frame_saida4 = ctk.CTkFrame(master=self, fg_color="#ffffff")
        self.frame_saida4.place(relwidth=0.8, relheight=0.14, relx=0, rely=0.87)
        self.frame_saida5 = ctk.CTkFrame(master=self, fg_color="#F6F6F6")
        self.frame_saida5.place(relwidth=0.205, relheight=0.44, relx=0, rely=0.08)
        self.frame_saida6 = ctk.CTkFrame(master=self, fg_color="#01497C")
        self.frame_saida6.place(relwidth=0.205, relheight=0.05, relx=0, rely=0.04)
        self.frame_saida6_baixo = ctk.CTkFrame(master=self, fg_color="#c2061d")
        self.frame_saida6_baixo.place(relwidth=0.205, relheight=0.05, relx=0, rely=0)
        self.frame_saida7 = ctk.CTkFrame(master=self, fg_color="#F6F6F6")
        self.frame_saida7.place(relwidth=0.205, relheight=0.33, relx=0, rely=0.53)

        self.tree_saida = criar_treeview(self.frame_saida1)
        
        # Adicionando Labels
        self.label1 = ctk.CTkLabel(self.frame_saida6_baixo, text="Saídas de Estoque", text_color="#ffffff", font=("Arial bold", 22))
        self.label1.pack()
        self.label_codigo_barras_saida = ctk.CTkLabel(self.frame_saida5, text="Código de Barras:", text_color="black", font=("Arial bold", 14))
        self.label_codigo_barras_saida.place(relx=0, rely=0)
        self.label_quantidade_saida = ctk.CTkLabel(self.frame_saida5, text="Quantidade:", text_color="black", font=("Arial extra-bold", 14))
        self.label_quantidade_saida.place(relx=0.32, rely=0.17)
        self.label_nome_produto_saida = ctk.CTkLabel(self.frame_saida2, text="", text_color="#ffffff", font=("Arial extra-bold", 32))
        self.label_nome_produto_saida.place(relx=0.05, rely=0.2)
        self.label_preco_total_saida = ctk.CTkLabel(self.frame_saida3, text="Valor Total:\nR$0.00", text_color="#ffffff", font=("Arial extra-bold", 32))
        self.label_preco_total_saida.place(relx=0.2, rely=0.1)       
        # Entrada para código de barras
        self.entry_codigo_barras_saida = ctk.CTkEntry(self.frame_saida5, fg_color="#ffffff", border_color="black", border_width=1, text_color="black")
        self.entry_codigo_barras_saida.place(relwidth=0.95, relheight=0.09, relx=0.02, rely=0.08)
        self.entry_codigo_barras_saida.bind("<KeyRelease>", self.agendar_verificacao_codigo_barras_saida)
        self.agendamento_verificacao = None
        self.entry_quantidade_saida = ctk.CTkEntry(self.frame_saida5, fg_color="#ffffff", border_color="black", border_width=1, text_color="black")
        self.entry_quantidade_saida.place(relwidth=0.4, relheight=0.09, relx=0.27, rely=0.26)
        
        # Botões de ação
        self.btn_botao_adicionar_saida = ctk.CTkButton(self.frame_saida5, text="Adicionar", image=self.icon_photo_adicionar, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7", font=("Arial extra-bold", 16), command=lambda: adicionar_produto(self.modo_rapido_saida, self.entry_codigo_barras_saida,self.sistema_estoque,self.produtos_saida,self.entry_quantidade_saida,self.label_nome_produto_saida, self.label_preco_total_saida, self.tree_saida, "saida"))
        self.btn_botao_adicionar_saida.place(relwidth=0.95, relheight=0.13, relx=0.02, rely=0.65)
        self.btn_botao_salvar_saida = ctk.CTkButton(self.frame_saida4, text="", image=self.icon_photo_salvar, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7", command=lambda: registrar_movimento(self.label_data,self.group_var,self.produtos_saida,self.sistema_estoque,self.tree_saida, self.label_preco_total_saida, "saida"))
        self.btn_botao_salvar_saida.place(relwidth=0.08, relheight=0.8, relx=0.05, rely=0.06)
        self.btn_botao_excluir_saida = ctk.CTkButton(self.frame_saida4, text="", image=self.icon_photo_excluir, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#c2061d", command=lambda: apagar_itens_selecionados(self.produtos_saida, self.tree_saida, self.label_preco_total_saida))
        self.btn_botao_excluir_saida.place(relwidth=0.08, relheight=0.8, relx=0.3, rely=0.06)
        self.btn_modo_rapido_saida = ctk.CTkSwitch(self.frame_saida5, text="Modo Normal", onvalue="Ativado", offvalue="Desativado", bg_color="#F6F6F6", text_color="black", font=("Arial bold", 16), command=lambda: self.toggle_modo_rapido_saida(self.btn_modo_rapido_saida))
        self.btn_modo_rapido_saida.place(relx=0.2, rely=0.5)
        self.entry_quantidade_saida.bind("<Return>", lambda event: adicionar_produto(
            self.modo_rapido_saida, self.entry_codigo_barras_saida, self.sistema_estoque, self.produtos_saida, self.entry_quantidade_saida, self.label_nome_produto_saida, self.label_preco_total_saida, self.tree_saida, "saida"
        ))
        self.tree_saida.bind("<Delete>", lambda event: apagar_itens_selecionados(self.produtos_saida, self.tree_saida, self.label_preco_total_saida))

        # Calendário
        self.data_saida = Calendar(self.frame_saida7, selectmode="day", date_pattern="dd/mm/yyyy", background='#01497C', font=('Helvetica', 12), width=200, height=200)
        self.data_saida.place(relwidth=0.9, relheight=0.7, relx=0.05, rely=0.03)
        
        self.label_data = ctk.CTkLabel(self.frame_saida7, text="", text_color="black", font=("Arial bold", 16), bg_color="Lightgreen")
        self.label_data.place(relx=0.5, rely=0.81)
        

        # OptionMenu
        self.group_var = StringVar(self.frame_saida4)
        self.group_var.set("Selecione um evento")
        self.option_menu_frame = ctk.CTkFrame(self.frame_saida4, fg_color="#ffffff")
        self.option_menu_frame.place(relwidth=0.4, relheight=0.5, relx=0.55, rely=0.25)
        fonte = tkFont.Font(family="Arial", size=20)
        eventos = [""]
        self.combo_cliente_saida = OptionMenu(self.option_menu_frame, self.group_var, *eventos)
        self.combo_cliente_saida.config(width=60, font=fonte)
        self.combo_cliente_saida.pack(pady=10)
        self.btn_data_saida = ctk.CTkButton(self.frame_saida7, text="Selecionar data", command=lambda: selecionar_data(self.data_saida, self.label_data, self.group_var, self.combo_cliente_saida))
        self.btn_data_saida.place(relwidth=0.4, relheight=0.13, relx=0.05, rely=0.8)
        
    def agendar_verificacao_codigo_barras_saida(self, event):
        # Chama a função externa passando a instância da classe e o evento
        agendar_verificacao_codigo_barras(self, event, self.entry_codigo_barras_saida, self.modo_rapido_saida, self.sistema_estoque, self.label_nome_produto_saida, self.entry_quantidade_saida, self.produtos_saida, self.tree_saida, self.label_preco_total_saida, 'saida')
    def toggle_modo_rapido_saida(self, btn_modo_rapido_saida):
        # Alterar a variável de modo rápido diretamente no objeto (self.modo_rapido_saida)
        self.modo_rapido_saida = not self.modo_rapido_saida
        if self.modo_rapido_saida:
            btn_modo_rapido_saida.configure(text="Modo Rápido")
        else:
            btn_modo_rapido_saida.configure(text="Modo Normal")