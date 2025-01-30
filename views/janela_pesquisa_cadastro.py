import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage  # Para carregar imagens de ícones

class JanelaPesquisa(ctk.CTkToplevel):
    def __init__(self, parent, tipo, itens):
        super().__init__(parent)
        self.tipo = tipo
        self.itens = itens  # Recebe os itens carregados do WebView
        self.parent = parent
        self.title(f"Pesquisar {tipo}")

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        self.geometry(f"550x400+{largura_tela//2-200}+{altura_tela//3}")
        self.resizable(True, True)  # Permitir redimensionamento

        # Criar o frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # StringVar para rastrear a entrada de pesquisa
        self.search_var = tk.StringVar()

        # Frame para o Entry e o botão de lupa ficarem na mesma linha
        self.pesquisa_frame = ctk.CTkFrame(self.frame)
        self.pesquisa_frame.pack(fill="x", pady=10)

        # Calcular larguras e alturas relativos à janela
        largura_janela = self.winfo_width()
        altura_janela = self.winfo_height()

        # Input de pesquisa
        largura_entry = largura_janela * 0.6  # 60% da largura da janela
        self.entry_pesquisa = ctk.CTkEntry(self.pesquisa_frame, width=largura_entry, height=40, font=("Arial", 16), textvariable=self.search_var)
        self.entry_pesquisa.pack(side="left", padx=(0, 10))

        # Botão de lupa
        largura_btn = largura_janela * 0.1  # 10% da largura da janela
        self.btn_lupa = ctk.CTkButton(self.pesquisa_frame, text="🔎", width=largura_btn, height=40, command=self.filtrar_itens)
        self.btn_lupa.pack(side="left")

        # Definir o foco no campo de pesquisa após a janela ser exibida
        self.after(100, self.entry_pesquisa.focus)

        # Lista de grupos ou subgrupos usando CTkScrollableFrame
        altura_lista = altura_janela * 0.4  # 40% da altura da janela
        largura_lista = largura_janela * 0.8  # 80% da largura da janela
        self.lista_frame = ctk.CTkScrollableFrame(self.frame, height=altura_lista, width=largura_lista)
        self.lista_frame.pack(fill="both", expand=True, pady=10)

        # Atualiza a lista com os itens carregados
        self.atualizar_lista(self.itens)

    def filtrar_itens(self, *args):
        """Filtra os itens com base no texto da pesquisa.""" 
        termo_busca = self.search_var.get().lower()
        itens_filtrados = [item for item in self.itens if termo_busca in item.lower()]
        self.atualizar_lista(itens_filtrados)

    def atualizar_lista(self, itens):
        """Atualiza a lista de itens exibidos na tela."""
        # Limpa os widgets existentes na lista
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

         # Cria um Listbox para exibir os itens
        listbox = tk.Listbox(self.lista_frame, font=("Arial", 14), selectmode=tk.SINGLE, height = 15)
        
        # Faz o Listbox ocupar todo o espaço disponível na lista_frame
        listbox.pack(fill="both", expand=True)

        # Adiciona os itens ao Listbox
        for item in itens:
            listbox.insert(tk.END, item)

        # Ação quando um item é selecionado (opcional)
        def item_selecionado(event):
            selected_item = listbox.get(listbox.curselection())
            self.selecionar_item(selected_item)

        listbox.bind('<<ListboxSelect>>', item_selecionado)


    def selecionar_item(self, item_selecionado=None):
        """Seleciona um item e atualiza o botão na tela principal.""" 
        if not item_selecionado:
            return  # Não faz nada caso não seja passado o item

        # Atualiza o botão na tela principal com o item selecionado
        if self.tipo == "grupo":
            self.parent.btn_grupo.configure(text=item_selecionado)
        elif self.tipo == "subgrupo":
            self.parent.btn_subgrupo.configure(text=item_selecionado)

        # Fecha a janela de pesquisa
        self.destroy()
