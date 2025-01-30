from datetime import datetime
import os
import math
import platform
import re
import subprocess
import fitz 
import sqlite3
import tempfile
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import Calendar
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import win32print
import win32ui
import win32api
from babel.numbers import format_currency


class Grupo:
    def __init__(self, nome):
        self.nome = nome
class SubGrupo:
    def __init__(self, subnome):
        self.subnome = subnome
        
class SistemaEstoque:
    def __init__(self, db_file, parent=None):
        self.parent = parent
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
    def __del__(self):
        self.conn.close()
    

    def gerar_relatorio_estoque_pdf(self, grupo=None):
        def mm2p(milimetros):
            return milimetros / 0.352777

        def listar_produtos(cnv, y_start, y_step, grupo):
            # Escreve o nome do grupo
            rect_y = y_start
            rect_height = mm2p(6)
            cnv.setFillColor(colors.lightgrey)
            cnv.rect(mm2p(7), rect_y, mm2p(196), rect_height, fill=1, stroke=1)

            cnv.setFillColor(colors.black)
            cnv.setFont("Helvetica-Bold", 12)
            cnv.drawString(mm2p(60), y_start + 3, grupo)
            cnv.setFont("Helvetica-Bold", 9)
            cnv.drawString(mm2p(145), y_start + 3, "QTD")
            cnv.drawString(mm2p(162), y_start + 3, "Valor UN")
            cnv.drawString(mm2p(185), y_start + 3, "V. Total")

            if grupo:
                query = """
                    SELECT nome, quantidade_estoque, preco_unitario 
                    FROM produtos 
                    WHERE grupo = ? AND quantidade_estoque > 0
                    ORDER BY nome
                """
                self.c.execute(query, (grupo,))
            else:
                query = """
                    SELECT nome, quantidade_estoque, preco_unitario 
                    FROM produtos 
                    WHERE quantidade_estoque > 0
                    ORDER BY grupo, nome
                """
                self.c.execute(query)
            
            produtos = self.c.fetchall()

            rect_height = mm2p(6)
            grupo_valor_total = 0
            
            def formatar_valor(valor):
                if isinstance(valor, int):
                    return f"{valor:,}"
                elif isinstance(valor, float):
                    valor_formatado = f"{valor:.3f}".rstrip('0').rstrip('.')
                    return valor_formatado
                else:
                    return str(valor)
            
            def abreviar_nome(nome, max_length=60):
                if len(nome) > max_length:
                    return nome[:max_length - 3] + "..."
                return nome

            subgrupo_index = 1

            for nome, quantidade, preco in produtos:
                y_start -= y_step

                if y_start < mm2p(10):
                    cnv.showPage()
                    cnv.setFont("Helvetica", 9)
                    cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")
                    y_start = mm2p(280)

                cnv.rect(mm2p(7), y_start, mm2p(196), rect_height, fill=0)

                for coluna in range(1):
                    x_pos = mm2p(20 + coluna * 50)
                    cnv.line(x_pos, y_start, x_pos, y_start + y_step)
                for coluna in range(1):
                    x_pos = mm2p(140 + coluna * 50)
                    cnv.line(x_pos, y_start, x_pos, y_start + y_step)
                for coluna in range(1):
                    x_pos = mm2p(160 + coluna * 50)
                    cnv.line(x_pos, y_start, x_pos, y_start + y_step)
                for coluna in range(1):
                    x_pos = mm2p(180 + coluna * 50)
                    cnv.line(x_pos, y_start, x_pos, y_start + y_step)

                cnv.setFont("Helvetica", 9)
                nome_abreviado = abreviar_nome(nome)
                cnv.drawString(mm2p(12), y_start + 4, str(subgrupo_index))
                subgrupo_index += 1
                cnv.drawString(mm2p(25), y_start + 4, nome_abreviado)
                cnv.drawString(mm2p(145), y_start + 4, formatar_valor(quantidade))
                cnv.drawString(mm2p(162), y_start + 4, self.formatar_moeda(preco))

                # Verificações de tipo
                try:
                    if isinstance(quantidade, str):
                        quantidade = float(quantidade)
                    if isinstance(preco, str):
                        preco = float(preco)

                    total = quantidade * preco
                    cnv.drawString(mm2p(185), y_start + 4, self.formatar_moeda(total))
                    grupo_valor_total += total
                except ValueError as e:
                    print(f"Erro ao calcular total para {nome}: quantidade={quantidade}, preco={preco}, erro={e}")
                    cnv.drawString(mm2p(185), y_start + 4, "Erro")

            y_start -= y_step
            if y_start < mm2p(10):
                cnv.showPage()
                cnv.setFont("Helvetica", 9)
                cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")
                y_start = mm2p(280)

            rect_y = y_start
            cnv.rect(mm2p(7), rect_y, mm2p(196), rect_height, fill=0)
            cnv.setFont("Helvetica-Bold", 9)
            cnv.drawString(mm2p(25), rect_y + 4, "Total do Grupo:")
            cnv.drawString(mm2p(162), rect_y + 4, self.formatar_moeda(grupo_valor_total))

            return y_start - y_step, grupo_valor_total

        # Gerando o PDF
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, "Relatorio_Estoque.pdf")
        cnv = canvas.Canvas(pdf_path, pagesize=A4)

        # Título e Cabeçalho
        cnv.setFont("Helvetica-Bold", 16)
        cnv.drawString(mm2p(10), mm2p(282), "RELATÓRIO DE ESTOQUE")
        cnv.setFont("Helvetica", 12)
        cnv.drawString(mm2p(10), mm2p(275), "LISTA DE PRODUTOS POR GRUPO")

        cnv.setFont("Helvetica", 9)
        cnv.drawString(mm2p(180), mm2p(5), "Pagina: 1")
        cnv.line(mm2p(10), mm2p(290), mm2p(200), mm2p(290))

        y_start = mm2p(250)
        valor_total_relatorio = 0

        query = "SELECT DISTINCT grupo FROM produtos WHERE quantidade_estoque > 0 ORDER BY grupo"
        self.c.execute(query)
        grupos = self.c.fetchall()

        current_page = 1
        if grupo:
            grupos = [(grupo,)]

        for (grupo,) in grupos:
            y_start, grupo_valor_total = listar_produtos(cnv, y_start, mm2p(6), grupo)
            valor_total_relatorio += grupo_valor_total

            if y_start < mm2p(10):
                cnv.showPage()
                cnv.setFont("Helvetica", 9)
                current_page += 1
                cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{current_page}")
                y_start = mm2p(280)

        if y_start < mm2p(10):
            cnv.showPage()
            cnv.setFont("Helvetica", 9)
            cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")
            y_start = mm2p(280)

        rect_y = y_start
        cnv.rect(mm2p(7), rect_y, mm2p(196), mm2p(6), fill=0)
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(mm2p(25), rect_y + 4, "Total Geral do Estoque:")
        cnv.drawString(mm2p(162), rect_y + 4, self.formatar_moeda(valor_total_relatorio))

        cnv.save()

        # Depois de gerar o PDF, abra o visualizador de PDF
        pdf_viewer = PDFViewer(pdf_path)
        pdf_viewer.mainloop()



    def formatar_moeda (self, valor):
        formatted_value = format_currency(valor, 'BRL', locale='pt_BR')
        return formatted_value
    

    def __del__(self):
        self.conn.close()
