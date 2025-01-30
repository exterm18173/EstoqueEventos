import sqlite3
import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from main import EstoqueApp
import socket

from main_cliente import EstoqueCliente



class SistemaEstoque:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT NOT NULL,
                            senha TEXT NOT NULL,
                            email TEXT NOT NULL,
                            tipo_usuario TEXT NOT NULL,
                            ipv4_usuario TEXT NOT NULL
                            )''')
        self.conn.commit()
    def registrar_usuario(self, usuario, senha, email, tipo, ipv4_usuario):
        self.c.execute("INSERT INTO usuarios (usuario, senha, email, tipo_usuario, ipv4_usuario) VALUES (?, ?, ?, ?, ?)", (usuario, senha, email, tipo, ipv4_usuario))
        self.conn.commit()

    def autenticar_usuario(self, usuario, senha):
        self.c.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        return self.c.fetchone()


class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.sistema_estoque = SistemaEstoque("db_file.db")
        
        self.title("ScanEstoque")
        self.geometry("700x400+450+250")
        self.iconbitmap("img/logo.ico")
        self.resizable(width=False, height=False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Adicionando imagem
        self.imagem = ctk.CTkImage(light_image=Image.open("img/login.jpg"), dark_image=Image.open("img/login.jpg"), size=(400,400))
        
        # Adicionando Frames
        self.frame1 = ctk.CTkFrame(self, fg_color="#01497C")
        self.frame1.place(relwidth=0.43, relheight=1, x=400, y=0)
        
        # Adicionando Labels
        self.label_imagem = ctk.CTkLabel(self, image=self.imagem, text="")
        self.label_imagem.place(x=0, y=0)
        self.label_login = ctk.CTkLabel(self.frame1, text="LOGIN DE USUÁRIO", text_color="#FFFFFF", font=("Roboto", 28))
        self.label_login.place(x=30, y=45)
        self.label_usuario = ctk.CTkLabel(self.frame1, text="*Obrigatório o preenchimento do campo usuário", text_color="#FFFFFF", font=("Roboto", 12))
        self.label_usuario.place(x=20, y=145)
        self.label_senha = ctk.CTkLabel(self.frame1, text="*Obrigatório o preenchimento do campo senha", text_color="#FFFFFF", font=("Roboto", 12))
        self.label_senha.place(x=20, y=225)
        self.label_cadastro = ctk.CTkLabel(self.frame1, text="Se não possui conta, Cadastre-se", text_color="#FFFFFF", font=("Roboto", 12))
        self.label_cadastro.place(x=60, y=315)
        
        # Adicionando Entry
        self.entry_usuario = ctk.CTkEntry(self.frame1, placeholder_text="Nome de Usuário", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black")
        self.entry_usuario.place(x=20, y=120)
        self.entry_senha = ctk.CTkEntry(self.frame1, placeholder_text="Senha", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black", show="*")
        self.entry_senha.place(x=20, y=200)
        
        # Adicionando Botão
        self.btn_login = ctk.CTkButton(self.frame1, text="Login", hover_color="#87BA5A", command=self.login_usuario)
        self.btn_login.place(x=80, y=270)
        self.btn_cadastro = ctk.CTkButton(self.frame1, text="Criar Conta", command=self.tela_cadastro)
        self.btn_cadastro.place(x=80, y=350)
        
    def tela_cadastro(self):
        self.frame1.place_forget()
        self.frame2 = ctk.CTkFrame(self, fg_color="#01497C")
        self.frame2.place(relwidth=0.43, relheight=1, x=400, y=0)
        
        self.label_cadastro1 = ctk.CTkLabel(self.frame2, text="CADASTRE-SE NO SISTEMA", text_color="#FFFFFF", font=("Roboto", 20))
        self.label_cadastro1.place(x=30, y=45)
        
        self.entry_usuario_cadastro = ctk.CTkEntry(self.frame2, placeholder_text="Nome de Usuário", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black")
        self.entry_usuario_cadastro.place(x=20, y=100)
        self.entry_email_cadastro = ctk.CTkEntry(self.frame2, placeholder_text="Email do Usuário", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black")
        self.entry_email_cadastro.place(x=20, y=150)
        self.entry_senha_cadastro = ctk.CTkEntry(self.frame2, placeholder_text="Senha", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black", show="*")
        self.entry_senha_cadastro.place(x=20, y=200)
        self.entry_confirmar_senha = ctk.CTkEntry(self.frame2, placeholder_text="Confirme sua Senha", width=250, font=("Roboto", 12), fg_color="#FFFFFF", text_color="black", placeholder_text_color="black", show="*")
        self.entry_confirmar_senha.place(x=20, y=250)
        self.combo_tipo_usuario = ctk.CTkComboBox(self.frame2, values=("SERVIDOR", "CLIENTE"), fg_color="#FFFFFF", text_color="black", width=100)
        self.combo_tipo_usuario.place(x=20, y=300)
        self.btn_login = ctk.CTkButton(self.frame2, text="Login", hover_color="#9AA3AF", width=80, command=self.tela_login)
        self.btn_login.place(x=10, y=350)
        self.btn_cadastrar = ctk.CTkButton(self.frame2, text="Cadastrar", fg_color="#87BA5A", command=self.cadastrar_usuario)
        self.btn_cadastrar.place(x=150, y=350)
        def get_ipv4():
            try:
                # Obtém o nome do host
                hostname = socket.gethostname()
                # Obtém o endereço IPv4 associado ao nome do host
                ipv4_address = socket.gethostbyname(hostname)
                return ipv4_address
            except Exception as e:
                print("Erro ao obter o endereço IPv4:", e)
                return None
        ipv4 = get_ipv4()
        self.label_ipv4 = ctk.CTkLabel(self.frame2, text=ipv4, text_color="#FFFFFF")
        self.label_ipv4.place(x=150, y=300)
        
        
        
    def tela_login(self):
        self.frame2.place_forget()
        self.frame1.place(relwidth=0.43, relheight=1, x=400, y=0)
        
    def cadastrar_usuario(self):
        usuario = self.entry_usuario_cadastro.get()
        senha = self.entry_senha_cadastro.get()
        confirmar_senha = self.entry_confirmar_senha.get()
        email = self.entry_email_cadastro.get()
        tipo = self.combo_tipo_usuario.get()
        ipv4_usuario = self.label_ipv4.cget("text")
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        if not usuario or not senha or not email or not tipo:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return
        
        self.sistema_estoque.registrar_usuario(usuario, senha, email, tipo, ipv4_usuario)
        messagebox.showinfo("Cadastro", "Cadastro de usuário realizado com sucesso!")
        self.tela_login()
        
    def login_usuario(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        user = self.sistema_estoque.autenticar_usuario(usuario, senha)
        
        if user:
            tipo_usuario = user[4]  # A coluna tipo_usuario é a quinta coluna no banco de dados
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.destroy()  # Fecha a janela de login
            
            if tipo_usuario == "SERVIDOR":
                self.abrir_estoque_app(EstoqueApp)
            elif tipo_usuario == "CLIENTE":
                self.abrir_estoque_app(EstoqueCliente)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            
    def abrir_estoque_app(self, app_class):
        db_file = "db/db_file.db"
        app = app_class(db_file)
        app.mainloop()
        
if __name__ == "__main__":
    app = Login()
    app.mainloop()