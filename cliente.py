import sqlite3
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import socket
import time
import mysql.connector
        
class SistemaEstoque:
    def __init__(self, host, port, usuario_db, senha_db, banco_de_dados):
        self.conn = mysql.connector.connect(
            host=host,
            port=port,
            user=usuario_db,
            password=senha_db,
            database=banco_de_dados
        )
        self.c = self.conn.cursor()
    def obter_usuarios_ipv4(self):
        try:
            self.c.execute('''SELECT usuario, ipv4_usuario FROM usuarios''')
            usuarios_ipv4 = self.c.fetchall()
            return usuarios_ipv4
        except Exception as e:
            print("Erro ao obter os usuários e seus endereços IPv4:", e)
            return None

      
class JanelaCliente(ctk.CTk):
    def __init__(self, root):  # Adicione db_file como argumento
        super().__init__()
        
        self.root = root
        self.title("Sincronizar Banco de Dados")
        self.geometry("450x250+200+315")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.resizable(width=False, height=False) 
        
        
       
       #Adicionando Frames
        self.frame_socket1 = ctk.CTkFrame(self, fg_color="#2D3137")
        self.frame_socket1.place(relwidth = 1, relheight= 0.2, x=0, y=0)
        self.frame_socket2 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_socket2.place(relwidth = 0.5, relheight= 0.8, x=0, y=50)
        self.frame_socket3 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame_socket3.place(relwidth = 0.5, relheight= 0.8, x=225, y=50)
       #Adicionando Botões
        

        self.btn_socket_ipv4_1 = ctk.CTkButton(self.frame_socket2, text="Receber Banco de Dados", command=self.receber_banco_dados)
        self.btn_socket_ipv4_1.place(x=10, y=150)
        self.btn_socket_ipv4_2 = ctk.CTkButton(self.frame_socket2, text="Buscar Cadastrados", command=self.buscar_usuarios)
        self.btn_socket_ipv4_2.place(x=10, y=20)
       #Adicionando Labels
        self.label_socket2 = ctk.CTkLabel(self.frame_socket1, text="Sincronizar Banco de Dados", text_color="#FFFFFF", font=("Roboto", 20))
        self.label_socket2.pack(pady=10)
        self.label_socket3 = ctk.CTkLabel(self.frame_socket2, text="Insira o IPV4 do Servidor", text_color="black", font=("Roboto", 12))
        self.label_socket3.place(x=5, y=60)
        #Adicionanod Entry
        self.entry_socket = ctk.CTkEntry(self.frame_socket2, width=150, fg_color="#FFFFFF", text_color="black")
        self.entry_socket.place(x=5, y=90)
        #Adicionado treeview
        self.tree_ipv4 = ttk.Treeview(self.frame_socket3, columns=("Nome", "IPV4"), show="headings", height=20)
        self.tree_ipv4.heading("Nome", text="Nome")
        self.tree_ipv4.heading("IPV4", text="IPV4 Usuario")
        self.tree_ipv4.column("Nome", width=80, anchor=tk.CENTER)
        self.tree_ipv4.column("IPV4", width=100, anchor=tk.CENTER)
        self.tree_ipv4.grid(row=0, column=0, sticky="nsew")
        # Criando a barra de rolagem saida
        self.scroll_bar = ctk.CTkScrollbar(self.frame_socket3, orientation="vertical", command=self.tree_ipv4.yview)
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        # Configurando a barra de rolagem para o Treeview saida
        self.tree_ipv4.configure(yscrollcommand=self.scroll_bar.set)
        # Configurando pesos das colunas e linhas para expandir conforme o tamanho do frame
        self.frame_socket3.grid_rowconfigure(0, weight=1)
        self.frame_socket3.grid_columnconfigure(0, weight=1)
        self.tree_ipv4.bind("<ButtonRelease-1>", self.selecionar_usuario)
    def buscar_usuarios(self):
        usuarios_ipv4 = self.sistema_estoque.obter_usuarios_ipv4()
        
        # Atualize a TreeView com as movimentações filtradas
        self.atualizar_tree_ipv4(usuarios_ipv4)   
        
    def atualizar_tree_ipv4(self, usuarios_ipv4):
        for item in self.tree_ipv4.get_children():
            self.tree_ipv4.delete(item)       
        for index, usuario in enumerate(usuarios_ipv4, start=1):
            self.tree_ipv4.insert("", "end", text=str(index), values=usuario)
    def receber_banco_dados(self):
        while True:
            # Criação do cliente
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                ipv4_sevidor = self.entry_socket.get()
                cliente.connect((ipv4_sevidor, 7777)) # Endereço IP do servidor e porta
                print("Conectado!!")

                namefile = "db/db_file.db"
                cliente.send(namefile.encode())
                with open(namefile, "wb") as file:
                    while True:
                        data = cliente.recv(1000000000)
                        if not data:
                            break
                        file.write(data)
                print(f'{namefile} recebido!')
                break
            except Exception as e:
                print("Erro ao conectar:", e)
                time.sleep(10)
                break
            finally:
                cliente.close()

        
        
    def selecionar_usuario(self, event):
        item = self.tree_ipv4.selection()[0]
        ipv4_selecionado = self.tree_ipv4.item(item, "values")[1]
        self.entry_socket.delete(0, tk.END)
        self.entry_socket.insert(0, ipv4_selecionado)                    
    def fechar_janela(self):
        self.root.destroy()  # Destruindo a janela principal
        self.destroy()  # Destruindo a janela secundária    
if __name__ == "__main__":
   

    root = ctk.CTk()
    app = JanelaCliente(root)
    app.mainloop()