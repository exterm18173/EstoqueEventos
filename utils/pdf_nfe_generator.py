# pdf_generator.py
import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PdfGenerator:
    def __init__(self, app, formatar_moeda, sistema_estoque):
        self.app = app
        self.sistema_estoque = sistema_estoque
        self.formatar_moeda = formatar_moeda
        

    def gerar_pdf(self, item_id):
        # Recupera o conteúdo do XML (BLOB)
        self.sistema_estoque.c.execute("SELECT conteudo_xml FROM xml_import WHERE id=?", (item_id,))
        result = self.sistema_estoque.c.fetchone()

        if result:
            conteudo_xml = result[0]
            pdf_file_path = "output.pdf"
            self.create_pdf(conteudo_xml, pdf_file_path)
            os.startfile(pdf_file_path)

    def create_pdf(self, xml_content, pdf_file_path):
        # Salva o conteúdo XML em um arquivo temporário para extração
        xml_file_path = "temp.xml"
        with open(xml_file_path, 'wb') as f:
            f.write(xml_content)

        # Processa o XML
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        width, height = letter

        # Cabeçalho do PDF
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 50, "Detalhes da Nota Fiscal Eletrônica")
        c.setFont("Helvetica", 10)
        c.drawString(100, height - 70, "=======================================")

        # Extraindo informações do cabeçalho da NF-e
        emitente = root.find('.//nfe:emit', namespace)
        xFant = root.find('.//nfe:infNFe/nfe:emit/nfe:xFant', namespace)
        vPag = root.find('.//nfe:infNFe/nfe:pag/nfe:detPag/nfe:vPag', namespace).text
        nome_fornecedor = xFant.text if xFant is not None else "N/A"
        data_emissao = root.find('.//nfe:dhEmi', namespace).text if root.find('.//nfe:dhEmi', namespace) is not None else "N/A"

        c.drawString(100, height - 90, f"Emitente: {emitente.find('nfe:xNome', namespace).text if emitente is not None else 'N/A'}")
        c.drawString(100, height - 110, f"Nome Fantasia: {nome_fornecedor}")
        c.drawString(100, height - 130, f"Data de Emissão: {data_emissao}")
        c.drawString(350, height - 130, f"Valor pago: {self.formatar_moeda(vPag)}")

        # Cabeçalho dos produtos
        c.drawString(100, height - 150, "Produto                 | Código EAN       | Valor Unitário  | Quantidade")
        c.drawString(100, height - 160, "----------------------------------------------------------------------------------------")

        # Definindo as larguras das colunas
        column_widths = [150, 100, 80, 50]  # em pontos
        y_position = height - 180
        c.setFont("Helvetica", 7)  # Fonte menor para os produtos

        for det in root.findall('.//nfe:det', namespace):
            prod = det.find('nfe:prod', namespace)
            cEAN = prod.find('nfe:cEAN', namespace).text if prod.find('nfe:cEAN', namespace) is not None else "N/A"
            xProd = prod.find('nfe:xProd', namespace).text if prod.find('nfe:xProd', namespace) is not None else "N/A"
            qCom = prod.find('nfe:qCom', namespace).text if prod.find('nfe:qCom', namespace) is not None else "N/A"
            vUnCom = prod.find('nfe:vUnCom', namespace).text if prod.find('nfe:vUnCom', namespace) is not None else "N/A"

            # Adicionar os dados ao PDF, formatando em colunas
            y_position = self.add_product_to_pdf(c, xProd, cEAN, vUnCom, qCom, y_position, column_widths)

            # Verifica se a posição Y está próxima do limite da página
            if y_position < 40:  # Deixa um espaço de 40 para o rodapé
                c.showPage()  # Cria uma nova página
                self.add_pdf_header(c)
                y_position = height - 180  # Reinicia a posição Y

        c.save()
        os.remove(xml_file_path)

    def add_product_to_pdf(self, c, xProd, cEAN, vUnCom, qCom, y_position, column_widths):
        c.setFont("Helvetica", 7)  # Fonte menor
        # Quebra o texto longo e adiciona ao PDF
        wrapped_lines = self.wrap_text(xProd, column_widths[0])
        for line in wrapped_lines:
            c.drawString(100, y_position, f"{line:<150}")
            y_position -= 10  # Move para baixo na página

        # Adiciona os outros detalhes de produto em colunas
        c.drawString(100 + column_widths[0], y_position, cEAN)
        c.drawString(100 + column_widths[0] + column_widths[1], y_position, vUnCom)
        c.drawString(100 + column_widths[0] + column_widths[1] + column_widths[2], y_position, qCom)

        # Adiciona linha horizontal
        c.line(100, y_position - 2, 100 + sum(column_widths), y_position - 2)

        return y_position - 10  # Move para baixo na página

    def wrap_text(self, text, width):
        """Quebra o texto em linhas que cabem na largura especificada."""
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += (word + " ")
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def add_pdf_header(self, c):
        """Adiciona o cabeçalho na nova página."""
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, c._pagesize[1] - 50, "Detalhes da Nota Fiscal Eletrônica")
        c.setFont("Helvetica", 10)
        c.drawString(100, c._pagesize[1] - 70, "=======================================")
        c.drawString(100, c._pagesize[1] - 150, "Produto                 | Código EAN       | Valor Unitário  | Quantidade")
        c.drawString(100, c._pagesize[1] - 160, "----------------------------------------------")
