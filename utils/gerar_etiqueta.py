import os
import sqlite3
import tkinter as tk
from tkinter import ttk
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import ImageDraw, ImageFont
from assets.icons import carregar_imagens
from controllers.interface import adicionar_produto_code_bar
from tkinter import messagebox
from utils.utils import format_number
from db.database import SistemaEstoque
import win32print, win32ui
from PIL import ImageWin

from PIL import ImageFont, ImageDraw, Image
import barcode
from barcode.writer import ImageWriter
import time


class GeradorEtiqueta:
    def __init__(self, sistema_estoque, treeview, etiqueta_label, entry_peso):
        self.sistema_estoque = sistema_estoque
        self.treeview = treeview
        self.etiqueta_label = etiqueta_label
        self.entry_peso = entry_peso

    def gerar_etiqueta(self, full_code, nome_produto, peso_produto, valor_produto):
        # Definir o DPI para 300 (alta resolução)
        nome_produto_formatado = nome_produto[:25]
        dpi = 203
        largura = int(10 * dpi / 2.54)  # 10 cm convertidos para pixels
        altura = int(5 * dpi / 2.54)    # 5 cm convertidos para pixels

        etiqueta = Image.new('RGB', (largura, altura), color=(255, 255, 255))  # Fundo branco
        draw = ImageDraw.Draw(etiqueta)

        # Carregar fontes com melhor qualidade (caso disponível)
        try:
            font_regular = ImageFont.truetype("arialbd.ttf", 28)
            font_bold = ImageFont.truetype("arialbd.ttf", 30)
            font_header = ImageFont.truetype("arialbd.ttf", 24)
            font_total_header = ImageFont.truetype("arialbd.ttf", 30)
            font_total_value = ImageFont.truetype("arialbd.ttf", 40)
        except IOError:
            font_regular = ImageFont.load_default()
            font_bold = ImageFont.load_default()
            font_header = ImageFont.load_default()
            font_total_header = ImageFont.load_default()
            font_total_value = ImageFont.load_default()

        # Desenha a etiqueta
        draw.rectangle([22, 8, largura - 8, altura - 8], outline="black", width=2)
        draw.text((30, 10), "Etiqueta de Produto", font=font_header, fill="black")

        espacamento = 40
        draw.line([22, espacamento, largura - 10, espacamento], fill="black", width=2)
        espacamento += 10
        draw.text((30, espacamento + 30), f"{nome_produto_formatado}", font=font_bold, fill="black")
        espacamento += 30
        draw.text((30, espacamento + 150), f"Peso: {peso_produto} kg", font=font_regular, fill="black")
        espacamento += 30

        draw.text((30, espacamento + 170), f"Valor kg: R${valor_produto:.2f}", font=font_regular, fill="black")
        
        espacamento += 50


        draw.line([22, espacamento, largura - 10, espacamento], fill="black", width=2)
        draw.line([300,  espacamento, 300, espacamento + 228], fill="black", width=2)


        valor_total = peso_produto * valor_produto
        espacamento += 20
        retangulo_y = 20
        draw.rectangle([600, retangulo_y, 780, retangulo_y + 40], fill="black")
        draw.text((600 + 10, retangulo_y + 5), f"TOTAL R$: ", font=font_total_header, fill="white")

        espacamento += 40
        draw.text((600, 80), f"{valor_total:.2f}", font=font_total_value, fill="black")

        # Gerar o código de barras
        code128 = barcode.get_barcode_class('code128')
        barcode_image = code128(full_code, writer=ImageWriter())

        # Caminho absoluto para salvar o código de barras (sem a extensão .png duplicada)
        caminho_barras = os.path.join(os.getcwd(), 'codigo_de_barras')  # Retira a extensão aqui
        
        # Ajuste a opção de largura do módulo do código de barras
        barcode_image.default_writer_options['module_width'] = 0.2
        barcode_image.default_writer_options['module_height'] = 10
        barcode_image.default_writer_options['font_size'] = 8
        barcode_image.default_writer_options['text_distance'] = 5
        barcode_image.default_writer_options['quiet_zone'] = 10

        # Tente salvar o código de barras com a extensão .png
        try:
            barcode_image.save(caminho_barras)  # O código de barras agora será salvo como codigo_de_barras.png
            print(f"Arquivo de código de barras salvo em: {caminho_barras}.png")
        except Exception as e:
            print(f"Erro ao salvar o código de barras: {e}")
            return None

        # Verificar se o arquivo foi realmente salvo
        caminho_barras_completo = caminho_barras + ".png"
        if not os.path.exists(caminho_barras_completo):
            print(f"Erro: o arquivo {caminho_barras_completo} não foi encontrado.")
            return None

        # Abrir a imagem do código de barras
        try:
            img_barcode = Image.open(caminho_barras_completo)
            #img_barcode = img_barcode.resize((largura - 200, 150))  # Ajuste do código de barras
        except Exception as e:
            print(f"Erro ao abrir a imagem do código de barras: {e}")
            return None

        posicao_barcode = (350, 170)  
        etiqueta.paste(img_barcode, posicao_barcode)

        

        # Caminho para salvar a etiqueta final
        caminho_imagem = 'etiqueta_produto_10x5.png'
        etiqueta.save(caminho_imagem, format='PNG')

        print("Etiqueta gerada com sucesso!")
        return caminho_imagem

    def imprimir_etiqueta(self, caminho_imagem):
        """Função para imprimir a etiqueta gerada diretamente para a impressora L42 Pro utilizando EPL."""
        try:
            # Carregar a imagem
            imagem = Image.open(caminho_imagem)

            # Obter o contexto da impressora
            printer_name = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_name)
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)

            # Definir o DPI da impressora (203 DPI, compatível com a L42 Pro)
            dpi = 203  # Resolução da impressora L42 Pro

            # Obter o tamanho da imagem original
            largura_imagem, altura_imagem = imagem.size

            # Calcular a largura e altura da página para a impressora
            largura_pagina = int(10 * dpi / 2.54)  # 10 cm convertidos para pixels
            altura_pagina = int(5 * dpi / 2.54)   # 5 cm convertidos para pixels

            # Iniciar o processo de impressão
            hdc.StartDoc("Etiqueta")
            hdc.StartPage()

            # Calcular as margens para centralizar a imagem na página
            x_offset = (largura_pagina - largura_imagem) // 2
            y_offset = (altura_pagina - altura_imagem) // 2

            # Desenhar a imagem original (sem redimensionamento) centralizada na página
            hbitmap = ImageWin.Dib(imagem)
            hbitmap.draw(hdc.GetHandleOutput(), (x_offset, y_offset, x_offset + largura_imagem, y_offset + altura_imagem))

            # Finalizar a impressão
            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()

            print(f"Etiqueta enviada para a impressora {printer_name}.")
        
        except Exception as e:
            print(f"Erro ao imprimir a etiqueta: {e}")


    def generate_barcode(self):
        """Função para gerar o código de barras e exibir a etiqueta na interface."""
        selected_item = self.treeview.selection()
        
        if selected_item:
            produto = self.treeview.item(selected_item[0], "values")[1]
            codigo_barras = self.treeview.item(selected_item[0], "values")[2]
            peso = self.entry_peso.get()

            if peso:
                try:
                    self.sistema_estoque.c.execute("SELECT preco_unitario FROM produtos WHERE codigo_barras=?", (codigo_barras,))
                    valor_kg = self.sistema_estoque.c.fetchone()
                    
                    if not valor_kg:
                        raise ValueError("Produto não encontrado no banco de dados.")
                    
                    valor_kg = valor_kg[0]  # Preço por kg do produto
                    peso_float = float(peso)
                    
                    if peso_float <= 0:
                        raise ValueError("Peso inválido! O peso deve ser um valor positivo.")
                    
                    peso_codigo = format_number(peso_float)
                    full_code = f"{codigo_barras}{peso_codigo}"
                    print(full_code)

                    caminho_imagem = self.gerar_etiqueta(full_code, produto, peso_float, valor_kg)

                    if caminho_imagem:
                        etiqueta_image = Image.open(caminho_imagem)
                        ctk_photo = CTkImage(etiqueta_image, size=(300, 100))
                        self.etiqueta_label.configure(image=ctk_photo)
                        self.etiqueta_label.image = ctk_photo
                        return caminho_imagem

                        # Chamar a função de impressão após gerar a etiqueta
                        #self.imprimir_etiqueta(caminho_imagem)

                except ValueError as ve:
                    messagebox.showerror("Erro", str(ve))
                except Exception as e:
                    messagebox.showerror("Erro inesperado", f"Ocorreu um erro inesperado: {str(e)}")
            else:
                messagebox.showerror("Erro", "Por favor, insira o peso.")
                self.etiqueta_label.config(text="Por favor, insira o peso.", fg="red")
        else:
            messagebox.showerror("Erro", "Por favor, selecione um produto.")
            self.etiqueta_label.config(text="Por favor, selecione um produto.", fg="red")
    