import os
import sqlite3
from tkinter import messagebox
from typing import Tuple
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from edicao import TelaEdicaoItem
from tkinter import filedialog
import xml.etree.ElementTree as ET
from datetime import datetime
import threading
from assets.icons import carregar_imagens
from views.janela_visualizar_xml import JanelaVisualizarNfe
from db.database import SistemaEstoque
from views.janela_detalhes_xml import JanelaDetalhesXml


class Produto:
    def __init__(self, id, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo):
        self.id = id
        self.nome = nome
        self.codigo_barras = codigo_barras
        self.preco_unitario = preco_unitario
        self.quantidade_estoque = quantidade_estoque
        self.grupo = grupo
        self.sub_grupo = sub_grupo

    
class JanelaXml(ctk.CTkToplevel):
    def __init__(self, db_file):  # Adicione db_file como argumento
        super().__init__()
        self.icons = carregar_imagens()
        self.icon_arquivos = self.icons["lista_arquivos"]
        self.janela_visualizar_xml = None  # Inicialize com None
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)  # Passe db_file aqui
        self.title("Entrada com XML")
        # Obtendo as dimensões da tela
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        largura_janela = largura_tela * 0.7  # 71.5% da largura da tela
        altura_janela = altura_tela * 0.6  # 85.7% da altura da tela
        x_pos = largura_tela * 0.005  # Posição horizontal (0% da largura da tela)
        y_pos = altura_tela * 0.27  # Posição vertical (14.5% da altura da tela)
        self.geometry(f"{int(largura_janela)}x{int(altura_janela)}+{int(x_pos)}+{int(y_pos)}")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.resizable(width=False, height=False) 
        
        #Adicionando Frames
        self.frame_xml1 = ctk.CTkFrame(self, fg_color="#87BA5A")
        self.frame_xml1.place(relwidth= 1, relheight= 0.15, relx=0, rely=0)
        self.frame_xml2 = ctk.CTkFrame(self, fg_color="#F6F6F6")
        self.frame_xml2.place(relwidth=1, relheight= 0.15, relx=0, rely=0.15)
        self.frame_xml3 = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.frame_xml3.place(relwidth=1, relheight= 0.7, relx=0, rely=0.30)
        
        self.font = ctk.CTkFont(family="Arial",weight="bold", size=48 )
        
        #Adicionando Label
        self.label_xml1 = ctk.CTkLabel(self.frame_xml1, text="ENTRADA DE ITENS POR XML", text_color="#252A3F", font=self.font)
        self.label_xml1.pack(pady=15)

        #Adicionando botões
        self.btn_entrada_xml = ctk.CTkButton(self.frame_xml2, text="Selecionar XML", text_color="black", fg_color="#FFFFFF", hover_color="#F6F6F6", command=self.extrair_dados_xml)
        self.btn_entrada_xml.place(relx=0.01, rely=0.35)
        self.btn_salvar_xml = ctk.CTkButton(self.frame_xml2, text="Salvar", width=100, text_color="black", fg_color="#FFFFFF", hover_color="#F6F6F6", command=self.salvar_no_banco)
        self.btn_salvar_xml.place(relx=0.2, rely=0.35)
        self.btn_arquivos = ctk.CTkButton(self.frame_xml2, text="Visualizar", width=80, image=self.icon_arquivos, text_color="black", fg_color="#FFFFFF", hover_color="#F6F6F6", command=self.abrir_janela_visualizar_xml)
        self.btn_arquivos.place(relx=0.8, rely=0.35)
        
        
        #Adicionando treeview
        self.tree_xml = ttk.Treeview(self.frame_xml3, columns=("Descrição", "Código de Barras", "Preço Unitario", "Quantidade"),show="headings", height=20)
        self.tree_xml.heading("Descrição", text="Descrição")
        self.tree_xml.heading("Código de Barras", text="Código de Barras")
        self.tree_xml.heading("Preço Unitario", text="Valor")
        self.tree_xml.heading("Quantidade", text="Quantidade")
        self.tree_xml.column("Descrição", width=400)
        self.tree_xml.column("Código de Barras", width=150, anchor= tk.CENTER)
        self.tree_xml.column("Preço Unitario", width=100, anchor= tk.CENTER)
        self.tree_xml.column("Quantidade", width=150, anchor= tk.CENTER)
        self.tree_xml.grid(row=0, column=0, sticky="nsew")
        # Criando a barra de rolagem saida
        self.scroll_bar = ctk.CTkScrollbar(self.frame_xml3, orientation="vertical", command=self.tree_xml.yview, bg_color="#FFFFFF")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        # Configurando a barra de rolagem para o Treeview saida
        self.tree_xml.configure(yscrollcommand=self.scroll_bar.set)
        # Configurando pesos das colunas e linhas para expandir conforme o tamanho do frame
        self.frame_xml3.grid_rowconfigure(0, weight=1)
        self.frame_xml3.grid_columnconfigure(0, weight=1)
        
      
        


    def abrir_janela_visualizar_xml(self):
        # Verifique se a janela já existe. Se não, crie uma nova instância.
        if self.janela_visualizar_xml is None or not self.janela_visualizar_xml.winfo_exists():
            self.janela_visualizar_xml = JanelaVisualizarNfe()
            self.janela_visualizar_xml.grab_set()
            self.janela_visualizar_xml.deiconify()  # Agora você pode mostrar a janela
        else:
            # Se já existir, apenas a mostre
            self.janela_visualizar_xml.deiconify()

    def fechar_janela_visualizar_xml(self):
        if self.janela_visualizar_xml is not None:
            self.janela_visualizar_xml.destroy()  # Destrua a janela quando fechada
            self.janela_visualizar_xml = None  # Defina como None para permitir a criação novamente
        

    

    def extrair_dados_xml(self):
        self.arquivo_nome = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
        self.focus_force()
        if self.arquivo_nome:
            tree = ET.parse(self.arquivo_nome)
            root = tree.getroot()
            namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

            # Limpar dados anteriores da treeview
            for item in self.tree_xml.get_children():
                self.tree_xml.delete(item)

            # Iterar sobre cada elemento "det" (detalhe do produto)
            for det in root.findall('.//nfe:det', namespace):
                # Extrair detalhes do produto
                prod = det.find('nfe:prod', namespace)
                cEAN = prod.find('nfe:cEAN', namespace).text
                xProd = prod.find('nfe:xProd', namespace).text
                qCom = prod.find('nfe:qCom', namespace).text
                vUnCom = prod.find('nfe:vUnCom', namespace).text

                # Adicionar os dados à treeview
                qCom_arredondado = round(float(qCom), 3)

                # Convertendo de volta para string (se necessário)
                qCom_formatado = str(qCom_arredondado)
                print(qCom_formatado)
                self.tree_xml.insert('', 'end', values=(xProd, cEAN, vUnCom, qCom_formatado))
        return self.arquivo_nome


    def salvar_no_banco(self):
        items_novos = []
        items_atualizados = []

        for child in self.tree_xml.get_children():
            nome, codigo_barras, preco_unitario, quantidade = self.tree_xml.item(child)['values']
            
            # Verificar se o produto já existe e o tipo de operação (novo ou atualizar)
            tipo, produto = self.sistema_estoque.verificar_produto(nome, codigo_barras)
            
            if tipo == "atualizar":
                # Caso seja para atualizar, pegamos os dados do produto
                nome, codigo_barras, preco_nota, quantidade = self.tree_xml.item(child)['values']
                preco_unitario = preco_nota
                grupo = produto[2]
          
                sub_grupo = produto[3]
         
                items_atualizados.append((nome, codigo_barras, preco_unitario, quantidade, grupo, sub_grupo))
            
            elif tipo == "novo":
                # Caso seja um produto novo, adicionamos os dados
                if codigo_barras == "SEM GTIN":
                    items_novos.append((nome, codigo_barras, preco_unitario, quantidade, "--NAO-DEFINIDO--", "--NAO-DEFINIDO--"))
                elif str(codigo_barras).startswith("2") and len(str(codigo_barras)) == 13:
                    codigo_item = "2" + str(codigo_barras)[6:12]
                    items_novos.append((nome, codigo_item, preco_unitario, quantidade, "--NAO-DEFINIDO--", "--NAO-DEFINIDO--"))
                else:
                    items_novos.append((nome, codigo_barras, preco_unitario, quantidade, "--NAO-DEFINIDO--", "--NAO-DEFINIDO--"))
        
        
        
        self.janela_detalhes = JanelaDetalhesXml(self.arquivo_nome)
        # Após o loop, todos os itens foram verificados, então agora mostramos os detalhes
        self.janela_detalhes.mostrar_detalhes(items_novos, items_atualizados)























    
    
    def fechar_janela(self):
        self.destroy()  # Destruindo a janela secundária
if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = JanelaXml(db_file)  # Passar root e db_file como argumentos
    app.mainloop()