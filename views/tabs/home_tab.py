import customtkinter as ctk
from PIL import Image
from evento import CadastroEvento
from grupos import JanelaGrupos
from entrada_xml import JanelaXml
from produtos import JanelaProduto
from views.janela_cadastro import JanelaCadastro
#from movimentacao import JanelaMovimentacao
from views.janela_movimentacao import JanelaMovimentacao
from views.janela_code_bar import JanelaCodeBar
from relatorios import JanelaRelatorio
from servidor import JanelaServidor
from saida_lote import SaidaPorGrupo
from utils.gerar_lista_compras import GerarListaCompras
from assets.icons import carregar_imagens

class HomeTab(ctk.CTkFrame):
    def __init__(self, master=None, sistema_estoque=None, **kwargs):
        super().__init__(master, **kwargs)
        self.sistema_estoque = sistema_estoque
        # Calculando as dimensões relativas da imagem
        self.icons = carregar_imagens()

        # Agora você pode acessar as imagens pelo dicionário
        self.icon_photo_cadastrar = self.icons["cadastrar"]
        self.icon_photo_pesquizar = self.icons["pesquizar"]
        self.icon_photo_grupos = self.icons["grupos"]
        self.icon_photo_xml = self.icons["xml"]
        self.icon_photo_movimentacao = self.icons["movimentacao"]
        self.icon_photo_compras = self.icons["compras"]
        self.icon_photo_bar_code = self.icons["bar_code"]
        self.icon_photo_cod_bar = self.icons["cod_bar"]
        self.icon_photo_relatorio = self.icons["relatorio"]
        self.icon_photo_saida_grupo = self.icons["saida_grupo"]
        self.icon_photo_socket = self.icons["socket"]
        self.icon_event = self.icons["event"]
        self.icon_photo_tela = self.icons["tela"]
        #Adicionando e posicionando Frames 
        self.frame1_home = ctk.CTkFrame(master=self, fg_color="#F8FCFF")
        self.frame1_home.place(relwidth=0.29, relheight=0.32, relx= 0.716, rely= 0.693)
        self.frame2_home = ctk.CTkFrame(master=self, fg_color="#F8FCFF")
        self.frame2_home.place(relwidth=0.715, relheight=0.857, relx= 0, rely= 0.145)
        self.frame3_home = ctk.CTkFrame(master=self, fg_color="#01497C")
        self.frame3_home.place(relwidth=1, relheight=0.143, relx= 0, rely= 0)
        self.frame4_home = ctk.CTkFrame(master=self, fg_color="#F8FCFF")
        self.frame4_home.place(relwidth=0.3, relheight=0.55, relx= 0.716, rely= 0.14)
        self.frame5_home = ctk.CTkFrame(self.frame4_home, fg_color="#2D3137")
        self.frame5_home.place(relwidth=1, relheight=0.1, relx= 0, rely= 0)
        
        #Adicionando Labels a aba Home
        self.Label1_cadastro = ctk.CTkLabel(self.frame3_home, text="SISTEMA DE ESTOQUE NEW PALACE", text_color="#ffffff", font=("Arial", 40))
        self.Label1_cadastro.pack(pady = 30)
        self.Label2_cadastro = ctk.CTkLabel(self.frame5_home, text="ESTOQUE", text_color="#ffffff", font=("Arial", 16))
        self.Label2_cadastro.pack(pady= 8)
        
        
        #Colocando imagens nos frames
        self.cod_bar = ctk.CTkLabel( self.frame1_home, image=self.icon_photo_cod_bar, text="")
        self.cod_bar.pack()
        self.tela = ctk.CTkLabel( self.frame2_home, image=self.icon_photo_tela, text="")
        self.tela.pack()
        
        #Adicionando botões Home
        self.btn_botao_cadastro = ctk.CTkButton(self.frame4_home, text="Cadastrar Produto", font=("Arial", 12), image=self.icon_photo_cadastrar, fg_color="#F8FCFF", text_color="black", hover_color="#90EE90", command=lambda: abrir_janela('cadastro', sistema_estoque))
        self.btn_botao_cadastro.place(relwidth=0.45, relheight=0.12, relx=0.05, rely=0.1)
        self.btn_botao_pesquizar = ctk.CTkButton(self.frame4_home, text="Pesquizar Produto", font=("Arial", 12), image=self.icon_photo_pesquizar, fg_color="#F8FCFF", text_color="black", hover_color="#9AA3AF", command=lambda: abrir_janela('pesquiza',  sistema_estoque))
        self.btn_botao_pesquizar.place(relwidth=0.45, relheight=0.12, relx=0.05, rely=0.25)
        self.btn_botao_grupos = ctk.CTkButton(self.frame4_home, text="Grupos e SubGrupos", font=("Arial", 12), image=self.icon_photo_grupos, fg_color="#F8FCFF", text_color="black", hover_color="#9AA3AF", command=lambda: abrir_janela('grupos', sistema_estoque))
        self.btn_botao_grupos.place(relwidth=0.45, relheight=0.12, relx=0.05, rely=0.4)     
        self.btn_botao_xml = ctk.CTkButton(self.frame4_home,text="Entrada de XML", font=("Arial", 12), image=self.icon_photo_xml, fg_color="#F8FCFF", text_color="black", hover_color="#90EE90", command=lambda: abrir_janela('xml', sistema_estoque))
        self.btn_botao_xml.place(relwidth=0.45, relheight=0.12,relx=0.05, rely=0.55)        
        self.btn_botao_movimentacao = ctk.CTkButton(self.frame4_home,text="Movimentações", font=("Arial", 12), image=self.icon_photo_movimentacao, fg_color="#F8FCFF", text_color="black", hover_color="#9AA3AF", command=lambda: abrir_janela('movimentacao', sistema_estoque))
        self.btn_botao_movimentacao.place(relwidth=0.4, relheight=0.12, relx=0.5, rely=0.1)        
        self.btn_botao_compras = ctk.CTkButton(self.frame4_home, text="Lista de Compras", font=("Arial", 12), image=self.icon_photo_compras, fg_color="#F8FCFF", text_color="black", hover_color="#9AA3AF", command=lambda: abrir_janela('compras', sistema_estoque))
        self.btn_botao_compras.place(relwidth=0.4, relheight=0.12, relx=0.5, rely=0.25)
        self.btn_botao_code_bar = ctk.CTkButton(self.frame4_home,text="Gerar Barcode",font=("Arial", 12),image=self.icon_photo_bar_code,fg_color="#F8FCFF",text_color="black",hover_color="#9AA3AF", command=lambda: abrir_janela('codebar', sistema_estoque))
        self.btn_botao_code_bar.place(relwidth=0.4, relheight=0.12,relx=0.5, rely=0.4)
        self.btn_botao_relatorio = ctk.CTkButton(self.frame4_home,text="Relatorio Gastos",font=("Arial", 12),image=self.icon_photo_relatorio,fg_color="#F8FCFF",text_color="black",hover_color="#9AA3AF",command=lambda: abrir_janela('relatorio', sistema_estoque))
        self.btn_botao_relatorio.place(relwidth=0.4, relheight=0.12,relx=0.5, rely=0.55)
        self.btn_botao_automacao = ctk.CTkButton(self.frame4_home,text="Saida Lote",font=("Arial", 12),image=self.icon_photo_saida_grupo,fg_color="#F8FCFF",text_color="black",hover_color="#9AA3AF", command=lambda: abrir_janela('saida_lote', sistema_estoque))
        self.btn_botao_automacao.place(relwidth=0.4, relheight=0.12,relx=0.5, rely=0.7)
        self.btn_botao_socket= ctk.CTkButton(self.frame4_home,text="Socket DB",font=("Arial", 12),image=self.icon_photo_socket,fg_color="#F8FCFF",text_color="black",hover_color="#9AA3AF", command=lambda: abrir_janela('servidor', sistema_estoque))
        self.btn_botao_socket.place(relwidth=0.45, relheight=0.12,relx=0.05, rely=0.7)
        self.btn_botao_eventos= ctk.CTkButton(self.frame4_home,text="Eventos",font=("Arial", 12),image=self.icon_event,fg_color="#F8FCFF",text_color="black",hover_color="#9AA3AF", command=lambda: abrir_janela('event', sistema_estoque))
        self.btn_botao_eventos.place(relwidth=0.45, relheight=0.12,relx=0.05, rely=0.85)

