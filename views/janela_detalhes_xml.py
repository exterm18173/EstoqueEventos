import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
import threading
from datetime import datetime
from tkinter import messagebox
from db.database import SistemaEstoque
import time
from controllers.salvar_xml_controller import extrair_salvar_nfe

class JanelaDetalhesXml:
    def __init__(self, arquivo_nome):
        print(arquivo_nome)
        self.sistema_estoque = SistemaEstoque
        self.aquivo_nome = arquivo_nome
        print(self.aquivo_nome)
    def mostrar_detalhes(self, items_novos, items_atualizados):
        self.items_novos = items_novos
        self.items_atualizados = items_atualizados
        self.details_window = ctk.CTkToplevel()
        self.details_window.title("Detalhes dos Itens")
        self.details_window.geometry("950x600+80+215")
        self.details_window.grab_set()

        # Adicionando Frames
        self.frame_salvar_xml1 = ctk.CTkFrame(self.details_window, fg_color="#87BA5A")
        self.frame_salvar_xml1.place(relwidth= 1, relheight = 0.1, x=0, y=0)
        self.frame_salvar_xml2 = ctk.CTkFrame(self.details_window, fg_color="#FFFFFF")
        self.frame_salvar_xml2.place(relwidth= 1, relheight = 0.35, x=0, y=60)
        self.frame_salvar_xml3 = ctk.CTkFrame(self.details_window, fg_color="#87BA5A")
        self.frame_salvar_xml3.place(relwidth= 1, relheight = 0.1, x=0, y=270)
        self.frame_salvar_xml4 = ctk.CTkFrame(self.details_window, fg_color="#FFFFFF")
        self.frame_salvar_xml4.place(relwidth= 1, relheight = 0.35, x=0, y=330)
        self.frame_salvar_xml5 = ctk.CTkFrame(self.details_window, fg_color="#87BA5A")
        self.frame_salvar_xml5.place(relwidth= 1, relheight = 0.1, x=0, y=540)

        self.label_salvar_xml1 = ctk.CTkLabel(self.frame_salvar_xml1, text="Novos itens que serão adicionados ao estoque", text_color="#252A3F", font=("Arial", 22))
        self.label_salvar_xml1.pack(pady=15)
        self.label_salvar_xml2 = ctk.CTkLabel(self.frame_salvar_xml3, text="Itens já existem no estoque(Atualizar a quantidade de estoque)", text_color="#252A3F", font=("Arial", 22))
        self.label_salvar_xml2.pack(pady=15)

        # Adicionando treeview
        self.treeview_novos = ttk.Treeview(self.frame_salvar_xml2, columns=("Nome", "Código de Barras", "Preço Unitario", "Quantidade", "grupo", "sub_grupo"), show="headings", height=20)
        self.treeview_novos.heading("Nome", text="Nome")
        self.treeview_novos.heading("Código de Barras", text="Código de Barras")
        self.treeview_novos.heading("Preço Unitario", text="Valor")
        self.treeview_novos.heading("Quantidade", text="Quantidade")
        self.treeview_novos.heading("grupo", text="Grupo")
        self.treeview_novos.heading("sub_grupo", text="Sub-Grupo")
        self.treeview_novos.column("Nome", width=400)
        self.treeview_novos.column("Código de Barras", width=150, anchor=tk.CENTER)
        self.treeview_novos.column("Preço Unitario", width=100, anchor=tk.CENTER)
        self.treeview_novos.column("Quantidade", width=150, anchor=tk.CENTER)
        self.treeview_novos.column("grupo", width=150, anchor=tk.CENTER)
        self.treeview_novos.column("sub_grupo", width=150, anchor=tk.CENTER)
        self.treeview_novos.grid(row=0, column=0, sticky="nsew")
        #self.treeview_novos.bind("<ButtonRelease-1>", self.on_treeview_click)

        # Barra de rolagem
        self.scroll_bar = ctk.CTkScrollbar(self.frame_salvar_xml2, orientation="vertical", command=self.treeview_novos.yview, bg_color="#FFFFFF")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        self.treeview_novos.configure(yscrollcommand=self.scroll_bar.set)

        # Configuração das linhas e colunas para expandir conforme o tamanho do frame
        self.frame_salvar_xml2.grid_rowconfigure(0, weight=1)
        self.frame_salvar_xml2.grid_columnconfigure(0, weight=1)

        # Criando combobox
        self.combobox = ttk.Combobox(self.frame_salvar_xml2, state="readonly")
        self.combobox.place_forget()

        # Treeview para itens atualizados
        self.tree_atualizados = ttk.Treeview(self.frame_salvar_xml4, columns=("Nome", "Código de Barras", "Preço Unitario", "Quantidade", "grupo", "sub_grupo"), show="headings", height=20)
        self.tree_atualizados.heading("Nome", text="Nome")
        self.tree_atualizados.heading("Código de Barras", text="Código de Barras")
        self.tree_atualizados.heading("Preço Unitario", text="Valor")
        self.tree_atualizados.heading("Quantidade", text="Quantidade")
        self.tree_atualizados.heading("grupo", text="Grupo")
        self.tree_atualizados.heading("sub_grupo", text="Sub-Grupo")
        self.tree_atualizados.column("Nome", width=400)
        self.tree_atualizados.column("Código de Barras", width=150, anchor=tk.CENTER)
        self.tree_atualizados.column("Preço Unitario", width=100, anchor=tk.CENTER)
        self.tree_atualizados.column("Quantidade", width=150, anchor=tk.CENTER)
        self.tree_atualizados.column("grupo", width=150, anchor=tk.CENTER)
        self.tree_atualizados.column("sub_grupo", width=150, anchor=tk.CENTER)
        self.tree_atualizados.grid(row=0, column=0, sticky="nsew")

        # Barra de rolagem para o Treeview
        self.scroll_bar = ctk.CTkScrollbar(self.frame_salvar_xml4, orientation="vertical", command=self.tree_atualizados.yview, bg_color="#FFFFFF")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        self.tree_atualizados.configure(yscrollcommand=self.scroll_bar.set)

        # Preencher Treeview de Novos Itens
        for item in items_novos:
            self.treeview_novos.insert('', 'end', values=item)

        # Preencher Treeview de Itens Atualizados
        for item in items_atualizados:
            self.tree_atualizados.insert('', 'end', values=item)

        # Botão para confirmar e salvar
        self.btn_salvar = ctk.CTkButton(self.frame_salvar_xml5, text="Confirmar e Salvar", fg_color="#252A3F", command=lambda:self.confirmar_salvar(self.aquivo_nome))
        self.btn_salvar.place(x=800, y=20)

        self.conn = sqlite3.connect("db/db_file.db")
        self.c = self.conn.cursor()
        self.carregar_grupos()

    def carregar_grupos(self):
        # Carregar grupos do banco de dados
        self.c.execute("SELECT nome FROM grupo")
        grupos = self.c.fetchall()
        grupos = [grupo[0] for grupo in grupos]
        self.combobox_values = grupos
        self.combobox.config(values=self.combobox_values)

    def on_treeview_click(self, event):
        item_id = self.treeview_novos.identify_row(event.y)
        if not item_id:
            return
        column_id = self.treeview_novos.identify_column(event.x)
        if column_id != "#5":
            return

        column = int(column_id[1:]) - 1
        x, y, width, height = self.treeview_novos.bbox(item_id, column)
        self.combobox.place(x=x, y=y, width=width, height=height)
        self.combobox.focus_set()
        self.combobox.bind("<<ComboboxSelected>>", lambda e: self.on_combobox_select(item_id))

    def atualizar_lista(self, selected_value, item_id):
        # Atualizar valores na Treeview
        for child in self.treeview_novos.get_children():
            if self.treeview_novos.item(child)['values'][0] == item_id:
                item_values = list(self.treeview_novos.item(child)['values'])
                item_values[4] = selected_value
                self.treeview_novos.item(child, values=tuple(item_values))
                break
        for i, item in enumerate(self.items_novos):
            if item[0] == item_id:
                self.items_novos[i] = list(item)
                self.items_novos[i][4] = selected_value
                self.items_novos[i] = tuple(self.items_novos[i])
                break

    def on_combobox_select(self, event):
        selected_value = self.combobox.get()
        item_id = self.treeview_novos.item(self.treeview_novos.focus())['values'][0]
        self.atualizar_lista(selected_value, item_id)
        self.combobox.place_forget()



    def confirmar_salvar(self, arquivo_nome):
        print(arquivo_nome)
        extrair_salvar_nfe(arquivo_nome)
        self.loading_window = ctk.CTkToplevel(self.details_window)
        self.loading_window.title("Carregando...")
        self.loading_window.geometry("300x120+400+300")
        self.loading_window.grab_set()

        self.progressbar = ctk.CTkProgressBar(self.loading_window, mode="determinate")
        self.progressbar.pack(padx=20, pady=30)

        self.label_status = ctk.CTkLabel(self.loading_window, text="Salvando itens. Por favor, aguarde...")
        self.label_status.pack(padx=20, pady=(0, 30))

        threading.Thread(target=self.processar_itens).start()

    def processar_itens(self):
        try:
            total_items = len(self.items_novos) + len(self.items_atualizados)
            progresso = 0

            # Processar itens novos
            for item in self.items_novos:
                
                # Verificar se o item tem 6 elementos
                if len(item) != 6:
                    raise ValueError(f"Item inválido: {item}. Esperado 6 elementos.")
                
                self.sistema_estoque.adicionar_atualizar_produto(self.sistema_estoque, *item)
                
                self.salvar_movimentacao(*item, "entrada")
                progresso += 1
                if progresso % (total_items // 1) == 0:
                    self.atualizar_progresso(progresso, total_items)

            for item in self.items_atualizados:

                
                # Verificar se o item tem 6 elementos
                if len(item) != 6:
                    raise ValueError(f"Item inválido: {item}. Esperado 6 elementos.")
                    
                self.sistema_estoque.adicionar_atualizar_produto(self.sistema_estoque, *item)
                
                self.salvar_movimentacao(*item, "entrada")
                progresso += 1
                if progresso % (total_items // 1) == 0:
                    self.atualizar_progresso(progresso, total_items)

            self.atualizar_progresso(total_items, total_items)
            self.limpar_treeviews()
            time.sleep(1)
            self.details_window.destroy()

            messagebox.showinfo("Sucesso", "Os itens foram salvos com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os itens: {str(e)}")
        finally:
            
            self.loading_window.destroy()


    def atualizar_progresso(self, progresso, total_items):
        percentual = int((progresso / total_items) * 100)
        self.progressbar.set(percentual)

    def limpar_treeviews(self):
        for child in self.treeview_novos.get_children():
            self.treeview_novos.delete(child)
        for child in self.tree_atualizados.get_children():
            self.tree_atualizados.delete(child)

    def salvar_movimentacao(self, nome_item, codigo_barras, preco_unitario, quantidade, tipo_movimento, grupo, sub_grupo):
        conn = sqlite3.connect('db/db_file.db')
        c = conn.cursor()
        data_atual = datetime.now().strftime("%d/%m/%Y")
        c.execute('''INSERT INTO movimentacoes (nome_item, codigo_barras, valor_movimento, quantidade_movimento, grupo_movimento, data_movimento, sub_grupo_movimento, tipo_movimento, cliente_movimento)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (nome_item, codigo_barras, preco_unitario, quantidade, tipo_movimento, data_atual, grupo, sub_grupo, 'NEW PALACE EVENTOS'))
        conn.commit()
        conn.close()
 

    