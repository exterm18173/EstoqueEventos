import sqlite3
from tkinter import Image, PhotoImage, messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import re
from PIL import Image, ImageTk
from utils.custom_entry_data import CustomEntry
from db.database import SistemaEstoque
from views.editar_movimentacao import EditarMovimentacao 
            
       
                
class JanelaMovimentacao(ctk.CTkToplevel):
    def __init__(self, db_file):  # Adicione db_file como argumento
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)  # Passe db_file aqui
        self.title("Movimentações de Estoque")
        # Obtendo as dimensões da tela
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
        
        
        self.icon_filtrar = ctk.CTkImage(light_image=Image.open("img/filtra.png"), dark_image=Image.open("img/filtra.png"),size=(30,30))
        self.icon_editar = ctk.CTkImage(light_image=Image.open("img/edit.png"), dark_image=Image.open("img/edit.png"),size=(30,30))
        #Adicionando Frames 
        self.frame_movimento1 = ctk.CTkFrame(self, fg_color="#2D3137")
        self.frame_movimento1.place(relwidth= 1 , relheight = 0.15, relx=0,rely=0)
        self.frame_movimento2 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_movimento2.place(relwidth = 1, relheight=0.2, relx=0, rely=0.15)
        self.frame_movimento3 = ctk.CTkFrame(self,fg_color="black")
        self.frame_movimento3.place(relwidth=1 , relheight=0.65, relx=0, rely=0.35)
        
        #Adicionando Label
        self.label_movimento1 = ctk.CTkLabel(self.frame_movimento1, text="FILTRAR MOVIMENTOS DE ESTOQUE", text_color="#FFFFFF", font=("Arial", 32))
        self.label_movimento1.pack(pady=15)
        self.label_movimento2 = ctk.CTkLabel(self.frame_movimento2, text="Nome:", text_color="black", font=("Arial", 12))
        self.label_movimento2.place(relx=0.01, rely=0.1)
        self.label_movimento3 = ctk.CTkLabel(self.frame_movimento2, text="Tipo:", text_color="black", font=("Arial", 12))
        self.label_movimento3.place(relx=0.01, rely=0.5)
        self.label_movimento4 = ctk.CTkLabel(self.frame_movimento2, text="Data:", text_color="black", font=("Arial", 12))
        self.label_movimento4.place(relx=0.5, rely=0.12)
        
        #Adicionando campos de filtragem
        self.entry_nome_produto_filtragem = ctk.CTkEntry(self.frame_movimento2, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_nome_produto_filtragem.place(relwidth=0.4, relheight=0.3, relx=0.06, rely=0.1)
        self.combo_tipo_movimentacao = ctk.CTkComboBox(self.frame_movimento2, values=["entrada", "saida", "devolucao"], fg_color="#FFFFFF", dropdown_fg_color="#FFFFFF", dropdown_text_color="black", button_color="#2D3137", text_color="black")
        self.combo_tipo_movimentacao.place(relwidth=0.18, relheight=0.3, relx=0.06, rely=0.5)
        self.entry_data_filtragem = CustomEntry(self.frame_movimento2, width=100, height=30, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_data_filtragem.place(relwidth=0.18, relheight=0.3, relx=0.55, rely=0.1)
        
        #Adicionando Botões
        self.btn_filtar = ctk.CTkButton(self.frame_movimento2, text="Filtrar", width=80, text_color="black", fg_color="#F8FCFF", hover_color="#9AA3AF", command=self.filtrar_movimentacoes, image=self.icon_filtrar)
        self.btn_filtar.place(relx=0.88, rely=0.5)
        self.btn_editar = ctk.CTkButton(self.frame_movimento2, text="Editar", width=80, text_color="black", fg_color="#F8FCFF", hover_color="#9AA3AF", command=self.abrir_editar_movimentacao, image=self.icon_editar)
        self.btn_editar.place(relx=0.73, rely=0.5)
        
        #Adicionando treeview

        self.tree_movimento = ttk.Treeview(self.frame_movimento3, columns=("id", "Nome", "Código de Barras", "Quantidade de movimento","Tipo Movimento", "Data Movimento", "Grupo", "Sub_grupo", "Cliente"),show="headings", height=20)
        self.tree_movimento.heading("id", text="id")
        self.tree_movimento.heading("Nome", text="Nome")
        self.tree_movimento.heading("Código de Barras", text="Código de Barras")
        self.tree_movimento.heading("Quantidade de movimento", text="QTD")
        self.tree_movimento.heading("Tipo Movimento", text="Tipo")
        self.tree_movimento.heading("Data Movimento", text="Data")
        self.tree_movimento.heading("Grupo", text="Grupo")
        self.tree_movimento.heading("Sub_grupo", text="Sub_grupo")
        self.tree_movimento.heading("Cliente", text="Sub_grupo")
        self.tree_movimento.column("id", width=20, anchor=tk.CENTER)
        self.tree_movimento.column("Nome", width=400, anchor= tk.CENTER)
        self.tree_movimento.column("Código de Barras", width=150, anchor= tk.CENTER)
        self.tree_movimento.column("Quantidade de movimento", width=80, anchor=tk.CENTER)
        self.tree_movimento.column("Tipo Movimento", width=80, anchor=tk.CENTER)
        self.tree_movimento.column("Data Movimento", width=80, anchor=tk.CENTER)
        self.tree_movimento.column("Grupo", width=150, anchor= tk.CENTER)
        self.tree_movimento.column("Sub_grupo", width=150, anchor= tk.CENTER)
        self.tree_movimento.column("Cliente", width=150, anchor= tk.CENTER)
        self.tree_movimento.grid(row=0, column=0, sticky="nsew")
        # Criando a barra de rolagem saida
        self.scroll_bar = ctk.CTkScrollbar(self.frame_movimento3, orientation="vertical", command=self.tree_movimento.yview, bg_color="#FFFFFF")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        # Configurando a barra de rolagem para o Treeview saida
        self.tree_movimento.configure(yscrollcommand=self.scroll_bar.set)
        # Configurando pesos das colunas e linhas para expandir conforme o tamanho do frame
        self.frame_movimento3.grid_rowconfigure(0, weight=1)
        self.frame_movimento3.grid_columnconfigure(0, weight=1)
              
    def filtrar_movimentacoes(self):
        nome_item = self.entry_nome_produto_filtragem.get().strip() or '%'  # Se não houver entrada, use '%' para selecionar todos os produtos
        tipo_movimentacao = self.combo_tipo_movimentacao.get().strip() or '%'  # Se não houver seleção, use '%' para selecionar todos os tipos de movimentação
        data = self.entry_data_filtragem.get().strip() or '%'  # Se não houver entrada, use '%' para selecionar todos os registros

        # Chame o método filtrar_movimentacoes do objeto SistemaEstoque passando os critérios fornecidos
        movimentacoes_filtradas = self.sistema_estoque.filtrar_movimentacoes(nome_item, tipo_movimentacao, data)
        
        # Atualize a TreeView com as movimentações filtradas
        self.atualizar_tree_movimentacoes(movimentacoes_filtradas)    
        
    def atualizar_tree_movimentacoes(self, movimentacoes):
        # Limpa a TreeView antes de atualizar
        for item in self.tree_movimento.get_children():
            self.tree_movimento.delete(item)       
        # Insere as movimentações na TreeView
        for index, movimentacao in enumerate(movimentacoes, start=1):
            self.tree_movimento.insert("", "end", text=str(index), values=movimentacao)   
        
        self.janela_edicao = None


    def abrir_editar_movimentacao(self):
        selected_item = self.tree_movimento.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione uma movimentação para editar.")
            return

        item_id = self.tree_movimento.item(selected_item)["values"][0]
        nome_item = self.tree_movimento.item(selected_item)["values"][1]
        tipo_movimento = self.tree_movimento.item(selected_item)["values"][4]
        data_movimento = self.tree_movimento.item(selected_item)["values"][5]
        cliente = self.tree_movimento.item(selected_item)["values"][8]

        # Verifica se a janela de edição já foi criada
        if self.janela_edicao and self.janela_edicao.winfo_exists():        
            # Traz a janela para frente e garante que tenha foco
            self.janela_edicao.deiconify()
            self.janela_edicao.lift()
            self.janela_edicao.focus_force()
            return

        # Cria e abre a janela de edição
        EditarMovimentacao(self, self.sistema_estoque, item_id, nome_item, tipo_movimento, data_movimento, cliente)
    


    def fechar_janela(self):
        self.destroy()  # Destruindo a janela secundária   
  
if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = JanelaMovimentacao(db_file)  # Passar root e db_file como argumentos
    app.mainloop()