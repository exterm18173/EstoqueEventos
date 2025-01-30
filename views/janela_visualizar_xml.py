import sqlite3
from tkinter import ttk, messagebox
from tkinter import filedialog
from babel.numbers import format_currency
import customtkinter as ctk
from datetime import datetime
from utils.pdf_nfe_generator import PdfGenerator
from db.database import SistemaEstoque

class JanelaVisualizarNfe(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        #ctk.set_appearance_mode("light")  # Modo claro
       # ctk.set_default_color_theme("blue")  # Tema azul
        self.arquivo_nome = None
        db_file = "db/db_file.db"
        self.sistema_estoque = SistemaEstoque(db_file)

        # Passando a conexão para o PdfGenerator
        self.pdf_generator = PdfGenerator(self, self.formatar_moeda, self.sistema_estoque)

        self.title("Lista de NFE XMLs")
        # Obtendo as dimensões da tela
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (800 // 2)  # Centralizar a janela
        pos_y = (altura_tela // 2) - (500 // 2)  # Centralizar a janela
        self.geometry(f"800x500+{pos_x}+{pos_y}")  # Ajuste o tamanho da janela
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        # Frame principal
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Criação de campos de entrada para filtros
        self.filter_label = ctk.CTkLabel(frame, text="Filtrar por Nome Arquivo ou Nome Fantasia:", font=("Helvetica", 16))
        self.filter_label.pack(pady=(0, 5))

        self.filter_entry = ctk.CTkEntry(frame, placeholder_text="Digite o nome ou fantasia...", font=("Helvetica", 12))
        self.filter_entry.pack(pady=(0, 10), padx=10, fill="x")

        # Botão para aplicar o filtro
        self.filter_button = ctk.CTkButton(frame, text="Filtrar", font=("Helvetica", 12), command=self.apply_filter)
        self.filter_button.pack(pady=5, padx=10, fill="x")

        # Criação da Treeview para listar os XMLs
        self.tree_xml = ttk.Treeview(frame, columns=('ID', 'Nome Arquivo', 'Nome Fantasia', 'Data Emissão', 'VALOR TOTAL'), show='headings')
        self.tree_xml.heading('ID', text='ID')
        self.tree_xml.heading('Nome Arquivo', text='Nome Arquivo')
        self.tree_xml.heading('Nome Fantasia', text='Nome Fantasia')
        self.tree_xml.heading('Data Emissão', text='Data Emissão')
        self.tree_xml.heading('VALOR TOTAL', text='Valor Total')

        # Ajustes nas colunas
        for col in ('ID', 'Nome Arquivo', 'Nome Fantasia', 'Data Emissão', 'VALOR TOTAL'):
            self.tree_xml.column(col, anchor="center")

        # Largura das colunas
        self.tree_xml.column('ID', width=50)
        self.tree_xml.column('Nome Arquivo', width=300)
        self.tree_xml.column('Nome Fantasia', width=200)
        self.tree_xml.column('Data Emissão', width=150)
        self.tree_xml.column('VALOR TOTAL', width=120)

        self.tree_xml.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões (sem ícones, apenas texto e com tamanho reduzido)
        self.convert_button = ctk.CTkButton(frame, text="Converter para PDF", font=("Helvetica", 12), command=self.gerar_pdf)
        self.convert_button.pack(pady=5, padx=10, fill="x")

        self.export_button = ctk.CTkButton(frame, text="Exportar XML", font=("Helvetica", 12), command=self.export_xml)
        self.export_button.pack(pady=5, padx=10, fill="x")

       

    def apply_filter(self):
        try:
            filter_text = self.filter_entry.get()
            query = """
            SELECT * FROM xml_import
            WHERE "nome_arquivo" LIKE ? OR "nome_fantasia" LIKE ?
            """
            self.sistema_estoque.c.execute(query, ('%' + filter_text + '%', '%' + filter_text + '%'))
            rows = self.sistema_estoque.c.fetchall()

            # Limpa a Treeview antes de exibir os resultados filtrados
            for item in self.tree_xml.get_children():
                self.tree_xml.delete(item)

            # Exibe mensagem se nenhum item for encontrado
            if not rows:
                messagebox.showinfo("Nenhum Resultado", "Nenhum XML encontrado com esse filtro.")

            # Insere os dados na Treeview
            for row in rows:
                formatted_date = datetime.fromisoformat(row[3]).strftime("%d de %B de %Y, %H:%M")
                new_row = (row[0], row[1], row[2], formatted_date, self.formatar_moeda(row[4]))
                self.tree_xml.insert('', 'end', values=new_row)
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro ao acessar o banco de dados: {e}")

    def formatar_moeda(self, valor):
        formatted_value = format_currency(valor, 'BRL', locale='pt_BR')
        return formatted_value

    def export_xml(self):
        # Obtém o item selecionado na Treeview
        selected_item = self.tree_xml.selection()
        if not selected_item:
            messagebox.showwarning("Selecionar item", "Por favor, selecione um item na lista.")
            return

        # Obtém o ID do item selecionado
        item_id = self.tree_xml.item(selected_item)['values'][0]

        # Busca o conteúdo XML no banco de dados usando o ID
        self.sistema_estoque.c.execute("SELECT conteudo_xml FROM xml_import WHERE id=?", (item_id,))
        xml_content = self.sistema_estoque.c.fetchone()

        if xml_content and xml_content[0]:
            # Pergunta ao usuário onde salvar o arquivo
            file_path = filedialog.asksaveasfilename(defaultextension=".xml",
                                                       filetypes=[("XML files", "*.xml"),
                                                                  ("All files", "*.*")])
            if file_path:
                # Salva o conteúdo XML no arquivo
                with open(file_path, 'wb') as file:
                    file.write(xml_content[0])
                messagebox.showinfo("Exportação completa", "XML exportado com sucesso!")
        else:
            messagebox.showerror("Erro", "Conteúdo XML não encontrado.")

    def gerar_pdf(self):
        selected_item = self.tree_xml.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Por favor, selecione um XML do banco de dados.")
            return

        item_id = self.tree_xml.item(selected_item, 'values')[0]
        self.pdf_generator.gerar_pdf(item_id)
    def fechar_janela(self):
        self.destroy()  # Destruindo a janela secundária

if __name__ == "__main__":
    db_file = "db/db_file.db"
    app = JanelaVisualizarNfe(db_file)  # Passando o db_file diretamente
    app.mainloop()
