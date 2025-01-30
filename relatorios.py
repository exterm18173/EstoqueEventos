import sqlite3
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import re
from PIL import Image, ImageTk
from imprimir_relatorios import ImprimirRelatorio


class SistemaEstoque:
    def __init__(self, db_file, parent=None):
        self.parent= parent
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()  
    def __del__(self):
        self.conn.close()

    def filtrar_movimentacoes(self, nome_item, data):
        try:
            # Define a consulta para calcular a quantidade total considerando saídas e devoluções
            query = """SELECT id, nome_item, codigo_barras, (SUM(CASE WHEN tipo_movimento = 'saida' THEN quantidade_movimento ELSE 0 END) -SUM(CASE WHEN tipo_movimento = 'devolucao' THEN quantidade_movimento ELSE 0 END)) as quantidade_total, data_movimento, valor_movimento FROM movimentacoes WHERE nome_item LIKE ? AND data_movimento LIKE ? GROUP BY nome_item, codigo_barras, data_movimento, valor_movimento"""
            # Executa a consulta com os filtros fornecidos
            self.c.execute(query, ('%' + nome_item + '%', '%' + data + '%'))
            movimentacoes_filtradas = self.c.fetchall()
            
            # Filtra as movimentações para remover aquelas com quantidade_total igual a 0
            movimentacoes_filtradas = [mov for mov in movimentacoes_filtradas if mov[3] != 0]

            return movimentacoes_filtradas
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao filtrar movimentações: {e}")     
            
class CustomEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<KeyRelease>", self.format_date)
    def format_date(self, event):
        current_text = self.get()
        current_text = re.sub(r'[^0-9/]', '', current_text)  # Remove caracteres que não são números ou barras
        current_text = re.sub(r'/', '', current_text)  # Remove todas as barras existentes
        if len(current_text) > 8:  # Limita a quantidade máxima de caracteres para formar uma data
            current_text = current_text[:8]
        formatted_text = ""
        for i, char in enumerate(current_text):
            if i in [2, 4]:  # Adiciona uma barra nas posições corretas
                formatted_text += "/"
            formatted_text += char
        self.delete("0", "end")
        self.insert("0", formatted_text)
                
                
