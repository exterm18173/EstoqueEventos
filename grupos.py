import sqlite3
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk


class Grupo:
    def __init__(self, nome):
        self.nome = nome
class SubGrupo:
    def __init__(self, subnome):
        self.subnome = subnome
        
class SistemaEstoque:
    def __init__(self, db_file, parent=None):
        self.parent = parent
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
    def __del__(self):
        self.conn.close()
    def __del__(self):
        self.conn.close()
    def adicionar_grupo(self, grupo):
        try:
            self.c.execute("INSERT INTO grupo (nome) VALUES (?)",
                           (grupo.nome,))
            self.conn.commit()
            messagebox.showinfo("Atenção", "Produto adicionado com sucesso.", parent=self.parent)
        except sqlite3.IntegrityError:
            messagebox.showinfo("Atenção", "Código de barras duplicado. Produto não adicionado.", parent=self.parent)
    def adicionar_sub_grupo(self, sub_grupo):
        try:
            self.c.execute("INSERT INTO sub_grupo (sub_nome) VALUES (?)",
                           (sub_grupo.subnome,))
            self.conn.commit()
            messagebox.showinfo("Atenção", "Sub-grupo adicionado com sucesso.", parent=self.parent)
        except sqlite3.IntegrityError:
            messagebox.showinfo("Atenção", "Nome de sub-grupo duplicado. Sub-grupo não adicionado.", parent=self.parent)
    def recuperar_grupos(self):
        self.c.execute("SELECT * FROM grupo")
        return self.c.fetchall()
    def recuperar_sub_grupos(self):
        self.c.execute("SELECT * FROM sub_grupo")
        return self.c.fetchall()
    def excluir_grupo(self, grupo_id):
        try:
            self.c.execute("DELETE FROM grupo WHERE id=?", (grupo_id,))
            self.conn.commit()
            messagebox.showinfo("Atenção", "Grupo excluído com sucesso.", parent=self.parent)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir grupo do banco de dados: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao excluir grupo do banco de dados: {e}")
    def excluir_sub_grupo(self, sub_grupo_id):
        try:
            self.c.execute("DELETE FROM sub_grupo WHERE id=?", (sub_grupo_id,))
            self.conn.commit()
            messagebox.showinfo("Atenção", "Sub-Grupo excluído com sucesso.", parent=self.parent)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir sub-grupo do banco de dados: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao excluir sub-grupo do banco de dados: {e}")
   
