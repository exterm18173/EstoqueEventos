import os
import socket
import tkinter as tk
import tkinter
import customtkinter as ctk
import sqlite3
from assets.icons import carregar_imagens
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from views.tabs.home_tab import HomeTab
from views.tabs.saida_tab import SaidaTab
from views.tabs.entrada_tab import EntradaTab
from views.tabs.devolucao_tab import DevolucaoTab
from db.database import SistemaEstoque

# Função para verificar se o aplicativo já está em execução
def verificar_instancia_unica():
    # Criar um socket de rede para verificar se já existe uma instância em execução
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Tentar vincular à porta 12345 (ou outra de sua escolha)
    try:
        sock.bind(("127.0.0.1", 12345))
    except socket.error:
        # Se houver erro, significa que a porta já está em uso (ou seja, o app já está rodando)
        return False
    sock.close()
    return True

# Função principal (aplicação)
class EstoqueApp(ctk.CTk):
    def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.sistema_estoque = SistemaEstoque(self.db_file)

        self.title("Estoque New")
        self.geometry("1324x750")
        self.iconbitmap("assets/img/logo.ico")
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.modo_rapido_saida = False
        self.modo_rapido_entrada = False
        self.modo_rapido_devolucao = False
        self.produtos_saida = [] 
        self.produtos_entrada = [] 
        self.produtos_devolucao= []

        # Verificar se já existe uma instância do aplicativo em execução
        if not verificar_instancia_unica():
            messagebox.showerror("Erro", "Já existe uma instância do sistema em execução.")
            self.quit()
            return

        # Adicionando lista para produtos de saída
        self.tabview = ctk.CTkTabview(self, fg_color="#9AA3AF", segmented_button_fg_color="#2C3036",
                                      segmented_button_unselected_color="#2C3036", segmented_button_selected_color="#004A7C")
        self.tabview.pack(side="bottom", fill="both", expand=True)
        self.tabview.add("Home")
        self.tabview.add("Entrada")
        self.tabview.add("Saida")
        self.tabview.add("Devolução")
        self.tabview.tab("Home").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Entrada").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Saida").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Devolução").grid_columnconfigure(0, weight=1)

        # Carregar a Splash Screen
        self.show_splash_screen()

    def show_splash_screen(self):
        splash_window = tk.Toplevel(self)
        splash_window.title("Carregando...")
        splash_window.geometry("600x600")  # Tamanho mais compacto
        splash_window.configure(bg="white")  # Fundo branco

        # Remover a borda da janela
        splash_window.overrideredirect(True)

        # Centralizar a janela da Splash Screen
        screen_width = splash_window.winfo_screenwidth()
        screen_height = splash_window.winfo_screenheight()
        position_top = int(screen_height / 3 - 400 / 2)
        position_left = int(screen_width / 2 - 600 / 2)
        splash_window.geometry(f"+{position_left}+{position_top}")

        # Carregar a imagem (logo)
        icon = carregar_imagens()
        icon_carregar = icon["carregar_sistema"]  # Logo da Splash Screen
        logo_label = ctk.CTkLabel(splash_window, text="", image=icon_carregar, fg_color="white")
        logo_label.pack(pady=30)  # Mais espaço acima do logo

        # Barra de progresso mais simples e moderna
        barra_progresso = ctk.CTkProgressBar(splash_window, width=300, height=10, progress_color="#66B2FF", mode="determinate")
        barra_progresso.pack(pady=20)  # Menos espaço ao redor

        # Label de percentual, mais discreto
        label_percentual = ctk.CTkLabel(splash_window, text="0%", fg_color="white", text_color="black", font=("Helvetica", 14))
        label_percentual.pack(pady=5)

        # Texto indicando qual tab está carregando
        label_aba_atual = ctk.CTkLabel(splash_window, text="Carregando: Home", fg_color="white", text_color="black", font=("Helvetica", 12))
        label_aba_atual.pack(pady=10)

        barra_progresso.set(0)

        # Carregar as tabs uma a uma
        progress_value = 0

        def update_progress():
            nonlocal progress_value
            if progress_value < 100:
                progress_value += 25  # Progresso a cada aba carregada
                barra_progresso.set(progress_value / 100)
                label_percentual.configure(text=f"{progress_value}%")

                # Atualizar o nome da aba que está sendo carregada
                if progress_value == 25:
                    label_aba_atual.configure(text="Carregando: Home")
                    self.home_tab = HomeTab(master=self.tabview.tab("Home"), sistema_estoque=self.sistema_estoque)
                    self.home_tab.pack(expand=True, fill="both")
                elif progress_value == 50:
                    label_aba_atual.configure(text="Carregando: Entrada")
                    self.entrada_tab = EntradaTab(master=self.tabview.tab("Entrada"), sistema_estoque=self.sistema_estoque)
                    self.entrada_tab.pack(expand=True, fill="both")
                elif progress_value == 75:
                    label_aba_atual.configure(text="Carregando: Saída")
                    self.saida_tab = SaidaTab(master=self.tabview.tab("Saida"), sistema_estoque=self.sistema_estoque)
                    self.saida_tab.pack(expand=True, fill="both")
                elif progress_value == 100:
                    label_aba_atual.configure(text="Carregando: Devolução")
                    self.devolucao_tab = DevolucaoTab(master=self.tabview.tab("Devolução"), sistema_estoque=self.sistema_estoque)
                    self.devolucao_tab.pack(expand=True, fill="both")

                # Atualizar a barra de progresso
                self.after(300, update_progress)
            else:
                splash_window.destroy()  # Fechar a Splash Screen
                self.deiconify()  # Mostrar a janela principal após a Splash Screen

        # Iniciar o processo de carregamento
        self.after(200, update_progress)

        # Inicializar a janela principal, mas mantê-la oculta até a Splash Screen desaparecer
        self.withdraw()

    def fechar_janela(self):
        confirmar_fechar = messagebox.askokcancel("Fechar", "Tem certeza que deseja fechar a janela?")
        if confirmar_fechar:
            widgets_secundarios = [widget for widget in self.winfo_children() if isinstance(widget, tkinter.Toplevel)]
            for widget in widgets_secundarios:
                widget.destroy()
            self.destroy()

# Iniciar a aplicação
if __name__ == "__main__":
    db_file = "db/db_file.db"
    app = EstoqueApp(db_file)
    app.mainloop()
