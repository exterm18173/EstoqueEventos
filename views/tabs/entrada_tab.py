import customtkinter as ctk
import tkinter as tk
from tkinter import StringVar
from tkcalendar import Calendar
from PIL import Image
from assets.icons import carregar_imagens
from utils.selecao_data import selecionar_data_entrada
from utils.treeview_utils import criar_treeview
from controllers.movimentacao_estoque import  adicionar_produto, registrar_movimento, adicionar_produto_normal
from controllers.interface import agendar_verificacao_codigo_barras, mostrar_nome_produto, apagar_itens_selecionados
from views.janela_code_bar import JanelaCodeBar


class EntradaTab(ctk.CTkFrame):
    def __init__(self, master=None, sistema_estoque = None, **kwargs):
        super().__init__(master, **kwargs)
        self.sistema_estoque = sistema_estoque
        self.modo_rapido_entrada = False
        self.produtos_entrada = [] 
        #Aba Entrada
        self.icons = carregar_imagens()
        # Configurando ícones de saída
        self.icon_photo_adicionar = self.icons["adicionar"]
        self.icon_photo_salvar = self.icons["salvar"]
        self.icon_photo_excluir = self.icons["delete"]
        self.icon_gerar_barcode = self.icons["gerar_barcode"]
    #adicionando frames da paleta de cores

        self.frame_entrada1 = ctk.CTkFrame(master= self, fg_color="#ffffff")
        self.frame_entrada1.place(relwidth=0.78, relheight=0.75, relx= 0.208, rely= 0.11)
        self.frame_entrada2 = ctk.CTkFrame(master= self, fg_color="#01497C")
        self.frame_entrada2.place(relwidth=0.78, relheight=0.1, relx= 0.208, rely= 0.015)
        self.frame_entrada3 = ctk.CTkFrame(master= self, fg_color="#2D3137")
        self.frame_entrada3.place(relwidth=0.2, relheight=0.14, relx= 0.8, rely= 0.87)
        self.frame_entrada4 = ctk.CTkFrame(master= self, fg_color="#ffffff")
        self.frame_entrada4.place(relwidth=0.8, relheight=0.14, relx= 0, rely= 0.87)
        self.frame_entrada5 = ctk.CTkFrame(master= self, fg_color="#F6F6F6")
        self.frame_entrada5.place(relwidth=0.205, relheight=0.44, relx= 0, rely= 0.08)
        self.frame_entrada6 = ctk.CTkFrame(master= self, fg_color="#01497C")
        self.frame_entrada6.place(relwidth=0.205, relheight=0.05, relx= 0, rely= 0.04)
        self.frame_entrada6 = ctk.CTkFrame(master= self, fg_color="#87BA5A")
        self.frame_entrada6.place(relwidth=0.205, relheight=0.05, relx= 0, rely= 0)
        self.frame_entrada7 = ctk.CTkFrame(master= self, fg_color="#F6F6F6")
        self.frame_entrada7.place(relwidth=0.205, relheight=0.33, relx= 0, rely= 0.53)        
        #Adicionando Labels saida
        self.label_entrada1 = ctk.CTkLabel(self.frame_entrada6, text="Entradas de Estoque", text_color="#ffffff", font=("Arial bold",22))
        self.label_entrada1.pack()
        self.label_codigo_barras_entrada = ctk.CTkLabel(self.frame_entrada5, text="Codigo de Barras:", text_color="black",font=("Arial bold",14))
        self.label_codigo_barras_entrada.place(relx=0, rely=0)
        self.label_quantidade_entrada = ctk.CTkLabel(self.frame_entrada5, text="Quantidade:", text_color="black",font=("Arial extra-bold",14))
        self.label_quantidade_entrada.place(relx=0.32, rely=0.17)
        self.label_nome_produto_entrada = ctk.CTkLabel(self.frame_entrada2, text="", text_color="#ffffff",font=("Arial extra-bold", 32))
        self.label_nome_produto_entrada.place(relx=0.05, rely=0.2)
        self.label_preco_total_entrada = ctk.CTkLabel(self.frame_entrada3, text="Valor Total:\nR$0.00", text_color="#ffffff", font=("Arial extra-bold", 32))
        self.label_preco_total_entrada.place(relx=0.2, rely=0.1)       
        #adicionado entry na aba saida
        self.entry_codigo_barras_entrada = ctk.CTkEntry(self.frame_entrada5, fg_color="#ffffff", border_color="black", border_width=1, text_color="black")
        self.entry_codigo_barras_entrada.place(relwidth=0.95, relheight=0.09, relx=0.02,rely=0.08)
        self.entry_codigo_barras_entrada.bind("<KeyRelease>", self.agendar_verificacao_codigo_barras_entrada)
        # Variável para armazenar o identificador do agendamento
        self.agendamento_verificacao = None
        self.entry_quantidade_entrada = ctk.CTkEntry(self.frame_entrada5, fg_color="#ffffff", border_color="black", border_width=1, text_color="black")
        self.entry_quantidade_entrada.place(relwidth=0.4, relheight=0.09, relx=0.27,rely=0.26)
        #adicionando botão na aba saida
        self.btn_botao_adicionar_entrada = ctk.CTkButton(self.frame_entrada5, text="Adicionar", image=self.icon_photo_adicionar, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7", font=("Arial extra-bold",16), command=lambda: adicionar_produto(self.modo_rapido_entrada, self.entry_codigo_barras_entrada,self.sistema_estoque,self.produtos_entrada,self.entry_quantidade_entrada,self.label_nome_produto_entrada, self.label_preco_total_entrada, self.tree_entrada, "entrada"))
        self.btn_botao_adicionar_entrada.place(relwidth=0.95, relheight=0.13, relx=0.02, rely=0.65)
        
        
        self.btn_botao_salvar_entrada = ctk.CTkButton(self.frame_entrada4, text="", image=self.icon_photo_salvar, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7",command=lambda: registrar_movimento(self.label_data_entrada,self.group_var,self.produtos_entrada,self.sistema_estoque,self.tree_entrada, self.label_preco_total_entrada, "entrada"))
        self.btn_botao_salvar_entrada.place(relwidth=0.08, relheight=0.8, relx=0.03, rely=0.06)
        
        
        self.btn_botao_excluir_entrada = ctk.CTkButton(self.frame_entrada4, text="", image=self.icon_photo_excluir, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#c2061d", command=lambda: apagar_itens_selecionados(self.produtos_entrada, self.tree_entrada, self.label_preco_total_entrada))
        self.btn_botao_excluir_entrada.place(relwidth=0.08, relheight=0.8, relx=0.15, rely=0.06)
        
        
        
        self.btn_botao_gerar_barcode = ctk.CTkButton(self.frame_entrada4, text="", image=self.icon_gerar_barcode, compound=tk.LEFT, fg_color="#D3D3D3", text_color="black", hover_color="#95cfb7", command=lambda: abrir_janela('gerar_barcode', sistema_estoque, self.tree_entrada, self.produtos_entrada, self.label_preco_total_entrada))
        self.btn_botao_gerar_barcode.place(relwidth=0.1, relheight=0.7, relx=0.3, rely=0.06)
        
        
        
        
        
        #self.bind("<Delete>", self.apagar_itens_selecionados)
        self.btn_modo_rapido_entrada = ctk.CTkSwitch(self.frame_entrada5, text="Modo Normal",  onvalue="Ativado", offvalue="Desativado",bg_color="#F6F6F6", text_color="black", font=("Arial bold", 16), command=lambda: self.toggle_modo_rapido_entrada(self.btn_modo_rapido_entrada))
        self.btn_modo_rapido_entrada.place(relx=0.2, rely=0.5)       
        #self.entry_codigo_barras_saida.bind("<KeyRelease>", self.mostrar_nome_produto_saida)
        self.entry_quantidade_entrada.bind("<Return>", lambda event: adicionar_produto_normal(
            self.entry_codigo_barras_entrada, 
            self.entry_quantidade_entrada, 
            self.sistema_estoque, 
            self.produtos_entrada, 
            self.label_nome_produto_entrada, 
            self.tree_entrada,  # Adicionando o parâmetro tree_saida
            self.label_preco_total_entrada,  # Adicionando o parâmetro label_preco_total_saida
            "entrada"
        ))
        
        #adicionando calendario de seleção
        self.group_var = StringVar(self.frame_entrada4)
        self.group_var.set("NEW PALACE EVENTOS")
        self.data_entrada = Calendar(self.frame_entrada7, selectmode="day", date_pattern="dd/mm/yyyy",  background='#01497C', font=('Helvetica', 12), width=200, height=200)
        self.data_entrada.place(relwidth=0.9, relheight=0.7, relx=0.05,rely=0.03)
        self.btn_data_entrada = ctk.CTkButton(self.frame_entrada7, text="Selecionar data", command= lambda: selecionar_data_entrada(self.data_entrada, self.label_data_entrada))
        self.btn_data_entrada.place(relwidth=0.4, relheight=0.13, relx=0.05,rely=0.8)
        self.label_data_entrada = ctk.CTkLabel(self.frame_entrada7, text="", text_color="black", font=("Arial bold", 16), bg_color="Lightgreen")
        self.label_data_entrada.place(relx=0.5, rely=0.81) 
        self.tree_entrada = criar_treeview(self.frame_entrada1)
        self.tree_entrada.bind("<Delete>", lambda event: apagar_itens_selecionados(self.produtos_entrada, self.tree_entrada, self.label_preco_total_entrada))



    def agendar_verificacao_codigo_barras_entrada(self, event):
            # Chama a função externa passando a instância da classe e o evento
        agendar_verificacao_codigo_barras(self, event, self.entry_codigo_barras_entrada, self.modo_rapido_entrada, self.sistema_estoque, self.label_nome_produto_entrada, self.entry_quantidade_entrada, self.produtos_entrada, self.tree_entrada, self.label_preco_total_entrada, 'entrada')
    def toggle_modo_rapido_entrada(self, btn_modo_rapido_entrada):
            # Alterar a variável de modo rápido diretamente no objeto (self.modo_rapido_saida)
        self.modo_rapido_entrada = not self.modo_rapido_entrada
        if self.modo_rapido_entrada:
            btn_modo_rapido_entrada.configure(text="Modo Rápido")
        else:
            btn_modo_rapido_entrada.configure(text="Modo Normal")
            
     # Dicionário de janelas abertas
janelas = {}
def abrir_janela(tipo, sistema_estoque, tree_entrada, produtos_entrada, label_preco_total_entrada ):
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
            janela = JanelaCodeBar("db/db_file.db",tree_entrada, produtos_entrada, label_preco_total_entrada )
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