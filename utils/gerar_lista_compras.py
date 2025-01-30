import os
import tempfile
import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image
from fitz import open as fitz_open
import customtkinter as ctk

class GerarListaCompras:
    def __init__(self, connection):
        self.c = connection.cursor()

    def mm2p(self, milimetros):
        """Converte milímetros para pontos (p)"""
        return milimetros / 0.352777

    def listar_grupos_e_subgrupos(self, cnv, y_start, y_step, current_page, grupo):
        """Função para listar os grupos e subgrupos no PDF"""
        rect_y = y_start
        rect_height = self.mm2p(6)
        cnv.setFillColor(colors.lightgrey)
        cnv.rect(self.mm2p(7), rect_y, self.mm2p(196), rect_height, fill=1, stroke=1)
        
        # Desenho das linhas da tabela
        for coluna in range(1):
            x_pos = self.mm2p(20 + coluna * 50)
            cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
        for coluna in range(1):
            x_pos = self.mm2p(140 + coluna * 50)
            cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
        for coluna in range(1):
            x_pos = self.mm2p(160 + coluna * 50)
            cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
        for coluna in range(1):
            x_pos = self.mm2p(180 + coluna * 50)
            cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)

        cnv.setFillColor(colors.black)
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(self.mm2p(60), y_start + 3, grupo)
        cnv.setFont("Helvetica-Bold", 9)
        cnv.drawString(self.mm2p(144), y_start + 3, "Estoque")
        cnv.drawString(self.mm2p(161), y_start + 3, "Quantidade")
        cnv.drawString(self.mm2p(185), y_start + 3, "Comprar")

        # Consulta para obter os subgrupos
        self.c.execute("SELECT sub_grupo, SUM(quantidade_estoque) FROM produtos WHERE grupo = ? AND sub_grupo != '--NAO-DEFINIDO--' GROUP BY sub_grupo", (grupo,))
        subgrupos = self.c.fetchall()

        # Desenhar subgrupos
        rect_height = self.mm2p(6)
        subgrupo_index = 1
        for subgrupo, total_quantidade in subgrupos:
            quantidade = f"{round(total_quantidade, 3):.3f}".rstrip("0").rstrip(".").replace('.', ',')
            y_start -= y_step  # Ajuste a posição vertical para o próximo item

            # Verifica se é necessário mudar de página
            if y_start < self.mm2p(10):
                cnv.showPage()
                cnv.setFont("Helvetica", 9)
                cnv.drawString(self.mm2p(180), self.mm2p(5), f"Pagina:{cnv.getPageNumber()}")
                y_start = self.mm2p(280)

            # Desenha os itens do subgrupo
            rect_y = y_start
            cnv.rect(self.mm2p(7), rect_y, self.mm2p(196), rect_height, fill=0)

            # Desenhando colunas
            for coluna in range(1):
                x_pos = self.mm2p(20 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
            for coluna in range(1):
                x_pos = self.mm2p(140 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
            for coluna in range(1):
                x_pos = self.mm2p(160 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
            for coluna in range(1):
                x_pos = self.mm2p(180 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)

            # Escrevendo o subgrupo e a quantidade
            cnv.setFont("Helvetica", 9)
            cnv.drawString(self.mm2p(12), rect_y + 4, f"{subgrupo_index}")
            subgrupo_index += 1
            cnv.drawString(self.mm2p(25), rect_y + 4, subgrupo)
            cnv.drawString(self.mm2p(145), rect_y + 4, quantidade)

        return y_start - y_step  # Retorna a posição para o próximo grupo

    def gerar_lista_compras_pdf(self):
        """Função principal para gerar o PDF da lista de compras"""
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, "lista_de_compras.pdf")
        cnv = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        margin = 50
        line_height = 20
        max_lines_per_page = math.floor((height - 2 * margin) / line_height)
        
        # Cabeçalho
        cnv.setFont("Helvetica-Bold", 16)
        cnv.drawString(self.mm2p(75), self.mm2p(282), "NEW PALACE EVENTOS")
        cnv.drawString(self.mm2p(75), self.mm2p(235), "LISTA DE COMPRAS")
        cnv.setFont("Helvetica", 12)
        cnv.drawString(self.mm2p(10), self.mm2p(265), "EVENTOS:")
        cnv.drawString(self.mm2p(10), self.mm2p(255), "DATA:")
        cnv.drawString(self.mm2p(10), self.mm2p(245), "QUANTIDADE DE PESSOAS:")

        # Consultar os grupos
        y_start = self.mm2p(220)  # Posição inicial para desenhar os itens
        self.c.execute("SELECT DISTINCT grupo FROM produtos WHERE grupo != '--NAO-DEFINIDO--'")
        grupos = self.c.fetchall()

        current_page = 1
        for grupo in grupos:
            grupo_nome = grupo[0]
            y_start = self.listar_grupos_e_subgrupos(cnv, y_start, self.mm2p(6), current_page, grupo_nome)

            # Verifica se é necessário uma nova página
            if y_start < self.mm2p(10):
                cnv.showPage()
                cnv.setFont("Helvetica", 9)
                current_page += 1
                cnv.drawString(self.mm2p(180), self.mm2p(5), f"Pagina:{current_page}")
                y_start = self.mm2p(280)

        cnv.save()

        # Depois de gerar o PDF, abrir o visualizador
        return pdf_path