class PDFViewer(ctk.CTkToplevel):
    def __init__(self, pdf_path):
        super().__init__()
        self.title("PDF Viewer")
        self.geometry("510x700+200+100")
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.scroll_frame = ttk.Frame(self)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        self.icon_photo_pdf = ctk.CTkImage(light_image=Image.open("img/pdf2.png"), dark_image=Image.open("img/pdf2.png"),size=(52,52))
        self.icon_imprimir_pdf = ctk.CTkImage(light_image=Image.open("img/imprimir.png"), dark_image=Image.open("img/imprimir.png"),size=(52,52))
        self.canvas = tk.Canvas(self.scroll_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.inner_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0,0), window=self.inner_frame, anchor=tk.NW)
        self.load_pdf(pdf_path)
        self.focus_force()
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.label = ctk.CTkLabel(self, text="", height=70).pack()
        self.btn_exportar_pdf = ctk.CTkButton(self, text="Exportar PDF",height=50, text_color="black", fg_color="#9AA3AF", command=lambda: self.exportar_pdf(pdf_path), image=self.icon_photo_pdf)
        self.btn_exportar_pdf.place(relwidth= 0.3, relheight= 0.08, relx=0.1, rely=0.91)
        self.btn_imprimir_pdf = ctk.CTkButton(self, text="Imprimir",height=50, text_color="black", fg_color="#9AA3AF", command=lambda: self.print_pdf(pdf_path), image=self.icon_imprimir_pdf)
        self.btn_imprimir_pdf.place(relwidth= 0.3, relheight= 0.08, relx=0.6, rely=0.91)
        # Adicionando o evento de roda do mouse
        self.bind("<MouseWheel>", self.on_mousewheel)

    def load_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pixmap = page.get_pixmap()
            image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            photo = ImageTk.PhotoImage(image)
            label = ttk.Label(self.inner_frame, image=photo)
            label.image = photo
            label.pack(padx=10, pady=10)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def exportar_pdf(self, pdf_path):
        data_atual = datetime.now().strftime("-%d-%m-%Y")
        nome_pdf = f"Relatorio{data_atual}"
        try:
            # Abrir o diálogo de "Salvar Como" para permitir que o usuário escolha onde salvar o PDF
            file_path = tkinter.filedialog.asksaveasfilename(initialfile= nome_pdf, defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            
            if file_path:
                # Copiar o conteúdo do PDF para o novo arquivo
                with fitz.open(pdf_path) as doc:
                    doc.save(file_path)
                
                messagebox.showinfo("Sucesso", "PDF exportado com sucesso!")
            else:
                messagebox.showinfo("Aviso", "Nenhum arquivo selecionado para exportação.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar PDF: {e}")
    def print_pdf(self, pdf_path):
        try:
            if platform.system() == 'Windows':
            # Tente abrir o PDF com o visualizador padrão
                subprocess.run(['start', '', pdf_path], shell=True)
            else:
                print("Sistema operacional não suportado para impressão.")
        except Exception as e:
            print(f"Erro ao abrir a caixa de diálogo de impressão: {e}")

    def fechar_janela(self):
        self.destroy()  # Destruindo a janela principal

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")


class ImprimirRelatorioEstoque(ctk.CTkToplevel):
    def __init__(self, db_file):
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)
        self.title("Gerar Relatórios")
        self.geometry("550x300+200+315")

        self.img_gerar_re = ctk.CTkImage(light_image=Image.open('img/gerar_re.png'), dark_image=Image.open('img/gerar_re.png'), size=(40, 40))
        self.img_cancelar = ctk.CTkImage(light_image=Image.open('img/cancelar_re.png'), dark_image=Image.open('img/cancelar_re.png'), size=(40, 40))

        self.frame1 = ctk.CTkFrame(self, fg_color='#ffffff')
        self.frame1.place(relwidth=1, relheight=1, relx=0, rely=0)
        self.frame2 = ctk.CTkFrame(self, fg_color='#01497C', corner_radius=100, bg_color='#ffffff')
        self.frame2.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.05)
        self.frame3 = ctk.CTkFrame(self.frame1, fg_color='#545454', corner_radius=100, bg_color='#545454')
        self.frame3.place(relwidth=0.9, relheight=0.009, relx=0.05, rely=0.1)

        self.label1 = ctk.CTkLabel(self.frame2, text="FILTROS", font=('arial', 20))
        self.label1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        
        self.label1 = ctk.CTkLabel(self.frame1, text="SELECIONAR GRUPO", font=('arial', 16),  text_color="black")
        self.label1.place( relx=0.2, rely=0.3)
        self.entry_grupo = ctk.CTkComboBox(self.frame1, text_color= "black", fg_color="#FFFFFF", bg_color="#FFFFFF", button_color="#01497C", dropdown_fg_color="#FFFFFF", dropdown_text_color="black", variable='')
        self.entry_grupo.place(relwidth=0.6, relheight=0.13, relx=0.1, rely=0.4)
        self.carregar_valores_grupo()
        

        
        self.btn_1 = ctk.CTkButton(self.frame1, image=self.img_gerar_re, text="Gerar", fg_color='#545454', command=self.gerar_relatorio_estoque_pdf)
        self.btn_1.place(relwidth=0.2, relheight=0.18, relx=0.75, rely=0.8)
        self.btn_2 = ctk.CTkButton(self.frame1, image=self.img_cancelar, text="Cancelar", fg_color='#545454', hover_color='red', command=self.fechar_janela)
        self.btn_2.place(relwidth=0.2, relheight=0.18, relx=0.5, rely=0.8)
       

    def carregar_valores_grupo(self):
        # Recuperar os valores da tabela 'grupo'
        self.c = self.conn.cursor()
        self.c.execute("SELECT nome FROM grupo")
        grupos = self.c.fetchall()

        # Extrair apenas os nomes dos grupos
        nomes_grupos = [grupo[0] for grupo in grupos]
        # Definir os valores no OptionMenu do grupo
        self.entry_grupo.configure(values=nomes_grupos) 
    
    def fechar_janela(sefl):
        sefl.destroy()
    def gerar_relatorio_estoque_pdf(self):
        grupo_selecionado = self.entry_grupo.get()  # Obtém o grupo selecionado
        
        # Chama o método para gerar o relatório, passando o grupo selecionado
        self.sistema_estoque.gerar_relatorio_estoque_pdf(grupo=grupo_selecionado)

       
        
    
if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = ImprimirRelatorioEstoque(db_file)  # Passar root e db_file como argumentos
    app.mainloop()