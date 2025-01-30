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
    def gerar_lista_compras_pdf(self, data_inicio, data_fim, nome_item, cliente_movimento):
        
        def mm2p(milimetros):
            return milimetros / 0.352777

        def listar_grupos_e_subgrupos(cnv, y_start, y_step, grupo):
            # Escreva o nome do grupo
            rect_y = y_start
            rect_height = mm2p(6)
            cnv.setFillColor(colors.lightgrey)
            cnv.rect(mm2p(7), rect_y, mm2p(196), rect_height, fill=1, stroke=1)
            for coluna in range(1):
                x_pos = mm2p(20 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
            for coluna in range(1):
                x_pos = mm2p(140 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
            for coluna in range(1):
                x_pos = mm2p(160 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
            for coluna in range(1):
                x_pos = mm2p(180 + coluna * 50)
                cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
            cnv.setFillColor(colors.black)
            cnv.setFont("Helvetica-Bold", 12)
            cnv.drawString(mm2p(60), y_start + 3, grupo)
            cnv.setFont("Helvetica-Bold", 9)
            cnv.drawString(mm2p(142), y_start + 3, "Quantidade")
            cnv.drawString(mm2p(162), y_start + 3, "Valor")
            cnv.drawString(mm2p(185), y_start + 3, "Total")
            
            query = """
                SELECT 
                    nome_item, 
                    (SUM(CASE WHEN tipo_movimento = 'saida' THEN quantidade_movimento ELSE 0 END) 
                    - SUM(CASE WHEN tipo_movimento = 'devolucao' THEN quantidade_movimento ELSE 0 END)) AS quantidade_total, 
                    valor_movimento  
                FROM 
                    movimentacoes 
                WHERE  
                    grupo_movimento = ? 
                    AND data_movimento BETWEEN ? AND ? 
                    AND nome_item LIKE ? 
                    AND cliente_movimento LIKE ?  -- Adicionando filtro por cliente
                GROUP BY 
                    nome_item
            """

            self.c.execute(query, (grupo, data_inicio, data_fim, '%' + nome_item + '%', '%' + cliente_movimento + '%'))
            movimentacoes_filtradas = self.c.fetchall()
            movimentacoes_filtradas = [mov for mov in movimentacoes_filtradas if mov[1] != 0]
            

            # Desenhar retângulos e colunas
            rect_height = mm2p(6)
            subgrupo_index = 1 
            grupo_valor_total = 0  # Inicializa o valor total do grupo
            def formatar_valor(valor):
                if isinstance(valor, int):  # Se o valor for um inteiro
                    return f"{valor:,}"  # Formata com separador de milhar
                elif isinstance(valor, float):  # Se o valor for um float
                    # Converte para string e remove zeros desnecessários
                    valor_formatado = f"{valor:.3f}".rstrip('0').rstrip('.')  # Remove zeros e o ponto final, se necessário
                    return valor_formatado
                else:
                    return str(valor)  # Retorna como string para outros tipos
            def abreviar_nome(nome, max_length=60):
                if len(nome) > max_length:
                    return nome[:max_length - 3] + "..."  # Mantém os últimos três caracteres para os pontos
                return nome
            
            


            for nome, total_quantidade, valor_und in movimentacoes_filtradas:
                quantidade = f"{round(total_quantidade, 3):.3f}".rstrip("0").rstrip(".").replace('.', ',')
                y_start -= y_step  # Ajuste a posição vertical para o próximo item

                # Se não houver espaço suficiente na página atual, mude para a próxima página
                if y_start < mm2p(10):
                    cnv.showPage()
                    cnv.setFont("Helvetica", 9)
                    cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")

                    # Redefina a posição inicial para o topo da página
                    y_start = mm2p(280)

                # Desenhar retângulo
                rect_y = y_start
                cnv.rect(mm2p(7), rect_y, mm2p(196), rect_height, fill=0)

                # Desenhar colunas
                for coluna in range(1):
                    x_pos = mm2p(20 + coluna * 50)
                    cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
                for coluna in range(1):
                    x_pos = mm2p(140 + coluna * 50)
                    cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
                for coluna in range(1):
                    x_pos = mm2p(160 + coluna * 50)
                    cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)
                for coluna in range(1):
                    x_pos = mm2p(180 + coluna * 50)
                    cnv.line(x_pos, rect_y, x_pos, rect_y + y_step)

                # Escrever nome do subgrupo
                cnv.setFont("Helvetica", 9)
                cnv.drawString(mm2p(12), rect_y + 4, f"{subgrupo_index}")
                subgrupo_index += 1
                nome_abreviado = abreviar_nome(nome)
                cnv.drawString(mm2p(25), rect_y + 4, nome_abreviado)
                cnv.drawString(mm2p(145), rect_y + 4, formatar_valor(quantidade))
                cnv.drawString(mm2p(162), rect_y + 4, self.formatar_moeda(valor_und))
                valor_total = total_quantidade * valor_und
                cnv.drawString(mm2p(182), rect_y + 4, self.formatar_moeda(valor_total))
                
                # Adiciona o valor total do item ao valor total do grupo
                grupo_valor_total += valor_total

            # Adiciona uma linha com o valor total do grupo
            y_start -= y_step
            if y_start < mm2p(10):  # Se não houver espaço, muda para nova página
                cnv.showPage()
                cnv.setFont("Helvetica", 9)
                cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")
                y_start = mm2p(280)

            rect_y = y_start
            cnv.rect(mm2p(7), rect_y, mm2p(196), rect_height, fill=0)
            cnv.setFont("Helvetica-Bold", 9)
            cnv.drawString(mm2p(25), rect_y + 4, "Total do Grupo:")
            cnv.drawString(mm2p(145), rect_y + 4, "")
            cnv.drawString(mm2p(162), rect_y + 4, self.formatar_moeda(grupo_valor_total))
            cnv.drawString(mm2p(182), rect_y + 4, '')

            return y_start - y_step, grupo_valor_total  # Retorne a posição vertical atualizada e o valor total do grupo

        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, "Relatorio.pdf")
        cnv = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        margin = 50
        line_height = 20
        max_lines_per_page = math.floor((height - 2 * margin) / line_height)
        cnv.setFont("Helvetica-Bold", 16)
        cnv.drawString(mm2p(10), mm2p(282), "RELATORIO DE GASTOS POR GRUPOS **")
        cnv.drawString(mm2p(75), mm2p(260), "NEW PALACE EVENTOS")
        cnv.setFont("Helvetica", 12)
        cnv.drawString(mm2p(10), mm2p(275), "CLIENTE: "+ cliente_movimento)
        cnv.drawString(mm2p(10), mm2p(270), "PERIODO:")
        cnv.drawString(mm2p(33), mm2p(270), data_inicio + " a " + data_fim)
        
        cnv.setFont("Helvetica", 9)
        cnv.drawString(mm2p(180), mm2p(5), "Pagina: 1")
        
        cnv.line(mm2p(10), mm2p(290), mm2p(200), mm2p(290))
        
        y_start = mm2p(250)  # Posição inicial para desenhar os itens
        valor_total_relatorio = 0  # Inicializa o valor total do relatório

        query = """
            SELECT DISTINCT grupo_movimento
            FROM movimentacoes
            WHERE data_movimento BETWEEN ? AND ?
            AND cliente_movimento LIKE ?
            AND tipo_movimento = ? ORDER BY grupo_movimento
        """
        # Executando a consulta com as datas como parâmetros
        self.c.execute(query, (data_inicio, data_fim, '%' + cliente_movimento + '%', 'saida'))

        # Obtendo os resultados
        grupos = self.c.fetchall()
        current_page = 1

        for grupo in grupos:
            grupo_nome = grupo[0]
            y_start, grupo_valor_total = listar_grupos_e_subgrupos(cnv, y_start, mm2p(6), grupo_nome)

            # Adiciona o valor total do grupo ao valor total do relatório
            valor_total_relatorio += grupo_valor_total

            # Verifica se é necessária uma nova página
            if y_start < mm2p(10):
                cnv.showPage()
                cnv.setFont("Helvetica", 9)
                current_page += 1
                cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{current_page}")
                y_start = mm2p(280)  # Posição inicial para desenhar os itens na nova página

        # Adiciona uma linha com o valor total do relatório
        
        rect_height = mm2p(6)
        if y_start < mm2p(10):  # Se não houver espaço, muda para nova página
            cnv.showPage()
            cnv.setFont("Helvetica", 9)
            cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")
            y_start = mm2p(280)
        
        rect_y = y_start
        cnv.rect(mm2p(7), rect_y, mm2p(196), rect_height, fill=0)
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(mm2p(25), rect_y + 4, "Total Geral:")
        cnv.drawString(mm2p(162), rect_y + 4, self.formatar_moeda(valor_total_relatorio))
        
 
        cnv.save()
        # Depois de gerar o PDF, abra o visualizador de PDF
        pdf_viewer = PDFViewer(pdf_path)
        pdf_viewer.mainloop()
    def formatar_moeda (self, valor):
        formatted_value = format_currency(valor, 'BRL', locale='pt_BR')
        return formatted_value
    

    def gerar_relatorio_estoque_pdf(self):
        def mm2p(milimetros):
            return milimetros / 0.352777

        def listar_produtos(cnv, y_start, y_step, grupo):
            print("grupos", grupo)
            # Escreva o nome do grupo
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

            query = """
                SELECT nome, quantidade_estoque, preco_unitario 
                FROM produtos 
                WHERE grupo = ? AND quantidade_estoque > 0
                ORDER BY nome
            """
            self.c.execute(query, (grupo,))
            produtos = self.c.fetchall()

            rect_height = mm2p(6)
            grupo_valor_total = 0
            def formatar_valor(valor):
                if isinstance(valor, int):  # Verifica se o valor é inteiro
                    return f"{int(valor)}"  # Retorna como inteiro
                else:
                    return f"{valor:.3f}"  # Retorna com 3 casas decimais
            def abreviar_nome(nome, max_length=60):
                if len(nome) > max_length:
                    return nome[:max_length - 3] + "..."  # Mantém os últimos três caracteres para os pontos
                return nome

            subgrupo_index = 1  # Para numeração dos itens

            for nome, quantidade, preco in produtos:
                y_start -= y_step

                # Se não houver espaço suficiente na página atual, mude para a próxima página
                if y_start < mm2p(10):
                    cnv.showPage()
                    cnv.setFont("Helvetica", 9)
                    cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")
                    y_start = mm2p(280)

                cnv.rect(mm2p(7), y_start, mm2p(196), rect_height, fill=0)

                # Desenhar linhas verticais
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
                cnv.drawString(mm2p(12), y_start + 4, str(subgrupo_index))  # Numeração do item
                subgrupo_index += 1
                cnv.drawString(mm2p(25), y_start + 4, nome_abreviado)
                cnv.drawString(mm2p(145), y_start + 4, formatar_valor(quantidade))
                cnv.drawString(mm2p(162), y_start + 4, f'R$ {preco:.2f}')
                total = quantidade * preco
                cnv.drawString(mm2p(185), y_start + 4, f'R$ {total:.2f}')

                grupo_valor_total += total

            # Adiciona uma linha com o valor total do grupo
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
            cnv.drawString(mm2p(162), rect_y + 4, f'R$ {grupo_valor_total:.2f}'.replace('.', ','))

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

        y_start = mm2p(250)  # Posição inicial para desenhar os itens
        valor_total_relatorio = 0

        query = "SELECT DISTINCT grupo FROM produtos WHERE quantidade_estoque > 0 ORDER BY grupo"
        self.c.execute(query)
        grupos = self.c.fetchall()
        
        current_page = 1

        for (grupo,) in grupos:
            y_start, grupo_valor_total = listar_produtos(cnv, y_start, mm2p(6), grupo)
            valor_total_relatorio += grupo_valor_total

            if y_start < mm2p(10):
                cnv.showPage()
                cnv.setFont("Helvetica", 9)
                current_page += 1
                cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{current_page}")
                y_start = mm2p(280)

        # Adiciona uma linha com o valor total do relatório
        if y_start < mm2p(10):
            cnv.showPage()
            cnv.setFont("Helvetica", 9)
            cnv.drawString(mm2p(180), mm2p(5), f"Pagina:{cnv.getPageNumber()}")
            y_start = mm2p(280)

        rect_y = y_start
        cnv.rect(mm2p(7), rect_y, mm2p(196), mm2p(6), fill=0)
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(mm2p(25), rect_y + 4, "Total Geral do Estoque:")
        cnv.drawString(mm2p(162), rect_y + 4, f'R$ {valor_total_relatorio:.2f}'.replace('.', ','))

        cnv.save()

        # Depois de gerar o PDF, abra o visualizador de PDF
        pdf_viewer = PDFViewer(pdf_path)
        pdf_viewer.mainloop()



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
   
class ClientePesquisa(ctk.CTkToplevel):
    def __init__(self, parent, clientes):
        super().__init__(parent)
        self.title("Selecionar Cliente")
        self.geometry("300x300")
        self.clientes = clientes
        self.filtered_clientes = clientes
        self.selected_cliente = None

        # Campo de pesquisa
        self.entry_pesquisa = ctk.CTkEntry(self, placeholder_text="Pesquise um cliente...")
        self.entry_pesquisa.pack(pady=10)
        self.entry_pesquisa.bind("<KeyRelease>", self.atualizar_lista)

        # Listbox para exibir os clientes filtrados
        self.listbox = tk.Listbox(self)  # Usando tk.Listbox
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for cliente in self.clientes:
            self.listbox.insert(tk.END, cliente)

        self.listbox.bind("<Double-Button-1>", self.selecionar_cliente)

        self.btn_selecionar = ctk.CTkButton(self, text="Selecionar", command=self.selecionar_cliente)
        self.btn_selecionar.pack(pady=10)

    def atualizar_lista(self, event=None):
        pesquisa = self.entry_pesquisa.get().lower()
        self.filtered_clientes = [cliente for cliente in self.clientes if pesquisa in cliente.lower()]
        
        self.listbox.delete(0, tk.END)  # Limpa a listbox
        for cliente in self.filtered_clientes:
            self.listbox.insert(tk.END, cliente)  # Adiciona os clientes filtrados

    def selecionar_cliente(self, event=None):
        try:
            self.selected_cliente = self.listbox.get(self.listbox.curselection())
            self.destroy()
        except tk.TclError:
            pass  # Se nada estiver selecionado, não faz nada


class ImprimirRelatorio(ctk.CTkToplevel):
    def __init__(self, db_file):
        super().__init__()
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)
        self.title("Gerar Relatórios")
        self.geometry("550x400+200+315")

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
        self.label2 = ctk.CTkLabel(self.frame1, text="Periodo:", font=('arial', 16), text_color='black')
        self.label2.place(relwidth=0.2, relheight=0.1, relx=0.01, rely=0.3)
        self.label3 = ctk.CTkLabel(self.frame1, text="Data Inicial:", font=('arial', 12), text_color='black')
        self.label3.place(relwidth=0.2, relheight=0.1, relx=0.18, rely=0.22)
        self.label4 = ctk.CTkLabel(self.frame1, text='Data Final:', font=('arial', 12), text_color='black')
        self.label4.place(relwidth=0.2, relheight=0.1, relx=0.48, rely=0.22)
        self.label5 = ctk.CTkLabel(self.frame1, text="Nome Item:", font=('arial', 16), text_color='black')
        self.label5.place(relwidth=0.2, relheight=0.1, relx=0.01, rely=0.5)

        self.label_cliente = ctk.CTkLabel(self.frame1, text="Cliente:", font=('arial', 16), text_color='black')
        self.label_cliente.place(relwidth=0.2, relheight=0.1, relx=0.01, rely=0.65)
        
        self.entry_cliente = ctk.CTkEntry(self.frame1, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_cliente.place(relwidth=0.5, relheight=0.09, relx=0.2, rely=0.65)

        self.btn_pesquisar = ctk.CTkButton(self.frame1, text="🔍", command=self.abrir_janela_pesquisa)
        self.btn_pesquisar.place(relwidth=0.1, relheight=0.09, relx=0.7, rely=0.65)

        self.btn_1 = ctk.CTkButton(self.frame1, image=self.img_gerar_re, text="Gerar", fg_color='#545454', command=self.gerar_lista_compras_pdf_interface)
        self.btn_1.place(relwidth=0.2, relheight=0.12, relx=0.75, rely=0.85)
        self.btn_2 = ctk.CTkButton(self.frame1, image=self.img_cancelar, text="Cancelar", fg_color='#545454', hover_color='red', command=self.fechar_janela)
        self.btn_2.place(relwidth=0.2, relheight=0.12, relx=0.5, rely=0.85)
        self.btn_estoque = ctk.CTkButton(self.frame1, text="QTD Estoque", command=self.gerar_relatorio_estoque_pdf)
        self.btn_estoque.place(relwidth=0.2, relheight=0.12, relx=0.25, rely=0.85)

        self.entry_data_inicio = CustomEntry(self.frame1, width=100, height=30, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_data_inicio.place(relwidth=0.2, relheight=0.09, relx=0.2, rely=0.3)
        self.entry_data_fim = CustomEntry(self.frame1, width=100, height=30, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_data_fim.place(relwidth=0.2, relheight=0.09, relx=0.5, rely=0.3)
        self.entry_nome_item = ctk.CTkEntry(self.frame1, width=100, height=30, font=("Arial", 14), text_color="black", fg_color="#FFFFFF")
        self.entry_nome_item.place(relwidth=0.6, relheight=0.09, relx=0.2, rely=0.5)

        self.carregar_clientes()

    def carregar_clientes(self):
        self.c = self.conn.cursor()
        self.c.execute("SELECT nome FROM eventos")
        self.clientes = [row[0] for row in self.c.fetchall()]
    def fechar_janela(sefl):
        sefl.destroy()
    def gerar_relatorio_estoque_pdf(self):
            self.sistema_estoque.gerar_relatorio_estoque_pdf()
    def gerar_lista_compras_pdf_interface(self):
        data_inicio = self.entry_data_inicio.get().strip()
        data_fim = self.entry_data_fim.get().strip()
        nome_item = self.entry_nome_item.get().strip()
        cliente = self.entry_cliente.get().strip()

        # Verifica se data_inicio e data_fim estão vazias
        if not data_inicio or not data_fim:
            messagebox.showerror("Erro", "Por favor, preencha as datas de início e fim.")
            return

        # Chama o método para gerar o PDF com as entradas fornecidas
        self.sistema_estoque.gerar_lista_compras_pdf(data_inicio, data_fim, nome_item, cliente)   
    def abrir_janela_pesquisa(self):
        janela_pesquisa = ClientePesquisa(self, self.clientes)
        self.wait_window(janela_pesquisa)  # Espera até que a janela de pesquisa seja fechada

        if janela_pesquisa.selected_cliente:
            self.entry_cliente.delete(0, tk.END)  # Limpa o campo
            self.entry_cliente.insert(0, janela_pesquisa.selected_cliente)
    
    
if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = ImprimirRelatorio(db_file)  # Passar root e db_file como argumentos
    app.mainloop()