# Dicionário de janelas abertas
janelas = {}
def abrir_janela(tipo, sistema_estoque):
    # Verifica se já existe uma janela do tipo solicitado aberta
    if tipo in janelas and janelas[tipo].winfo_exists():
        # Se a janela já está aberta, traz ela para frente
        janelas[tipo].deiconify()
        janelas[tipo].lift()
        janelas[tipo].focus()
        
    else:
        # Se não existe, cria uma nova janela
        janela = None
        if tipo == 'grupos':
            janela = JanelaGrupos("db/db_file.db")
        elif tipo == 'cadastro':
            janela = JanelaCadastro("db/db_file.db")
        elif tipo == 'pesquiza':
            janela = JanelaProduto("db/db_file.db")
        elif tipo == 'xml':
            janela = JanelaXml("db/db_file.db")
        elif tipo == 'movimentacao':
            janela = JanelaMovimentacao("db/db_file.db")
        elif tipo == 'codebar':
            janela = JanelaCodeBar("db/db_file.db")
        elif tipo == 'relatorio':
            janela = JanelaRelatorio("db/db_file.db")
        elif tipo == 'saida_lote':
            janela = SaidaPorGrupo("db/db_file.db")
        elif tipo == 'servidor':
            janela = JanelaServidor("db/db_file.db")
        elif tipo == 'event':
            janela = CadastroEvento("db/db_file.db")
        elif tipo == 'compras':  # Adicionando a lógica para a janela de Lista de Compras
            janela = GerarListaCompras("db/db_file.db")

        if janela:
            # Armazena a janela no dicionário
            janelas[tipo] = janela
            janela.protocol("WM_DELETE_WINDOW", lambda: fechar_janela(tipo))
            janela.mainloop()

def fechar_janela(tipo):
    # Remove a janela do dicionário ao fechar
    if tipo in janelas:
        janelas[tipo].destroy()
        del janelas[tipo]