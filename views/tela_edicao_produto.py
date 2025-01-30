import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
import customtkinter as ctk
from db.database import SistemaEstoque


class TelaEdicaoItem(ctk.CTkToplevel):
    def __init__(self, root, db_file, id_produto):  # Adicione db_file e id_produto como argumentos
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)  # Passe db_file aqui
        self.root = root
        self.id_produto = id_produto
        self.title("Edição de Itens")
        self.geometry("650x450+200+315")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW")
        self.resizable(width=False, height=False)  
               
        # Adicionando frames
        self.frame_edicao1 = ctk.CTkFrame(self, fg_color="#01497C")
        self.frame_edicao1.place(relwidth= 1, relheight= 0.2, x=0, y=0 )
        self.frame_edicao2 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_edicao2.place(relwidth= 1, relheight= 0.8, x= 0, y= 90)


        # Adicionando Labels
        self.label_edicao1 = ctk.CTkLabel(self.frame_edicao1, text="EDITAR ITEM SELECIONADO", text_color="#FFFFFF", font=("Arial", 38))
        self.label_edicao1.pack(pady=25)
        self.label_edicao2 = ctk.CTkLabel(self.frame_edicao2, text="Dados do item:", text_color="black", font=("Arial", 22))
        self.label_edicao2.place(x=20 , y=20)
        self.label_edicao3 = ctk.CTkLabel(self.frame_edicao2, text="Nome:", text_color="black", font=("Arial", 14))
        self.label_edicao3.place(x=20 , y=50)
        self.label_edicao4 = ctk.CTkLabel(self.frame_edicao2, text="Código de Barras:", text_color="black", font=("Arial", 14))
        self.label_edicao4.place(x=20 , y=100)
        self.label_edicao5 = ctk.CTkLabel(self.frame_edicao2, text="Valor:", text_color="black", font=("Arial", 14))
        self.label_edicao5.place(x=20 , y=150)
        self.label_edicao6 = ctk.CTkLabel(self.frame_edicao2, text="Quantidade:", text_color="black", font=("Arial", 14))
        self.label_edicao6.place(x=20 , y=200)
        self.label_edicao7 = ctk.CTkLabel(self.frame_edicao2, text="Grupo:", text_color="black", font=("Arial", 14))
        self.label_edicao7.place(x=20 , y=250)
        self.label_edicao7 = ctk.CTkLabel(self.frame_edicao2, text="Sub-Grupo:", text_color="black", font=("Arial", 14))
        self.label_edicao7.place(x=20 , y=300)
        
        # Adicionando Entry
        self.entry_nome = ctk.CTkEntry(self.frame_edicao2, width=400, height=25, fg_color="#FFFFFF", text_color="black")
        self.entry_nome.place(x=70, y= 53)       
        self.entry_codigo_barras = ctk.CTkEntry(self.frame_edicao2, width=200, height=25, fg_color="#FFFFFF", text_color="black")
        self.entry_codigo_barras.place(x=140, y= 103) 
        self.entry_preco_unitario = ctk.CTkEntry(self.frame_edicao2, width=100, height=25, fg_color="#FFFFFF", text_color="black")
        self.entry_preco_unitario.place(x=70, y= 153)
        self.entry_quantidade = ctk.CTkEntry(self.frame_edicao2, width=100, height=25, fg_color="#FFFFFF", text_color="black")
        self.entry_quantidade.place(x=100, y= 203)
        

        self.entry_grupo = ctk.CTkComboBox(self.frame_edicao2, text_color= "black", fg_color="#FFFFFF", width=200, height=30, bg_color="#FFFFFF", button_color="green", dropdown_fg_color="#FFFFFF", dropdown_text_color="black")
        self.entry_grupo.place(x=70, y=253)
        self.carregar_valores_grupo()
            
        self.entry_sub_grupo = ctk.CTkComboBox(self.frame_edicao2, text_color="black", fg_color="#FFFFFF", width=200, height=30, bg_color="#FFFFFF", button_color="green", dropdown_fg_color="#FFFFFF", dropdown_text_color="black")
        self.entry_sub_grupo.place(x=100, y=303)
        self.carregar_valores_sub_grupo()

        # Adicione um evento para monitorar a digitação na combobox
        self.entry_sub_grupo.bind('<KeyRelease>', self.filtrar_subgrupos)

        # Adicionando Botão
        self.btn_salvar_edicao = ctk.CTkButton(self.frame_edicao2, text="Salvar", text_color="black", font=("Arial", 14), fg_color="#D3D3D3", hover_color="#90EE90", command=self.salvar_edicao)
        self.btn_salvar_edicao.place(x=400, y=300)

        # Carregar informações do item após criar os widgets
        self.carregar_informacoes_item()

    def carregar_valores_grupo(self):
        # Recuperar os valores da tabela 'grupo'
        self.c = self.conn.cursor()
        self.c.execute("SELECT nome FROM grupo")
        grupos = self.c.fetchall()

        # Extrair apenas os nomes dos grupos
        nomes_grupos = [grupo[0] for grupo in grupos]
        # Definir os valores no OptionMenu do grupo
        self.entry_grupo.configure(values=nomes_grupos)

    def carregar_valores_sub_grupo(self):
        # Recuperar os valores da tabela 'sub_grupo'
        self.c = self.conn.cursor()
        self.c.execute("SELECT sub_nome FROM sub_grupo")
        sub_grupos = self.c.fetchall()
        # Extrair apenas os nomes dos subgrupos
        nomes_sub_grupos = [sub_grupo[0] for sub_grupo in sub_grupos]
        # Definir os valores no OptionMenu do subgrupo
        self.entry_sub_grupo.configure(values=nomes_sub_grupos)

    def carregar_informacoes_item(self):
        try:
            self.c.execute("SELECT * FROM produtos WHERE id=?", (self.id_produto,))
            produto = self.c.fetchone()
            if produto:
                # Preencher os campos com as informações do produto
                self.entry_nome.insert(0, produto[1])
                self.entry_codigo_barras.insert(0, produto[2])
                self.entry_preco_unitario.insert(0, produto[3])
                self.entry_quantidade.insert(0, produto[4])
                # Configurar a combobox de grupo e subgrupo para exibir os valores corretos
                if produto[5] in self.entry_grupo.cget('values'):
                    self.entry_grupo.set(produto[5])
                if produto[6] in self.entry_sub_grupo.cget('values'):
                    self.entry_sub_grupo.set(produto[6])
            else:
                messagebox.showerror("Erro", "Item não encontrado.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar informações do item: {e}")


    def filtrar_subgrupos(self, event):
        # Obtém o texto atualmente digitado na combobox de subgrupo
        texto_digitado = self.entry_sub_grupo.get().lower()
        # Obtém todos os valores disponíveis na combobox de subgrupo
        valores_disponiveis = self.entry_sub_grupo.cget('values')
        # Filtra os valores baseados no texto digitado
        valores_filtrados = [valor for valor in valores_disponiveis if texto_digitado in valor.lower()]
        # Atualiza os valores na combobox de subgrupo
        self.entry_sub_grupo.configure(values=valores_filtrados)
        # Simula a pressão da seta para baixo para abrir a dropdown
        self.entry_sub_grupo.event_generate('<Down>')
    def salvar_edicao(self):
        novo_nome = self.entry_nome.get().strip()
        novo_codigo_barras = self.entry_codigo_barras.get().strip()
        novo_preco_unitario = self.entry_preco_unitario.get().strip()
        novo_quantidade = self.entry_quantidade.get().strip()
        novo_grupo = self.entry_grupo.get().strip()
        novo_sub_grupo = self.entry_sub_grupo.get().strip()
        if novo_nome and novo_codigo_barras and novo_preco_unitario:
            try:
                self.sistema_estoque.c.execute("UPDATE produtos SET nome=?, codigo_barras=?, preco_unitario=?, quantidade_estoque=?, grupo=?, sub_grupo=? WHERE id=?",
                                                (novo_nome, novo_codigo_barras, novo_preco_unitario, novo_quantidade, novo_grupo, novo_sub_grupo, self.id_produto))
                self.sistema_estoque.conn.commit()
                messagebox.showinfo("Sucesso", "Edição do item salva com sucesso.")
                
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao salvar edição do item: {e}")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            

