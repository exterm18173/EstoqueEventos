import sqlite3
from tkinter import END, messagebox, ttk
import customtkinter as ctk
from PIL import Image

class SistemaEstoque:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
    
    def __del__(self):
        self.conn.close()

class CadastroEvento(ctk.CTkToplevel):

    def __init__(self, db_file):
        super().__init__()
        
        self.title("Cadastro de Eventos")
        self.geometry("550x400+450+250")
        self.iconbitmap("img/logo.ico")
        self.resizable(width=False, height=False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Inicializa a conexão com o banco de dados
        self.sistema_estoque = SistemaEstoque(db_file)

        # Adicionando imagem
        self.imagem = ctk.CTkImage(light_image=Image.open("img/login.jpg"), dark_image=Image.open("img/login.jpg"), size=(400, 400))

        # Adicionando Frames
        self.frame1 = ctk.CTkFrame(self, fg_color="#01497C")
        self.frame1.place(relwidth=0.55, relheight=1, relx=0.225, y=0)

        self.label_titulo = ctk.CTkLabel(self.frame1, text="CADASTRO DE EVENTOS", text_color="#FFFFFF", font=("Roboto", 22))
        self.label_titulo.place(x=15, y=45)
        
        # Labels de instrução
        self.label_nome = ctk.CTkLabel(self.frame1, text="*Preencha todos os campos", text_color="#FFFFFF", font=("Roboto", 12))
        self.label_nome.place(x=20, y=145)
        
        # Adicionando Entries
        self.entry_nome_evento = ctk.CTkEntry(self.frame1, placeholder_text="Nome do Evento", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black")
        self.entry_nome_evento.place(x=20, y=120)
        
        # ComboBox para a escolha de datas
        self.combo_data_evento = ctk.CTkComboBox(self.frame1, values=["Escolha uma data", "Todas as datas"], width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", command=self.atualiza_entry_data)
        self.combo_data_evento.place(x=20, y=200)
        
        # Entry para data específica
        self.entry_data_evento = ctk.CTkEntry(self.frame1, placeholder_text="Data (DD/MM/YYYY)", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black")
        self.entry_data_evento.place(x=20, y=240)
        self.entry_data_evento.place_forget()  # Esconde inicialmente
        
        # ComboBox para o tipo de evento
        self.combo_tipo_evento = ctk.CTkComboBox(self.frame1, values=["CASAMENTO", "FORMATURA", "NEW PALACE", "PALESTRA", "DECORAÇÃO", "DELIVERY"], width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black")
        self.combo_tipo_evento.place(x=20, y=280)

        # Adicionando Botão
        self.btn_cadastrar_evento = ctk.CTkButton(self.frame1, text="Cadastrar Evento", fg_color="#87BA5A", command=self.cadastrar_evento)
        self.btn_cadastrar_evento.place(relx=0.05, rely=0.85)

        # Botão para abrir a tela de eventos
        self.btn_ver_eventos = ctk.CTkButton(self.frame1, text="Ver Eventos", command=self.abrir_tela_eventos)
        self.btn_ver_eventos.place(relx=0.5, rely=0.85)

    def atualiza_entry_data(self, escolha):
        if escolha == "Escolha uma data":
            self.entry_data_evento.place(x=20, y=240)  # Mostra o Entry
        else:
            self.entry_data_evento.place_forget()  # Esconde o Entry

    def cadastrar_evento(self):
        nome_evento = self.entry_nome_evento.get()
        tipo_evento = self.combo_tipo_evento.get()
        data_evento = self.entry_data_evento.get() if self.combo_data_evento.get() == "Escolha uma data" else "Todas as datas"
        
        # Validação básica da data
        if self.combo_data_evento.get() == "Escolha uma data" and data_evento:
            try:
                dia, mes, ano = map(int, data_evento.split('/'))
                if not (1 <= dia <= 31) or not (1 <= mes <= 12) or ano < 1900:
                    raise ValueError("Data inválida")
            except ValueError:
                messagebox.showwarning("Atenção", "Formato de data inválido! Use DD/MM/YYYY.")
                return

        if nome_evento and tipo_evento:
            # Aqui você pode adicionar a lógica para inserir no banco de dados
            self.sistema_estoque.c.execute("INSERT INTO eventos (nome, tipo, data) VALUES (?, ?, ?)", (nome_evento, tipo_evento, data_evento))
            self.sistema_estoque.conn.commit()
            
            self.entry_nome_evento.delete(0, END)
            self.entry_data_evento.delete(0, END)
            self.combo_tipo_evento.set("CASAMENTO")  # Resetando para o valor padrão
            self.combo_data_evento.set("Escolha uma data")  # Resetando para o valor padrão
            self.entry_data_evento.place_forget()  # Esconde o Entry após cadastrar
            messagebox.showinfo("Sucesso", "Evento cadastrado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def abrir_tela_eventos(self):
        TelaEventos(self.sistema_estoque)

class TelaEventos(ctk.CTkToplevel):
    
    def __init__(self, sistema_estoque):
        super().__init__()

        self.title("Lista de Eventos")
        self.geometry("600x400+450+250")
        self.iconbitmap("img/logo.ico")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.sistema_estoque = sistema_estoque
        
        self.label_titulo = ctk.CTkLabel(self, text="Eventos Cadastrados", font=("Roboto", 22))
        self.label_titulo.pack(pady=10)

        # Criando Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Tipo", "Data"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Data", text="Data")
        self.tree.pack(pady=10, fill='both', expand=True)

        # Botões para editar e apagar
        self.btn_editar = ctk.CTkButton(self, text="Editar Evento", command=self.editar_evento)
        self.btn_editar.pack(pady=5)

        self.btn_apagar = ctk.CTkButton(self, text="Apagar Evento", command=self.apagar_evento)
        self.btn_apagar.pack(pady=5)

        self.carregar_eventos()

    def carregar_eventos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)  # Limpa a árvore
        self.sistema_estoque.c.execute("SELECT * FROM eventos")
        eventos = self.sistema_estoque.c.fetchall()

        for evento in eventos:
            self.tree.insert("", "end", values=evento)  # Adiciona os eventos à árvore

    def editar_evento(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            id_evento = item['values'][0]

            # Abre a tela de edição
            self.editar_tela = ctk.CTkToplevel(self)
            self.editar_tela.title("Editar Evento")
            
            self.label_nome = ctk.CTkLabel(self.editar_tela, text="Nome do Evento:")
            self.label_nome.pack(pady=5)
            self.entry_nome = ctk.CTkEntry(self.editar_tela, width=250)
            self.entry_nome.pack(pady=5)
            self.entry_nome.insert(0, item['values'][1])  # Nome

            self.label_tipo = ctk.CTkLabel(self.editar_tela, text="Tipo do Evento:")
            self.label_tipo.pack(pady=5)
            self.entry_tipo = ctk.CTkEntry(self.editar_tela, width=250)
            self.entry_tipo.pack(pady=5)
            self.entry_tipo.insert(0, item['values'][2])  # Tipo

            self.label_data = ctk.CTkLabel(self.editar_tela, text="Data do Evento:")
            self.label_data.pack(pady=5)
            self.entry_data = ctk.CTkEntry(self.editar_tela, width=250)
            self.entry_data.pack(pady=5)
            self.entry_data.insert(0, item['values'][3])  # Data

            self.btn_salvar = ctk.CTkButton(self.editar_tela, text="Salvar", command=lambda: self.salvar_evento(id_evento))
            self.btn_salvar.pack(pady=10)
        else:
            messagebox.showwarning("Atenção", "Selecione um evento para editar.")

    def salvar_evento(self, id_evento):
        nome = self.entry_nome.get()
        tipo = self.entry_tipo.get()
        data = self.entry_data.get()

        self.sistema_estoque.c.execute("UPDATE eventos SET nome=?, tipo=?, data=? WHERE id=?", (nome, tipo, data, id_evento))
        self.sistema_estoque.conn.commit()
        
        self.carregar_eventos()
        self.editar_tela.destroy()
        messagebox.showinfo("Sucesso", "Evento atualizado com sucesso!")

    def apagar_evento(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_evento = self.tree.item(selected_item)['values'][0]
            if messagebox.askyesno("Confirmar", "Você tem certeza que deseja apagar este evento?"):
                self.sistema_estoque.c.execute("DELETE FROM eventos WHERE id=?", (id_evento,))
                self.sistema_estoque.conn.commit()
                self.carregar_eventos()
                messagebox.showinfo("Sucesso", "Evento apagado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "Selecione um evento para apagar.")

if __name__ == "__main__":
    db_file = "db/db_file.db"
    app = CadastroEvento(db_file)  # Passar db_file como argumento
    app.mainloop()
