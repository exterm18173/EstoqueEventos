from datetime import datetime
import os
import math
import re
from tkinter import messagebox
import fitz 
import sqlite3
import tempfile
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import customtkinter as ctk

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
class SaidaPorGrupo(ctk.CTkToplevel):
    def __init__(self, db_file):
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.title("Zerar Estoque por Grupo")
        self.geometry("500x300")
        self.resizable(width=False, height=False)

        self.frame_1 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_1.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.group_label = ctk.CTkLabel(self.frame_1, text="Selecione o Grupo:", text_color="black")
        self.group_label.pack()

        self.group_var = ctk.StringVar(self.frame_1)
        self.group_var.set("")  # Valor inicial

        self.group_menu = ttk.OptionMenu(self.frame_1, self.group_var, "")
        self.group_menu.pack()

        self.porcentagem_label = ctk.CTkLabel(self.frame_1, text="Porcentagem de Saída (%):", text_color="black")
        self.porcentagem_label.pack()

        self.porcentagem_entry = ctk.CTkEntry(self.frame_1, fg_color="#FFFFFF", text_color="black")
        self.porcentagem_entry.pack()

        self.data_label = ctk.CTkLabel(self.frame_1, text="Data da Saída:", text_color="black")
        self.data_label.pack()

        self.data_entry = CustomEntry(self.frame_1, fg_color="#FFFFFF", text_color="black")
        self.data_entry.pack()

        self.zerar_button = ctk.CTkButton(self.frame_1, text="Zerar Estoque", command=self.zerar_estoque)
        self.zerar_button.place(relwidth = 0.2, relheight = 0.1, relx = 0.3, rely= 0.7)

        self.saida_button = ctk.CTkButton(self.frame_1, text="Registrar Saída", command=self.registrar_saida)
        self.saida_button.place(relwidth = 0.2, relheight = 0.1, relx = 0.6, rely= 0.7)

        self.conn = sqlite3.connect("db/db_file.db")
        self.c = self.conn.cursor()

        self.carregar_grupos()

    def carregar_grupos(self):
        self.c.execute("SELECT nome FROM grupo")
        grupos = self.c.fetchall()
        for grupo in grupos:
            self.group_menu['menu'].add_command(label=grupo[0], command=tk._setit(self.group_var, grupo[0]))

    def zerar_estoque(self):
        grupo_selecionado = self.group_var.get()
        if grupo_selecionado:
            # Mostrar caixa de diálogo de confirmação
            confirmacao = messagebox.askyesno("Confirmar", f"Deseja realmente zerar o estoque do grupo {grupo_selecionado}?")
            if confirmacao:  # Se o usuário clicar em "Sim"
                self.c.execute("UPDATE produtos SET quantidade_estoque = 0 WHERE grupo = ?", (grupo_selecionado,))
                self.conn.commit()
                messagebox.showinfo("Sucesso", f"Estoque do grupo {grupo_selecionado} zerado.")
            else:
                messagebox.showinfo("Cancelado", "Operação cancelada.")
        else:
            messagebox.showerror("Erro", "Nenhum grupo selecionado.")

    def registrar_saida(self):
        grupo_selecionado = self.group_var.get()
        porcentagem_saida_str = self.porcentagem_entry.get()
        data_saida = self.data_entry.get()

        # Tenta converter a porcentagem de saída para um número float
        try:
            porcentagem_saida = float(porcentagem_saida_str) / 100
        except ValueError:
            messagebox.showerror("Erro", "Porcentagem de saída inválida.")
            return

        # Exibe uma caixa de diálogo de confirmação
        confirmacao = messagebox.askyesno("Confirmar", f"Deseja realmente dar saída em {porcentagem_saida_str}% do grupo {grupo_selecionado}?")
        
        if confirmacao and grupo_selecionado and porcentagem_saida is not None and data_saida:
            try:
                # Seleciona todos os produtos do grupo selecionado
                self.c.execute("SELECT * FROM produtos WHERE grupo = ?", (grupo_selecionado,))
                produtos_grupo = self.c.fetchall()

                # Itera sobre todos os produtos do grupo
                for produto in produtos_grupo:
                    id_produto, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo = produto
                    if quantidade_estoque > 0:
                        # Calcula a quantidade de saída
                        quantidade_saida = float(quantidade_estoque) * porcentagem_saida

                        # Insere o registro de movimentação
                        self.c.execute("INSERT INTO movimentacoes (nome_item, codigo_barras, valor_movimento, quantidade_movimento, tipo_movimento, data_movimento, grupo_movimento, sub_grupo_movimento) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                        (nome, codigo_barras, preco_unitario, quantidade_saida, 'saida', data_saida, grupo, sub_grupo))
                        self.conn.commit()

                        # Atualiza a quantidade de estoque
                        self.c.execute("UPDATE produtos SET quantidade_estoque = ? WHERE nome = ?",
                                        (quantidade_estoque - quantidade_saida, nome))
                        self.conn.commit()

                messagebox.showinfo("Sucesso", f"Saída de produtos do grupo {grupo_selecionado} registrada com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao registrar saída de produtos: {e}")
        else:
            messagebox.showinfo("Cancelado", "Operação cancelada.")
            
       

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    conn = "db/db_file.db"
    app = SaidaPorGrupo(conn)
    app.mainloop()
