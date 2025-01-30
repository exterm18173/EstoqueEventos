import sqlite3
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import socket

        
class SistemaEstoque:
    def __init__(self, db_file, parent=None):
        self.parent = parent
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
    def __del__(self):
        self.conn.close()
      
class JanelaServidor(ctk.CTkToplevel):
    def __init__(self, db_file):  # Adicione db_file como argumento
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)  # Passe db_file aqui
        self.title("Sincronizar Banco de Dados")
        self.geometry("450x250+200+315")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.resizable(width=False, height=False) 
        
        
       
       #Adicionando Frames
        self.frame_socket1 = ctk.CTkFrame(self, fg_color="#2D3137")
        self.frame_socket1.place(relwidth = 1, relheight= 0.2, x=0, y=0)
        self.frame_socket2 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_socket2.place(relwidth = 1, relheight= 0.8, x=0, y=50)
       #Adicionando Botões
        def adicionar_ipv4 ():
            ipv4 = get_ipv4()
            self.label_socket1.configure(text=ipv4)
        self.btn_socket_ipv4_1 = ctk.CTkButton(self.frame_socket2, text="Buscar Ipv4 local", command=adicionar_ipv4)
        self.btn_socket_ipv4_1.place(x=10, y=50)
        self.btn_socket_ipv4_2 = ctk.CTkButton(self.frame_socket2, text="Enviar Banco de Dados", command=self.enviar_banco_dados)
        self.btn_socket_ipv4_2.place(x=280, y=150)
       #Adicionando Labels
        self.label_socket1 = ctk.CTkLabel(self.frame_socket2, text="", text_color="black")
        self.label_socket1.place(x=180, y=50)
        self.label_socket2 = ctk.CTkLabel(self.frame_socket1, text="Sincronizar Banco de Dados - SERVIDOR", text_color="#FFFFFF", font=("Roboto", 20))
        self.label_socket2.pack(pady=10)
        self.label_socket3 = ctk.CTkLabel(self.frame_socket2, text="Para sincronizar o banco de dados, deve inserir esse IPV4 \n no outro no dispositivo que deseja atualizar", text_color="black", font=("Roboto", 12))
        self.label_socket3.place(x=5, y=20)
       
        
       
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
    def enviar_banco_dados(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(("", 7777))
        server.listen(2)

        # Define um tempo limite de 10 segundos para a conexão
        server.settimeout(10)

        try:
            connection, address = server.accept()
            namefile = connection.recv(1024).decode()
            with open(namefile, 'rb') as file:
                for data in file.readlines():
                    connection.send(data)
            messagebox.showinfo("ATENÇÃO", "Banco de Dados Enviado!")
        except socket.timeout:
            messagebox.showinfo("ATENÇÃO", "Tempo limite de conexão excedido. Não foi possível enviar o banco de dados.")
        finally:
            server.close() 
        
        
                        
    def fechar_janela(self):
        self.destroy()  # Destruindo a janela secundária    
if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = JanelaServidor(db_file)  # Passar root e db_file como argumentos
    app.mainloop()