import sqlite3
import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import OptionMenu, StringVar, ttk
from assets.icons import carregar_imagens
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import font as tkFont
# No arquivo saida_tab.py
from controllers.produtos import Produto
from utils.selecao_data import selecionar_data
from utils.treeview_utils import criar_treeview
from controllers.movimentacao_estoque import  adicionar_produto, registrar_movimento, adicionar_produto_normal
from controllers.interface import agendar_verificacao_codigo_barras, mostrar_nome_produto, apagar_itens_selecionados
from views.janela_code_bar import JanelaCodeBar

class DevolucaoTab(ctk.CTkFrame):
    def __init__(self, master=None, sistema_estoque=None, **kwargs):
        super().__init__(master, **kwargs)
        self.sistema_estoque = sistema_estoque
        self.produtos_devolucao = []
        self.modo_rapido_devolucao = False 
        self.icons = carregar_imagens()
        # Configurando ícones de saída
        self.icon_photo_adicionar = self.icons["adicionar"]
        self.icon_photo_salvar = self.icons["salvar"]
        self.icon_photo_excluir = self.icons["delete"]
        self.icon_gerar_barcode = self.icons["gerar_barcode"]
        #Aba Devolução
    #adicionando frames da paleta de cores
        self.frame_devolucao1 = ctk.CTkFrame(master= self, fg_color="#ffffff")
        self.frame_devolucao1.place(relwidth=0.78, relheight=0.75, relx= 0.208, rely= 0.11)
        self.frame_devolucao2 = ctk.CTkFrame(master= self, fg_color="#01497C")
        self.frame_devolucao2.place(relwidth=0.78, relheight=0.1, relx= 0.208, rely= 0.015)
        self.frame_devolucao3 = ctk.CTkFrame(master= self, fg_color="#2D3137")
        self.frame_devolucao3.place(relwidth=0.2, relheight=0.14, relx= 0.8, rely= 0.87)
        self.frame_devolucao4 = ctk.CTkFrame(master= self, fg_color="#ffffff")
        self.frame_devolucao4.place(relwidth=0.8, relheight=0.14, relx= 0, rely= 0.87)
        self.frame_devolucao5 = ctk.CTkFrame(master= self, fg_color="#F6F6F6")
        self.frame_devolucao5.place(relwidth=0.205, relheight=0.44, relx= 0, rely= 0.08)
        self.frame_devolucao6 = ctk.CTkFrame(master= self, fg_color="#01497C")
        self.frame_devolucao6.place(relwidth=0.205, relheight=0.05, relx= 0, rely= 0.04)
        self.frame_devolucao6 = ctk.CTkFrame(master= self, fg_color="#2D3137")
        self.frame_devolucao6.place(relwidth=0.205, relheight=0.05, relx= 0, rely= 0)
        self.frame_devolucao7 = ctk.CTkFrame(master= self, fg_color="#F6F6F6")
        self.frame_devolucao7.place(relwidth=0.205, relheight=0.33, relx= 0, rely= 0.53)        
        #Adicionando Labels saida
        self.label_devolucao1 = ctk.CTkLabel(self.frame_devolucao6, text="Devolução de Produtos", text_color="#ffffff", font=("Arial bold",22))
        self.label_devolucao1.pack()
        self.label_codigo_barras_devolucao = ctk.CTkLabel(self.frame_devolucao5, text="Codigo de Barras:", text_color="black",font=("Arial bold",14))
        self.label_codigo_barras_devolucao.place(relx=0, rely=0)
        self.label_quantidade_devolucao = ctk.CTkLabel(self.frame_devolucao5, text="Quantidade:", text_color="black",font=("Arial extra-bold",14))
        self.label_quantidade_devolucao.place(relx=0.32, rely=0.17)
        self.label_nome_produto_devolucao = ctk.CTkLabel(self.frame_devolucao2, text="", text_color="#ffffff",font=("Arial extra-bold", 32))
        self.label_nome_produto_devolucao.place(relx=0.05, rely=0.2)
        self.label_preco_total_devolucao = ctk.CTkLabel(self.frame_devolucao3, text="Valor Total:\nR$0.00", text_color="#ffffff", font=("Arial extra-bold", 32))
        self.label_preco_total_devolucao.place(relx=0.2, rely=0.1)       
        #adicionado entry na aba saida
        self.entry_codigo_barras_devolucao = ctk.CTkEntry(self.frame_devolucao5, fg_color="#ffffff", border_color="black", border_width=1, text_color="black")
        self.entry_codigo_barras_devolucao.place(relwidth=0.95, relheight=0.09, relx=0.02,rely=0.08)
        self.entry_codigo_barras_devolucao.bind("<KeyRelease>", self.agendar_verificacao_codigo_barras_devolucao)
        # Variável para armazenar o identificador do agendamento
        self.agendamento_verificacao = None
        self.entry_quantidade_devolucao = ctk.CTkEntry(self.frame_devolucao5, fg_color="#ffffff", border_color="black", border_width=1, text_color="black")
        self.entry_quantidade_devolucao.place(relwidth=0.4, relheight=0.09, relx=0.27,rely=0.26)
        #adicionando botão na aba saida
        self.btn_botao_adicionar_devolucao = ctk.CTkButton(self.frame_devolucao5, text="Adicionar", image=self.icon_photo_adicionar, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7", font=("Arial extra-bold",16), command=lambda: adicionar_produto(self.modo_rapido_devolucao, self.entry_codigo_barras_devolucao,self.sistema_estoque,self.produtos_devolucao,self.entry_quantidade_devolucao,self.label_nome_produto_devolucao, self.label_preco_total_devolucao, self.tree_devolucao, "devolucao"))
        self.btn_botao_adicionar_devolucao.place(relwidth=0.95, relheight=0.13, relx=0.02, rely=0.65)



        self.btn_botao_salvar_devolucao = ctk.CTkButton(self.frame_devolucao4, text="", image=self.icon_photo_salvar, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7",command=lambda: registrar_movimento(self.label_data_devolucao,self.group_var_dev,self.produtos_devolucao,self.sistema_estoque,self.tree_devolucao, self.label_preco_total_devolucao, "devolucao"))
        self.btn_botao_salvar_devolucao.place(relwidth=0.08, relheight=0.8, relx=0.03, rely=0.06)



        self.btn_botao_excluir_devolucao = ctk.CTkButton(self.frame_devolucao4, text="", image=self.icon_photo_excluir, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#c2061d", command=lambda: apagar_itens_selecionados(self.produtos_devolucao, self.tree_devolucao, self.label_preco_total_devolucao))
        self.btn_botao_excluir_devolucao.place(relwidth=0.08, relheight=0.8, relx=0.15, rely=0.06)



        self.btn_botao_gerar_barcode = ctk.CTkButton(self.frame_devolucao4, text="", image=self.icon_gerar_barcode, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7", command=lambda: abrir_janela('gerar_barcode', sistema_estoque, self.tree_devolucao, self.produtos_devolucao, self.label_preco_total_devolucao))
        self.btn_botao_gerar_barcode.place(relwidth=0.1, relheight=0.7, relx=0.3, rely=0.06)



        self.btn_modo_rapido_devolucao = ctk.CTkSwitch(self.frame_devolucao5, text="Modo Normal",  onvalue="Ativado", offvalue="Desativado",bg_color="#F6F6F6", text_color="black", font=("Arial bold", 16), command=lambda: self.toggle_modo_rapido_devolucao(self.btn_modo_rapido_devolucao))
        self.btn_modo_rapido_devolucao.place(relx=0.2, rely=0.5)       
        #self.entry_codigo_barras_saida.bind("<KeyRelease>", self.mostrar_nome_produto_saida)
        self.entry_quantidade_devolucao.bind("<Return>", lambda event: adicionar_produto_normal(
            self.entry_codigo_barras_devolucao, 
            self.entry_quantidade_devolucao, 
            self.sistema_estoque, 
            self.produtos_devolucao, 
            self.label_nome_produto_devolucao, 
            self.tree_devolucao,  # Adicionando o parâmetro tree_saida
            self.label_preco_total_devolucao,  # Adicionando o parâmetro label_preco_total_saida
            "devolucao"
        ))
        #adicionando calendario de seleção
        
        
        self.data_devolucao = Calendar(self.frame_devolucao7, selectmode="day", date_pattern="dd/mm/yyyy", background='#01497C', font=('Helvetica', 12), width=200, height=200)
        self.data_devolucao.place(relwidth=0.9, relheight=0.7, relx=0.05,rely=0.03)
        self.btn_data_devolucao = ctk.CTkButton(self.frame_devolucao7, text="Selecionar data", command=lambda: selecionar_data(self.data_devolucao, self.label_data_devolucao, self.group_var_dev, self.combo_cliente_dev))
        self.btn_data_devolucao.place(relwidth=0.4, relheight=0.13, relx=0.05,rely=0.8)
        self.label_data_devolucao = ctk.CTkLabel(self.frame_devolucao7, text="", text_color="black", font=("Arial bold", 16), bg_color="Lightgreen")
        self.label_data_devolucao.place(relx=0.5, rely=0.81) 
        #treeview saidas
        # Style
        
        # Variável para o OptionMenu
        self.group_var_dev = StringVar(self.frame_devolucao4)
        self.group_var_dev.set("Selecione um evento")  # Valor padrão

        # Frame para o OptionMenu para controle de tamanho
        self.option_menu_frame_dev = ctk.CTkFrame(self.frame_devolucao4, fg_color="#ffffff")
        self.option_menu_frame_dev.place(relwidth=0.4, relheight=0.5, relx= 0.55, rely= 0.25)
        fonte = tkFont.Font(family="Arial", size=20)
        # OptionMenu para seleção de eventos
        self.combo_cliente_dev = OptionMenu(self.option_menu_frame_dev, self.group_var_dev, 
                                                   self.group_var_dev.get(), "Selecione um evento")
        self.combo_cliente_dev.config(width=60, font=fonte)  # Ajuste a largura do OptionMenu
        self.combo_cliente_dev.pack(pady=10)  # Adiciona um espaçamento vertical
        self.tree_devolucao = criar_treeview(self.frame_devolucao1) 
        self.tree_devolucao.bind("<Delete>", lambda event: apagar_itens_selecionados(self.produtos_devolucao, self.tree_devolucao, self.label_preco_total_devolucao))
        

    def agendar_verificacao_codigo_barras_devolucao(self, event):
        # Chama a função externa passando a instância da classe e o evento
        agendar_verificacao_codigo_barras(self, event, self.entry_codigo_barras_devolucao, self.modo_rapido_devolucao, self.sistema_estoque, self.label_nome_produto_devolucao, self.entry_quantidade_devolucao, self.produtos_devolucao, self.tree_devolucao, self.label_preco_total_devolucao, 'devolucao')
    def toggle_modo_rapido_devolucao(self, btn_modo_rapido_devolucao):
        # Alterar a variável de modo rápido diretamente no objeto (self.modo_rapido_saida)
        self.modo_rapido_devolucao = not self.modo_rapido_devolucao
        if self.modo_rapido_devolucao:
            btn_modo_rapido_devolucao.configure(text="Modo Rápido")
        else:
            btn_modo_rapido_devolucao.configure(text="Modo Normal")


    # Dicionário de janelas abertas
janelas = {}
def abrir_janela(tipo, sistema_estoque, tree_devolucao, produtos_devolucao, label_preco_total_devolucao ):
    # Verifica se já existe uma janela do tipo solicitado aberta
    if tipo in janelas and janelas[tipo].winfo_exists():
        # Se a janela já está aberta, traz ela para frente
        janelas[tipo].deiconify()
        janelas[tipo].lift()
        janelas[tipo].focus()
        janelas[tipo].grab_set()
        
    else:
        # Se não existe, cria uma nova janela
        janela = None
        if tipo == 'gerar_barcode':
            janela = JanelaCodeBar("db/db_file.db",tree_devolucao, produtos_devolucao, label_preco_total_devolucao )
        if janela:
            # Armazena a janela no dicionário
            janelas[tipo] = janela
            janela.protocol("WM_DELETE_WINDOW", lambda: fechar_janela(tipo))
            janela.mainloop()

def fechar_janela(tipo):
    # Remove a janela do dicionário ao fechar
    if tipo in janelas:
        janelas[tipo].destroy()
        del janelas[tipo]