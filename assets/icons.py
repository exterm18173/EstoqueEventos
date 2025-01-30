# icons.py
import customtkinter as ctk
from PIL import Image

# Definindo as imagens para os botões
def carregar_imagens():
    icons = {
        "adicionar": ctk.CTkImage(light_image=Image.open("assets/img/adicionar.png"), dark_image=Image.open("assets/img/adicionar.png"), size=(32, 32)),
        "cadastrar": ctk.CTkImage(light_image=Image.open("assets/img/cadastrar.png"), dark_image=Image.open("assets/img/cadastrar.png"), size=(38, 38)),
        "pesquizar": ctk.CTkImage(light_image=Image.open("assets/img/pesquizar.png"), dark_image=Image.open("assets/img/pesquizar.png"), size=(38, 38)),
        "grupos": ctk.CTkImage(light_image=Image.open("assets/img/grupos.png"), dark_image=Image.open("assets/img/grupos.png"), size=(38, 38)),
        "xml": ctk.CTkImage(light_image=Image.open("assets/img/xml.png"), dark_image=Image.open("assets/img/xml.png"), size=(38, 38)),
        "movimentacao": ctk.CTkImage(light_image=Image.open("assets/img/movimentacao.png"), dark_image=Image.open("assets/img/movimentacao.png"), size=(38, 38)),
        "compras": ctk.CTkImage(light_image=Image.open("assets/img/compras.png"), dark_image=Image.open("assets/img/compras.png"), size=(38, 38)),
        "bar_code": ctk.CTkImage(light_image=Image.open("assets/img/barcode.png"), dark_image=Image.open("assets/img/barcode.png"), size=(38, 38)),
        "cod_bar": ctk.CTkImage(light_image=Image.open("assets/img/cod_bar.png"), dark_image=Image.open("assets/img/cod_bar.png"), size=(450, 300)),
        "relatorio": ctk.CTkImage(light_image=Image.open("assets/img/relatorio.png"), dark_image=Image.open("assets/img/relatorio.png"), size=(38, 38)),
        "saida_grupo": ctk.CTkImage(light_image=Image.open("assets/img/saida_grupo.png"), dark_image=Image.open("assets/img/saida_grupo.png"), size=(38, 38)),
        "socket": ctk.CTkImage(light_image=Image.open("assets/img/socket.png"), dark_image=Image.open("assets/img/socket.png"), size=(38, 38)),
        "event": ctk.CTkImage(light_image=Image.open("assets/img/event.png"), dark_image=Image.open("assets/img/event.png"), size=(38, 38)),
        "tela": ctk.CTkImage(light_image=Image.open("assets/img/tela2.jpg"), dark_image=Image.open("assets/img/tela2.jpg"), size=(1100,1000)),
        "salvar": ctk.CTkImage(light_image=Image.open("assets/img/salvar.png"), dark_image=Image.open("assets/img/salvar.png"),size=(82,82)),
        "delete": ctk.CTkImage(light_image=Image.open("assets/img/delete.png"), dark_image=Image.open("assets/img/delete.png"),size=(82,82)),   
        "imprimir_1": ctk.CTkImage(light_image=Image.open("assets/img/imprimir_1.png"), dark_image=Image.open("assets/img/imprimir_1.png"),size=(42,42)),   
        "gerar_barcode": ctk.CTkImage(light_image=Image.open("assets/img/gerar_barcode.png"), dark_image=Image.open("assets/img/gerar_barcode.png"),size=(98,58)),   
        "copiar": ctk.CTkImage(light_image=Image.open("assets/img/copiar.png"), dark_image=Image.open("assets/img/copiar.png"),size=(48,48)),   
        "recarregar": ctk.CTkImage(light_image=Image.open("assets/img/recarregando.png"), dark_image=Image.open("assets/img/recarregando.png"),size=(38,38)), 
        "erro": ctk.CTkImage(light_image=Image.open("assets/img/erro.png"), dark_image=Image.open("assets/img/erro.png"),size=(38,38)), 
        "carregar_sistema": ctk.CTkImage(light_image=Image.open("assets/img/logo.png"), dark_image=Image.open("assets/img/logo.png"),size=(300,300)), 
        "lista_arquivos": ctk.CTkImage(light_image=Image.open("assets/img/lista_arquivos.png"), dark_image=Image.open("assets/img/lista_arquivos.png"),size=(38,38)), 

    }
    return icons
