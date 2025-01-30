# treeview_utils.py
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

def criar_treeview(parent):
    """ Cria e configura a Treeview para uso nas diferentes tabs """
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Custom.Treeview", background="lightgray", foreground="black", rowheight=45, font=('Helvetica', 18))
    style.configure("Custom.Treeview.Heading", font=('Helvetica', 16))

    tree = ttk.Treeview(parent, columns=("Nome", "Código de Barras", "Preço", "Quantidade", "Valor Total", "Grupo", "Sub_Grupo"), show="headings", height=20, style="Custom.Treeview")
    
    # Definindo as colunas
    tree.heading("#0", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Código de Barras", text="Código de Barras")
    tree.heading("Preço", text="Preço")
    tree.heading("Quantidade", text="QTD")
    tree.heading("Valor Total", text="Valor Total")
    tree.heading("Grupo", text="Grupo")
    tree.heading("Sub_Grupo", text="Sub_Grupo")
    
    # Definindo o tamanho das colunas
    tree.column("#0", width=150, anchor=tk.CENTER)
    tree.column("Nome", width=450)
    tree.column("Código de Barras", width=200, anchor=tk.CENTER)
    tree.column("Preço", width=100, anchor=tk.CENTER)
    tree.column("Quantidade", width=90, anchor=tk.CENTER)
    tree.column("Valor Total", width=120, anchor=tk.CENTER)
    tree.column("Grupo", width=0, anchor=tk.CENTER)
    tree.column("Sub_Grupo", width=0, anchor=tk.CENTER)

    tree.grid(row=0, column=0, sticky="nsew")

    # Adicionando a barra de rolagem
    scroll_bar = ctk.CTkScrollbar(parent, orientation="vertical", command=tree.yview)
    scroll_bar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scroll_bar.set)

    # Configuração de grid
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    
    return tree
