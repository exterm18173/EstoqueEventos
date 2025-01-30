import sqlite3
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from assets.icons import carregar_imagens
from controllers.interface import pesquisar_item, adicionar
from db.database import SistemaEstoque
from utils.gerar_etiqueta import GeradorEtiqueta


class JanelaCodeBar(ctk.CTkToplevel):
    def __init__(self, db_file, tree_devolucao, produtos_devolucao, label_preco_total_devolucao):
        super().__init__()

        self.tree = tree_devolucao
        self.total = label_preco_total_devolucao
        self.produtos = produtos_devolucao
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)
        self.title("Gerador de Etiquetas")
        self.geometry("500x500")  # Ajustei o tamanho para acomodar melhor os elementos horizontalmente
        self.resizable(height=False, width=False)
        self.icons = carregar_imagens()
        self.icon_imprimir = self.icons["imprimir_1"]
        
        # Configuração de aparência
        ctk.set_appearance_mode("light")  # Modo claro
        ctk.set_default_color_theme("blue")  # Tema azul
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

        # Adicionando uma seção horizontal para a busca de produto
        self.frame_horizontal_busca = ctk.CTkFrame(self.frame_principal)
        self.frame_horizontal_busca.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        # Entrada para buscar produtos
        self.entry_buscar = ctk.CTkEntry(self.frame_horizontal_busca, placeholder_text="Digite o nome do produto para buscar")
        self.entry_buscar.pack(side=tk.LEFT, padx=10, fill="x", expand=True)

        # Botão para buscar produtos
        self.btn_buscar = ctk.CTkButton(self.frame_horizontal_busca, text="Buscar Produtos", command=lambda: pesquisar_item(self, self.entry_buscar, self.treeview, self.sistema_estoque))
        self.btn_buscar.pack(side=tk.LEFT, padx=10)

        # Treeview para exibir produtos encontrados
        self.treeview = ttk.Treeview(self.frame_principal, columns=("ID", "Nome", "Código de Barras"), show="headings", height=10)
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nome", text="Nome")
        self.treeview.heading("Código de Barras", text="Código de Barras")
        self.treeview.column("ID", anchor=tk.CENTER, width=40)
        self.treeview.column("Código de Barras", anchor=tk.CENTER)

        # Criando a barra de rolagem vertical
        self.scroll_y = tk.Scrollbar(self.frame_principal, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scroll_y.set)

        # Usando grid para colocar a Treeview e a barra de rolagem lado a lado
        self.treeview.grid(row=1, column=0, sticky="nsew")
        self.scroll_y.grid(row=1, column=1, sticky="ns")

        # Tornando o frame redimensionável
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        # Adicionando uma seção horizontal para o peso e o botão de gerar etiqueta
        self.frame_horizontal_peso_etiqueta = ctk.CTkFrame(self.frame_principal)
        self.frame_horizontal_peso_etiqueta.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        # Entrada para digitar o peso
        self.entry_peso = ctk.CTkEntry(self.frame_horizontal_peso_etiqueta, placeholder_text="Digite o peso (kg)")
        self.entry_peso.pack(side=tk.LEFT, padx=10, fill="x", expand=True)

        # Label para exibir a etiqueta gerada
        self.etiqueta_label = ctk.CTkLabel(self.frame_principal, text="", font=("Arial", 14), width=300, height=200, corner_radius=10, fg_color="lightgray")
        self.etiqueta_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")

        self.temp_file_path = None

        # Botão para gerar a etiqueta
        self.gerador_etiqueta = GeradorEtiqueta(self.sistema_estoque, self.treeview, self.etiqueta_label, self.entry_peso)
        self.btn_gerar_etiqueta = ctk.CTkButton(self.frame_horizontal_peso_etiqueta, text="Gerar Etiqueta", command=self.gerar_etiqueta_e_armazenar_caminho)
        self.btn_gerar_etiqueta.pack(side=tk.LEFT, padx=10)

        # Botão de imprimir
        self.btn_imprimir = ctk.CTkButton(self.frame_principal, text="", image=self.icon_imprimir, width=50, command=lambda: [adicionar(self, self.tree, self.sistema_estoque, self.produtos, self.total, self.treeview, self.entry_peso), self.gerador_etiqueta.imprimir_etiqueta(self.caminho_imagem)])
        self.btn_imprimir.place(relx=0.85, rely=0.86)



    def gerar_etiqueta_e_armazenar_caminho(self):
        caminho_imagem = self.gerador_etiqueta.generate_barcode()
        
        if caminho_imagem:
            # Agora você pode armazenar o caminho da imagem na variável desejada
            self.caminho_imagem = caminho_imagem
            print(f"Caminho da imagem armazenado: {self.caminho_imagem}")

if __name__ == "__main__":
    db_file = "db/db_file.db"
    app = JanelaCodeBar(db_file)
    app.mainloop()
