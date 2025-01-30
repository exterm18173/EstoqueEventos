from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter

def gerar_etiqueta(codigo_produto, nome_produto, peso_produto, valor_produto):
    # Tamanho da etiqueta em pixels (10x5 cm, 300 DPI)
    largura = 1181  # 10 cm * 300 DPI
    altura = 591  # 5 cm * 300 DPI

    # Criar a imagem da etiqueta com fundo branco
    etiqueta = Image.new('RGB', (largura, altura), color=(255, 255, 255))  # Fundo branco
    draw = ImageDraw.Draw(etiqueta)

    # Definir fontes para texto
    try:
        font_regular = ImageFont.truetype("arial.ttf", 18)
        font_bold = ImageFont.truetype("arialbd.ttf", 22)
        font_header = ImageFont.truetype("arialbd.ttf", 28)
        font_total_header = ImageFont.truetype("arialbd.ttf", 20)  # Fonte para "TOTAL R$: "
        font_total_value = ImageFont.truetype("arialbd.ttf", 40)  # Fonte maior para o valor total
    except IOError:
        font_regular = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_total_header = ImageFont.load_default()
        font_total_value = ImageFont.load_default()

    # Adicionar borda simples à etiqueta
    draw.rectangle([5, 5, largura-5, altura-5], outline="black", width=2)

    # Adicionar título em preto
    draw.text((20, 10), "Etiqueta de Produto", font=font_header, fill="black")

    # Espaçamento inicial
    espacamento = 60

    # Adicionar linha de separação entre o título e as informações
    draw.line([10, espacamento, largura-10, espacamento], fill="black", width=2)
    espacamento += 10

    # Adicionar as informações do produto à etiqueta, em preto
    draw.text((20, espacamento), f"Nome: {nome_produto}", font=font_bold, fill="black")
    espacamento += 40
    draw.text((20, espacamento), f"Peso: {peso_produto} kg", font=font_regular, fill="black")
    espacamento += 40
    draw.text((20, espacamento), f"Valor kg: R${valor_produto:.2f}", font=font_regular, fill="black")
    espacamento += 40
    draw.text((20, espacamento), f"Código: {codigo_produto}", font=font_bold, fill="black")

    # Adicionar linha de separação antes do código de barras
    espacamento += 60
    draw.line([10, espacamento, largura-10, espacamento], fill="black", width=2)

    # Calcular o valor total
    valor_total = peso_produto * valor_produto

    # Adicionar o retângulo para "TOTAL R$: " em preto
    espacamento += 70
    retangulo_y = 50
    draw.rectangle([1000, retangulo_y, 1150, retangulo_y + 40], fill="black")

    # Adicionar o texto "TOTAL R$: " em branco
    draw.text((1000 + 20, retangulo_y + 10), f"TOTAL R$: ", font=font_total_header, fill="white")

    # Exibir o valor total abaixo da tarja preta com a fonte maior
    espacamento += 55  # Ajuste o espaçamento para o valor total
    draw.text((950 + 20, 120), f"R$ {valor_total:.2f}", font=font_total_value, fill="black")

    # Gerar o código de barras
    code128 = barcode.get_barcode_class('code128')  # Tipo de código de barras
    barcode_image = code128(codigo_produto, writer=ImageWriter())
    barcode_image.save('codigo_de_barras')  # Salvar como imagem temporária

    # Abrir a imagem do código de barras
    img_barcode = Image.open('codigo_de_barras.png')

    # Redimensionar o código de barras para caber na etiqueta
    img_barcode = img_barcode.resize((largura - 400, 300))  # Ajuste o tamanho conforme necessário

    # Posicionar o código de barras de forma centralizada na parte inferior
    posicao_barcode = ((largura - img_barcode.width) // 2, altura - img_barcode.height - 40)
    etiqueta.paste(img_barcode, posicao_barcode)

    # Adicionar uma linha na parte inferior, abaixo do código de barras
    draw.line([10, altura - 10, largura - 10, altura - 10], fill="black", width=2)

    # Salvar a imagem final da etiqueta
    etiqueta.save('etiqueta_produto_monocromatica.png')

    print("Etiqueta gerada com sucesso!")

# Exemplo de uso
codigo_produto = '20079781038542012240'  # 20 dígitos
nome_produto = 'Produto Exemplo'
peso_produto = 50  # Peso em kg
valor_produto = 100  # Valor em R$

gerar_etiqueta(codigo_produto, nome_produto, peso_produto, valor_produto)
