import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from utils.custom_entry_data import CustomEntry
from assets.icons import carregar_imagens


class EditarMovimentacao:
    def __init__(self, master, sistema_estoque, item_id, nome_item, tipo_movimento, data_movimento, cliente):
        self.icons = carregar_imagens()
        self.icon_recarregar = self.icons["recarregar"]
        self.master = master
        self.sistema_estoque = sistema_estoque
        self.item_id = item_id
        self.nome_item = nome_item
        self.tipo_movimento = tipo_movimento
        self.data_movimento = data_movimento
        self.cliente = cliente
        self.lista_de_clientes = ["teste1", "teste2"]  # Simulação de clientes, pode ser atualizado dinamicamente
        
        self.janela_edicao = ctk.CTkToplevel(master)
        self.janela_edicao.title("Editar Movimentação")
        self.janela_edicao.geometry("550x300")
        self.janela_edicao.resizable(width=False, height=False)
        
        self.frame = ctk.CTkFrame(self.janela_edicao, fg_color="#F8FCFF")
        self.frame.place(relwidth=1, relheight=1, relx=0, rely=0)

        # Título do item (exibição não editável)
        ctk.CTkLabel(self.frame, text=f"Nome do Item: {self.nome_item}", text_color="#333333", font=("Arial", 16, "bold")).place(relx=0.05, rely=0.05)

        # Tipo de Movimento
        ctk.CTkLabel(self.frame, text="Tipo de Movimento:", text_color="#333333", font=("Arial", 12)).place(relx=0.05, rely=0.15)
        
        self.tipo_var = ctk.StringVar(value=self.tipo_movimento)
        self.combo_tipo_movimento_edicao = ctk.CTkComboBox(
            self.frame,
            variable=self.tipo_var,
            values=["entrada", "saida", "devolucao"],
            fg_color="#F5F5F5",  # Cor de fundo mais suave
            dropdown_fg_color="#F5F5F5",
            dropdown_text_color="black",
            button_color="#5D6D7E",  # Cor de botão mais suave e moderna
            text_color="black",
            font=("Arial", 12),
            border_width=1,  # Borda sutil
            corner_radius=8  # Bordas arredondadas
        )
        self.combo_tipo_movimento_edicao.place(relwidth=0.25, relheight=0.12, relx=0.3, rely=0.15)

        # Cliente
        ctk.CTkLabel(self.frame, text="Cliente:", text_color="#333333", font=("Arial", 12)).place(relx=0.05, rely=0.35)
        
        self.cliente_var = ctk.StringVar(value=self.cliente)
        self.combo_cliente_edicao = ctk.CTkComboBox(
            self.frame,
            variable=self.cliente_var,
            values=self.lista_de_clientes,  # Inicialmente vazio, será preenchido depois
            fg_color="#F5F5F5",
            dropdown_fg_color="#F5F5F5",
            dropdown_text_color="black",
            button_color="#5D6D7E",
            text_color="black",
            font=("Arial", 12),
            border_width=1,
            corner_radius=8
        )
        self.combo_cliente_edicao.place(relwidth=0.5, relheight=0.12, relx=0.3, rely=0.35)

        # Botão "Atualizar" para carregar os clientes
        self.btn_atualizar_cliente = ctk.CTkButton(self.frame, text="", command=self.recarregar_evento, font=("Arial", 12, "bold"), corner_radius=8, image=self.icon_recarregar, fg_color="#F8FCFF", hover_color="#90EE90")
        self.btn_atualizar_cliente.place(relwidth=0.1, relheight=0.15, relx=0.8, rely=0.34)

        # Data do Movimento
        ctk.CTkLabel(self.frame, text="Data do Movimento (dd/mm/aaaa):", text_color="#333333", font=("Arial", 12)).place(relx=0.05, rely=0.55)
        
        self.entry_data_movimento_edicao = CustomEntry(self.frame, font=("Arial", 14), fg_color="#F5F5F5", text_color="black", border_width=1, corner_radius=8)
        self.entry_data_movimento_edicao.place(relwidth=0.35, relheight=0.12, relx=0.378, rely=0.55)
        self.entry_data_movimento_edicao.insert(0, self.data_movimento)

        # Botão de Salvar
        self.btn_salvar_edicao = ctk.CTkButton(self.frame, text="Salvar", command=lambda: self.salvar_edicoes(self.item_id), font=("Arial", 12, "bold"), text_color="white", corner_radius=8)
        self.btn_salvar_edicao.place(relwidth=0.20, relheight=0.14, relx=0.375, rely=0.78)

        # Chama a função para carregar os eventos depois de criar o combo de cliente
        self.carregar_eventos()
    def recarregar_evento(self):
        self.data_movimento = self.entry_data_movimento_edicao.get()
        self.carregar_eventos()
    def carregar_eventos(self):
        # Conecta ao banco de dados
        conn = sqlite3.connect('db/db_file.db')
        c = conn.cursor()
            
        # Busca eventos com a data selecionada ou "Todas as datas"
        c.execute("SELECT nome FROM eventos WHERE data = ? OR data = ?", (self.data_movimento, "Todas as datas"))
        eventos = c.fetchall()
        
        # Atualiza a lista de clientes (valores) no combo de cliente
        novos_valores = [evento[0] for evento in eventos]  # Extrai apenas os nomes dos eventos
        self.combo_cliente_edicao.configure(values=novos_valores)
        
        # Se não houver eventos, coloca um texto alternativo
        if not novos_valores:
            self.combo_cliente_edicao.configure(values=["Nenhum evento encontrado"])

        conn.close()



    def salvar_edicoes(self, item_id):
        tipo_movimento = self.combo_tipo_movimento_edicao.get().strip()
        data_movimento = self.entry_data_movimento_edicao.get().strip()

        if not self._validar_campos(tipo_movimento, data_movimento):
            return

        try:
            movimentacao_original = self.sistema_estoque._obter_movimentacao_original(item_id)
            if not movimentacao_original:
                return

            tipo_movimento_original, quantidade_movimento_original, codigo_barras = movimentacao_original

            self.sistema_estoque._atualizar_movimentacao(item_id, tipo_movimento, data_movimento)
            self._ajustar_estoque(tipo_movimento_original, tipo_movimento, quantidade_movimento_original, codigo_barras)

            messagebox.showinfo("Sucesso", "Movimentação atualizada com sucesso!")
            self.janela_edicao.destroy()
            self.sistema_estoque.filtrar_movimentacoes(self.nome_item, self.tipo_movimento, self.data_movimento)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar movimentação: {e}")

    def _validar_campos(self, tipo_movimento, data_movimento):
        if not tipo_movimento or not data_movimento:
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")
            return False
        return True

    

    def _ajustar_estoque(self, tipo_movimento_original, tipo_movimento, quantidade_movimento_original, codigo_barras):
        if tipo_movimento_original == "saida":
            if tipo_movimento in ["entrada", "devolucao"]:
                self.sistema_estoque._ajustar_estoque_entrada_devolucao(quantidade_movimento_original, codigo_barras)
        elif tipo_movimento_original == "entrada":
            if tipo_movimento == "saida":
                self.sistema_estoque._ajustar_estoque_saida(quantidade_movimento_original, codigo_barras)
        elif tipo_movimento_original == "devolucao":
            if tipo_movimento == "saida":
                self.sistema_estoque._ajustar_estoque_saida(quantidade_movimento_original, codigo_barras)

    