class JanelaGrupos(ctk.CTkToplevel):
    def __init__(self, db_file):  # Adicione db_file como argumento
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)  # Passe db_file aqui
        self.title("Cadastro de Grupos")
        self.geometry("650x450+200+315")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.resizable(width=False, height=False) 
        
        
        #adicionando tabs
        self.tabview = ctk.CTkTabview(self, fg_color = "#9AA3AF", segmented_button_fg_color="#2C3036",segmented_button_unselected_color="#2C3036", segmented_button_selected_color="#004A7C")
        self.tabview.pack(side = "bottom", expand = True, fill = "both")
        self.tabview.add("Grupo")       
        self.tabview.add("Sub_Grupo")
        self.tabview.tab("Grupo").grid_columnconfigure(0, weight=1)   
        self.tabview.tab("Sub_Grupo").grid_columnconfigure(0, weight=1)   
        
        
        #Adicionando frames Grupo
        self.frame_grupo1 = ctk.CTkFrame(self.tabview.tab("Grupo"), fg_color="#008000") 
        self.frame_grupo1.place(relwidth=1, relheight=0.3, x= 0, y= 0)     
        self.frame_grupo2 = ctk.CTkFrame(self.tabview.tab("Grupo"), fg_color="#F8FCFF") 
        self.frame_grupo2.place(relwidth=1, relheight=0.2, x= 0, y= 60)     
        self.frame_grupo3 = ctk.CTkFrame(self.tabview.tab("Grupo"), fg_color="#F8FCFF") 
        self.frame_grupo3.place(relwidth=1, relheight=0.65, x= 0, y= 142)     
        #Adicionando Labels Grupo
        self.label_grupo1 = ctk.CTkLabel(self.frame_grupo1, text="Cadastrar Tipo de Grupo", font=("Arial", 30), text_color="#FFFFFF") 
        self.label_grupo1.pack(pady=10)
        self.label_nome_grupo = ctk.CTkLabel(self.frame_grupo2, text="Nome do grupo:", font=("Arial",16), text_color="black")
        self.label_nome_grupo.place(x= 30, y= 10)
        #Adicionando botão Grupo
        self.btn_salvar_grupo = ctk.CTkButton(self.frame_grupo2, text="Salvar", width=30, height=30, hover_color="#95cfb7", fg_color="#D3D3D3", text_color="black", compound=tk.LEFT, font=("Arial",16), command=self.adicionar_grupo) 
        self.btn_salvar_grupo.place(x=350, y=35)     
        self.btn_pesquizar_grupo = ctk.CTkButton(self.frame_grupo2, text="Atualizar", width=30, height=30, hover_color="#9AA3AF", fg_color="#D3D3D3", text_color="black", compound=tk.LEFT, font=("Arial",16), command=self.atualizar_grupos) 
        self.btn_pesquizar_grupo.place(x=540, y=35)     
        self.btn_excluir_grupo = ctk.CTkButton(self.frame_grupo2, text="Excluir", width=30, height=30, hover_color="#c2061d", fg_color="#D3D3D3", text_color="black", compound=tk.LEFT, font=("Arial",16), command=self.excluir_grupo) 
        self.btn_excluir_grupo.place(x=450, y=35)   
        #Adicionando Entry Grupo
        self.entry_nome_grupo = ctk.CTkEntry(self.frame_grupo2, width=300, height=30, fg_color="#FFFFFF", text_color="black", border_color="black", border_width=1)   
        self.entry_nome_grupo.place(x=20, y=35) 
        
        #Adicionando Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Custom.Treeview", background="lightgray", foreground="black", rowheight=35, font=('Helvetica', 16))
        self.style.configure("Custom.Treeview.Heading", font=('Helvetica', 14))
        self.tree_grupos = ttk.Treeview(self.frame_grupo3, columns=("id","Grupos"),show="headings", height=16, style= "Custom.Treeview")
        self.tree_grupos.heading("#0", text="ID")
        self.tree_grupos.heading("Grupos", text="Nomes")
        self.tree_grupos.heading("id", text="id")
        self.tree_grupos.column("id", width=50)
        self.tree_grupos.column("Grupos", width=792)
        self.tree_grupos.grid(row=0, column=0, sticky="nsew")
        # Criando a barra de rolagem saida
        self.scroll_bar = ctk.CTkScrollbar(self.frame_grupo3, orientation="vertical", command=self.tree_grupos.yview, bg_color="#FFFFFF")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        # Configurando a barra de rolagem para o Treeview saida
        self.tree_grupos.configure(yscrollcommand=self.scroll_bar.set)
        # Configurando pesos das colunas e linhas para expandir conforme o tamanho do frame
        self.frame_grupo3.grid_rowconfigure(0, weight=1)
        self.frame_grupo3.grid_columnconfigure(0, weight=1)
        
        
        
        #Adicionando frames Sub_Grupo
        self.frame_sub_grupo1 = ctk.CTkFrame(self.tabview.tab("Sub_Grupo"), fg_color="#008000") 
        self.frame_sub_grupo1.place(relwidth=1, relheight=0.3, x= 0, y= 0)     
        self.frame_sub_grupo2 = ctk.CTkFrame(self.tabview.tab("Sub_Grupo"), fg_color="#F8FCFF") 
        self.frame_sub_grupo2.place(relwidth=1, relheight=0.2, x= 0, y= 60)     
        self.frame_sub_grupo3 = ctk.CTkFrame(self.tabview.tab("Sub_Grupo"), fg_color="#F8FCFF") 
        self.frame_sub_grupo3.place(relwidth=1, relheight=0.65, x= 0, y= 142)     
        #Adicionando Labels sub_Grupo
        self.label_sub_grupo1 = ctk.CTkLabel(self.frame_sub_grupo1, text="Cadastrar Tipo de Sub-Grupo", font=("Arial", 30), text_color="#FFFFFF") 
        self.label_sub_grupo1.pack(pady=10)
        self.label_nome_sub_grupo = ctk.CTkLabel(self.frame_sub_grupo2, text="Nome do sub-grupo:", font=("Arial",16), text_color="black")
        self.label_nome_sub_grupo.place(x= 30, y= 10)
        #Adicionando botão Grupo
        self.btn_salvar_sub_grupo = ctk.CTkButton(self.frame_sub_grupo2, text="Salvar", width=30, height=30, hover_color="#95cfb7", fg_color="#D3D3D3", text_color="black", compound=tk.LEFT, font=("Arial",16), command=self.adicionar_sub_grupo) 
        self.btn_salvar_sub_grupo.place(x=350, y=35)     
        self.btn_pesquizar_sub_grupo = ctk.CTkButton(self.frame_sub_grupo2, text="Atualizar", width=30, height=30, hover_color="#9AA3AF", fg_color="#D3D3D3", text_color="black", compound=tk.LEFT, font=("Arial",16), command=self.atualizar_sub_grupos) 
        self.btn_pesquizar_sub_grupo.place(x=540, y=35)  
        self.btn_excluir_sub_grupo = ctk.CTkButton(self.frame_sub_grupo2, text="Excluir", width=30, height=30, hover_color="#c2061d", fg_color="#D3D3D3", text_color="black", compound=tk.LEFT, font=("Arial",16), command=self.excluir_sub_grupo) 
        self.btn_excluir_sub_grupo.place(x=450, y=35)   
        #Adicionando Entry Grupo
        self.entry_nome_sub_grupo = ctk.CTkEntry(self.frame_sub_grupo2, width=300, height=30, fg_color="#FFFFFF", text_color="black", border_color="black", border_width=1)   
        self.entry_nome_sub_grupo.place(x=20, y=35) 
        
        #Adicionando Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Custom.Treeview", background="lightgray", foreground="black", rowheight=35, font=('Helvetica', 16))
        self.style.configure("Custom.Treeview.Heading", font=('Helvetica', 14))
        self.tree_sub_grupos = ttk.Treeview(self.frame_sub_grupo3, columns=("id", "SubGrupos"),show="headings", height=16, style= "Custom.Treeview")
        self.tree_sub_grupos.heading("#0", text="ID")
        self.tree_sub_grupos.heading("SubGrupos", text="Nomes")
        self.tree_sub_grupos.heading("id", text="id")
        self.tree_sub_grupos.column("id", width=50)
        self.tree_sub_grupos.column("SubGrupos", width=792)
        self.tree_sub_grupos.grid(row=0, column=0, sticky="nsew")
        # Criando a barra de rolagem saida
        self.scroll_bar_sub = ctk.CTkScrollbar(self.frame_sub_grupo3, orientation="vertical", command=self.tree_sub_grupos.yview, bg_color="#FFFFFF")
        self.scroll_bar_sub.grid(row=0, column=1, sticky="ns")
        # Configurando a barra de rolagem para o Treeview saida
        self.tree_sub_grupos.configure(yscrollcommand=self.scroll_bar_sub.set)
        # Configurando pesos das colunas e linhas para expandir conforme o tamanho do frame
        self.frame_sub_grupo3.grid_rowconfigure(0, weight=1)
        self.frame_sub_grupo3.grid_columnconfigure(0, weight=1)  
        
        
    def excluir_grupo(self):
        selected_item = self.tree_grupos.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um grupo para excluir.")
            return

        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este grupo?")
        if confirmacao:
            item_data = self.tree_grupos.item(selected_item)
            grupo_id = item_data['values'][0]

            self.tree_grupos.delete(selected_item)  # Remove o item da árvore

            self.sistema_estoque.excluir_grupo(grupo_id)  # Remove o item do banco de dados
            self.atualizar_grupos()   
    def excluir_sub_grupo(self):
        selected_item = self.tree_sub_grupos.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um grupo para excluir.")
            return

        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este sub-grupo?")
        if confirmacao:
            item_data = self.tree_sub_grupos.item(selected_item)
            sub_grupo_id = item_data['values'][0]

            self.tree_sub_grupos.delete(selected_item)  # Remove o item da árvore

            self.sistema_estoque.excluir_sub_grupo(sub_grupo_id)  # Remove o item do banco de dados
            self.atualizar_sub_grupos()   
    def atualizar_grupos(self, event=None):
        for item in self.tree_grupos.get_children():
            self.tree_grupos.delete(item)
        try:
            Grupo = self.sistema_estoque.recuperar_grupos()
            for index, grupo in enumerate(Grupo, start=1):
                self.tree_grupos.insert("", "end", text=str(index), values=(grupo[0], grupo[1]))
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao recuperar grupos do banco de dados: {e}")               
    def atualizar_sub_grupos(self, event=None):
        for item in self.tree_sub_grupos.get_children():
            self.tree_sub_grupos.delete(item)
        try:
            SubGrupo = self.sistema_estoque.recuperar_sub_grupos()
            for index, subgrupo in enumerate(SubGrupo, start=1):
                self.tree_sub_grupos.insert("", "end", text=str(index), values=(subgrupo[0], subgrupo[1]))
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao recuperar sub-grupos do banco de dados: {e}")               
    def fechar_janela(self):
        self.destroy()  # Destruindo a janela secundária
    def adicionar_grupo(self):
        nome = self.entry_nome_grupo.get()
        grupo = Grupo(nome)
        self.sistema_estoque.adicionar_grupo(grupo)
        self.entry_nome_grupo.delete(0, tk.END)
        
    def adicionar_sub_grupo(self):
        subnome = self.entry_nome_sub_grupo.get()
        sub_grupo = SubGrupo(subnome)
        self.sistema_estoque.adicionar_sub_grupo(sub_grupo)
        self.entry_nome_sub_grupo.delete(0, tk.END)
    
if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = JanelaGrupos(db_file)  # Passar root e db_file como argumentos
    app.mainloop()