class JanelaRelatorio(ctk.CTkToplevel):
    def __init__(self, db_file):  # Adicione db_file como argumento
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)  # Passe db_file aqui
        self.title("BALANCETE")
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        largura_janela = largura_tela * 0.7  # 71.5% da largura da tela
        altura_janela = altura_tela * 0.6  # 85.7% da altura da tela
        x_pos = largura_tela * 0.005  # Posição horizontal (0% da largura da tela)
        y_pos = altura_tela * 0.27  # Posição vertical (14.5% da altura da tela)
        self.geometry(f"{int(largura_janela)}x{int(altura_janela)}+{int(x_pos)}+{int(y_pos)}")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        #self.resizable(width=False, height=False) 
        self.itens = []
        self.icon_filtrar = ctk.CTkImage(light_image=Image.open("img/filtra.png"), dark_image=Image.open("img/filtra.png"),size=(30,30))
        self.img_gerar_re = ctk.CTkImage(light_image=Image.open('img/gerar_re.png'), dark_image=Image.open('img/gerar_re.png'), size=(30,30))
        #Adicionando Frames 
        self.frame_movimento1 = ctk.CTkFrame(self, fg_color="#2D3137")
        self.frame_movimento1.place(relwidth= 1 , relheight = 0.15, relx=0,rely=0)
        self.frame_movimento2 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_movimento2.place(relwidth = 1, relheight=0.2, relx=0, rely=0.15)
        self.frame_movimento3 = ctk.CTkFrame(self,fg_color="black")
        self.frame_movimento3.place(relwidth=1 , relheight=0.65, relx=0, rely=0.35)
        
        #Adicionando Label
        self.label_movimento1 = ctk.CTkLabel(self.frame_movimento1, text="BALANCETE DE SAIDAS DE ESTOQUE", text_color="#FFFFFF", font=("Arial", 40))
        self.label_movimento1.place(relwidth=0.9 , relheight=0.65, relx=0.05, rely=0.1)
        self.label_movimento2 = ctk.CTkLabel(self.frame_movimento2, text="Nome:", text_color="black", font=("Arial", 12))
        self.label_movimento2.place(relx=0.01, rely=0.08)
        self.label_movimento4 = ctk.CTkLabel(self.frame_movimento2, text="Data:", text_color="black", font=("Arial", 12))
        self.label_movimento4.place(relx=0.01, rely=0.5)
        self.label_preco_total = ctk.CTkLabel(self.frame_movimento2, text="Valor Total:\nR$0.00", text_color="black", font=("Arial extra-bold", 16))
        self.label_preco_total.place(relx=0.5, rely=0.08)
        
        #Adicionando campos de filtragem
        self.entry_nome_produto_filtragem = ctk.CTkEntry(self.frame_movimento2, width=300, height=30, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_nome_produto_filtragem.place(relx=0.05, rely=0.08)

        self.entry_data_filtragem = CustomEntry(self.frame_movimento2, width=100, height=30, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_data_filtragem.place(relx=0.05, rely=0.5)
        
        #Adicionando Botões
        self.btn_filtar = ctk.CTkButton(self.frame_movimento2, text="Filtrar", width=80, text_color="#FFFFFF", fg_color="#2D3137", hover_color="#9AA3AF", command=self.filtrar_movimentacoes, image=self.icon_filtrar)
        self.btn_filtar.place(relx=0.85, rely=0.6)
        self.btn_re = ctk.CTkButton(self.frame_movimento2, text="Gerar Relatorios", width=80, text_color="#FFFFFF", fg_color="#2D3137", hover_color="#9AA3AF", command=abrir_janela_gerar_re, image=self.img_gerar_re)
        self.btn_re.place(relx=0.82, rely=0.08)
        
        #Adicionando treeview

        self.tree_movimento = ttk.Treeview(self.frame_movimento3, columns=("id", "Nome", "Código de Barras", "Quantidade de movimento", "Data Movimento", "Valor Unitario", "Valor Total"),show="headings", height=20)
        self.tree_movimento.heading("id", text="id")
        self.tree_movimento.heading("Nome", text="Nome")
        self.tree_movimento.heading("Código de Barras", text="Código de Barras")
        self.tree_movimento.heading("Quantidade de movimento", text="QTD")
        self.tree_movimento.heading("Data Movimento", text="Data")
        self.tree_movimento.heading("Valor Unitario", text="Valor und")
        self.tree_movimento.heading("Valor Total", text="Total")
        self.tree_movimento.column("id", width=20, anchor=tk.CENTER)
        self.tree_movimento.column("Nome", width=400)
        self.tree_movimento.column("Código de Barras", width=150, anchor= tk.CENTER)
        self.tree_movimento.column("Quantidade de movimento", width=80, anchor=tk.CENTER)
        self.tree_movimento.column("Data Movimento", width=80, anchor=tk.CENTER)
        self.tree_movimento.column("Valor Unitario", width=150, anchor= tk.CENTER)
        self.tree_movimento.column("Valor Total", width=150, anchor= tk.CENTER)
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

        data = self.entry_data_filtragem.get().strip() or '%'  # Se não houver entrada, use '%' para selecionar todos os registros

        # Chame o método filtrar_movimentacoes do objeto SistemaEstoque passando os critérios fornecidos
        movimentacoes_filtradas = self.sistema_estoque.filtrar_movimentacoes(nome_item, data)
        
        # Atualize a TreeView com as movimentações filtradas
        self.atualizar_tree_movimentacoes(movimentacoes_filtradas)    
        
    def atualizar_tree_movimentacoes(self, movimentacoes):
        # Limpa a TreeView antes de atualizar
        for item in self.tree_movimento.get_children():
            self.tree_movimento.delete(item)
            self.itens.clear()
            self.atualizar_valor_total()       
        # Insere as movimentações na TreeView
        for index, movimentacao in enumerate(movimentacoes, start=1):
            valor_total = movimentacao[3] * movimentacao[5]
            nova_movimentacao = list(movimentacao) + [valor_total]
            self.itens.append(nova_movimentacao)
            self.tree_movimento.insert("", "end", text=str(index), values=nova_movimentacao)
            self.atualizar_valor_total()
    def atualizar_valor_total(self):
        total = sum(item[6] for item in self.itens)
        self.label_preco_total.configure(text=f"Valor Total: \nR${total:.2f}")
    def fechar_janela(self):
        self.destroy()  # Destruindo a janela secundária    

janela_gerar_re = None
def abrir_janela_gerar_re():
    global janela_gerar_re    
    if janela_gerar_re is None or not janela_gerar_re.winfo_exists():
        janela_gerar_re = ImprimirRelatorio("db/db_file.db")
        janela_gerar_re.protocol("WM_DELETE_WINDOW", lambda: fechar_janela_gerar_re())
        janela_gerar_re.mainloop()
    else:
        janela_gerar_re.deiconify()  # Garante que a janela está restaurada (não minimizada)
        janela_gerar_re.lift()
        janela_gerar_re.focus_force()
def fechar_janela_gerar_re():
    global janela_gerar_re
    if janela_gerar_re:
        janela_gerar_re.destroy()
    janela_gerar_re = None   



if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = JanelaRelatorio(db_file)  # Passar root e db_file como argumentos
    app.mainloop()