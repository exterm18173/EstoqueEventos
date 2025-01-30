import sqlite3
from tkinter import messagebox
from typing import Tuple
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

import pyperclip
from views.tela_edicao_produto import TelaEdicaoItem
import webcolors
from assets.icons import carregar_imagens



class Produto:
    def __init__(self, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo):
        #self.id = id
        self.nome = nome 
        self.codigo_barras = codigo_barras
        self.preco_unitario = preco_unitario
        self.quantidade_estoque = quantidade_estoque
        self.grupo = grupo
        self.sub_grupo = sub_grupo

class SistemaEstoque:
    def __init__(self, db_file, parent=None):
        self.parent = parent
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
    def __del__(self):
        self.conn.close()
    def excluir_produto(self, id_produto):
        try:
            self.c.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
            self.conn.commit()
            messagebox.showinfo("Atenção", "Item excluído com sucesso.", parent=self.parent)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir item do banco de dados: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao excluir item do banco de dados: {e}")    



class JanelaProduto(ctk.CTkToplevel):
    def __init__(self, db_file):  # Adicione db_file como argumento
        super().__init__()
        self.icons = carregar_imagens()
        self.icon_copiar = self.icons["copiar"]
        self.edicao_aberta = False
        self.conn = sqlite3.connect(db_file)
        self.sistema_estoque = SistemaEstoque(db_file, parent=self)  # Passe db_file aqui
        self.title("Pesquizar produtos")
        # Obtendo as dimensões da tela
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        largura_janela = largura_tela * 0.7  # 71.5% da largura da tela
        altura_janela = altura_tela * 0.6  # 85.7% da altura da tela
        x_pos = largura_tela * 0.005  # Posição horizontal (0% da largura da tela)
        y_pos = altura_tela * 0.27  # Posição vertical (14.5% da altura da tela)
        self.geometry(f"{int(largura_janela)}x{int(altura_janela)}+{int(x_pos)}+{int(y_pos)}")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        #self.resizable(width=False, height=False)           

        
        
        #Adicionando frames
        self.frame_produtos1 = ctk.CTkFrame(self, fg_color="#2D3137")
        self.frame_produtos1.place(relwidth= 1 , relheight = 0.15, relx=0,rely=0)
        self.frame_produtos2 = ctk.CTkFrame(self, fg_color="#F8FCFF")
        self.frame_produtos2.place(relwidth = 1, relheight=0.2, relx=0, rely=0.15)
        self.frame_produtos3 = ctk.CTkFrame(self,fg_color="green")
        self.frame_produtos3.place(relwidth=1 , relheight=0.65, relx=0, rely=0.35)
        
        
        
        #Adicionando Labels
        self.label_produto1 = ctk.CTkLabel(self.frame_produtos1, text="PESQUIZAR PRODUTOS NO ESTOQUE", text_color="#FFFFFF", font=("Arial", 32))
        self.label_produto1.pack(pady=15)
        #Adicionando Combobox
        self.combobox_1 = ctk.CTkComboBox(self.frame_produtos2, values=["Nome", "Código de Barras", "Grupo"], fg_color="#FFFFFF", text_color="black", dropdown_fg_color="#FFFFFF", dropdown_text_color="black", dropdown_hover_color="#9AA3AF")
        self.combobox_1.place(relx=0.01, rely=0.2)
        #Adicionando Entry
        self.entry_pesquisar = ctk.CTkEntry(self.frame_produtos2, text_color="black", font=("Arial", 14), fg_color="#FFFFFF")
        self.entry_pesquisar.place(relwidth=0.4, relheight=0.35, relx=0.18, rely=0.18)

        #Adicionando Botão
        self.btn_pesquisar = ctk.CTkButton(self.frame_produtos2, text="Pesquisar", fg_color="#2D3137", hover_color="#9AA3AF", text_color="#FFFFFF", command=self.pesquisar_item)
        self.btn_pesquisar.place(relwidth=0.1, relheight=0.35, relx=0.6, rely=0.2)
        self.btn_excluir = ctk.CTkButton(self.frame_produtos2, text="Excluir", width=80, fg_color="#2D3137", hover_color="#c2061d", text_color="#FFFFFF", command=self.excluir_produto)
        self.btn_excluir.place(relwidth=0.1, relheight=0.35, relx=0.75, rely=0.2)
        
        
        self.btn_copy_codigo_barras = ctk.CTkButton(self.frame_produtos2, 
                                                    text="", 
                                                    fg_color="#F8FCFF", 
                                                    hover_color="#9AA3AF", 
                                                    image= self.icon_copiar, 
                                                    command=self.copy_codigo_barras)
        self.btn_copy_codigo_barras.place(relwidth=0.07, relheight=0.7, relx=0.9, rely=0.2)

 

        #Adicionando Treeview --- style nao esta funcionando lembrar de arrumar
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Custom.Tree", background="lightgray", foreground="black", rowheight=50, font=('Helvetica', 30))
        self.style.configure("Custom.Treeview.Heading", font=('Helvetica', 12))
        self.tree_pesquisar = ttk.Treeview(self.frame_produtos3, columns=("id", "Nome", "Código de Barras", "Preço Unitario", "Quantidade de Estoque","Grupo", "Sub_grupo"),show="headings", height=20)
        self.tree_pesquisar.heading("id", text="id")
        self.tree_pesquisar.heading("Nome", text="Nome")
        self.tree_pesquisar.heading("Código de Barras", text="Código de Barras")
        self.tree_pesquisar.heading("Preço Unitario", text="Valor")
        self.tree_pesquisar.heading("Grupo", text="Grupo")
        self.tree_pesquisar.heading("Sub_grupo", text="Sub_grupo")
        self.tree_pesquisar.heading("Quantidade de Estoque", text="QTD")
        self.tree_pesquisar.column("id", width=20, anchor=tk.CENTER)
        self.tree_pesquisar.column("Nome", width=400)
        self.tree_pesquisar.column("Código de Barras", width=150, anchor= tk.CENTER)
        self.tree_pesquisar.column("Preço Unitario", width=100, anchor= tk.CENTER)
        self.tree_pesquisar.column("Grupo", width=150, anchor= tk.CENTER)
        self.tree_pesquisar.column("Sub_grupo", width=150, anchor= tk.CENTER)
        self.tree_pesquisar.column("Quantidade de Estoque", width=80, anchor= tk.CENTER)
        self.tree_pesquisar.bind("<Double-1>", self.abrir_edicao_item)  # Abrir edição ao clicar duas vezes
        self.tree_pesquisar.grid(row=0, column=0, sticky="nsew")
        # Criando a barra de rolagem saida
        self.scroll_bar = ctk.CTkScrollbar(self.frame_produtos3, orientation="vertical", command=self.tree_pesquisar.yview, bg_color="#FFFFFF")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        # Configurando a barra de rolagem para o Treeview saida
        self.tree_pesquisar.configure(yscrollcommand=self.scroll_bar.set)
        # Configurando pesos das colunas e linhas para expandir conforme o tamanho do frame
        self.frame_produtos3.grid_rowconfigure(0, weight=1)
        self.frame_produtos3.grid_columnconfigure(0, weight=1)
        





     # Label de mensagem de sucesso (inicialmente invisível)
        self.msg_label = ctk.CTkLabel(self.frame_produtos3, 
                                      text="", 
                                      text_color="white", 
                                      font=("Arial Bold", 22), 
                                      fg_color="#28a745", height=50)  # Verde (cor sólida)
        self.msg_label.place(relx=0.4, rely=0.7)
        
        # (Restante do seu código de configuração da janela)

    def copy_codigo_barras(self):
        # Verifica se há uma linha selecionada na Treeview
        selected_item = self.tree_pesquisar.selection()
        if selected_item:
            # Obtém o código de barras do item selecionado (assumindo que o código de barras está na coluna 2)
            codigo_barras = self.tree_pesquisar.item(selected_item, "values")[2]
            
            # Copia o código de barras para a área de transferência
            pyperclip.copy(codigo_barras)
            
            # Atualiza o texto da mensagem de confirmação
            self.msg_label.configure(text=f"Código de barras copiado!")
            
            # Faz a animação de fade-in
            self.fade_in()
            
            # Remove a mensagem após 3 segundos e inicia o fade-out
            self.after(1500, self.fade_out)
        else:
            # Caso nenhum item seja selecionado
            print("Nenhum item selecionado.")
    
    def fade_in(self, step=5, max_brightness=1.0):
        # Animação de fade-in (faz o fundo e o texto ficarem visíveis gradualmente)
        current_brightness = 0.2  # Começa com a cor mais clara
        def animate():
            nonlocal current_brightness
            if current_brightness < max_brightness:
                current_brightness += step / 100  # Aumenta a intensidade da cor gradualmente
                # Define a cor de fundo e do texto com base no brilho
                bg_color = self._adjust_brightness("#28a745", current_brightness)
                fg_color = self._adjust_brightness("white", current_brightness)
                self.msg_label.configure(fg_color=bg_color, text_color=fg_color)
                self.after(10, animate)  # Chama a animação novamente
        animate()

    def fade_out(self, step=5, min_brightness=0.2):
        # Animação de fade-out (faz o fundo e o texto desaparecerem gradualmente)
        current_brightness = 1.0  # Começa com a cor mais forte
        def animate():
            nonlocal current_brightness
            if current_brightness > min_brightness:
                current_brightness -= step / 100  # Diminui a intensidade da cor gradualmente
                # Define a cor de fundo e do texto com base no brilho
                bg_color = self._adjust_brightness("#28a745", current_brightness)
                fg_color = self._adjust_brightness("white", current_brightness)
                self.msg_label.configure(fg_color=bg_color, text_color=fg_color)
                self.after(10, animate)  # Chama a animação novamente
            else:
                # Após o fade-out, mantém a label visível com texto vazio
                self.msg_label.configure(text="")
        animate()

    def _adjust_brightness(self, color, brightness):
        # Converte a cor para hexadecimal se necessário
        if color.startswith('#'):
            color_hex = color
        else:
            color_hex = webcolors.name_to_hex(color)  # Converte o nome para hex

        # Ajusta o brilho de uma cor hexadecimal (sem manipular a transparência)
        color_hex = color_hex.lstrip("#")
        r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
        
        # Ajusta o brilho de cada componente da cor
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        
        # Retorna a nova cor ajustada
        return f"#{r:02x}{g:02x}{b:02x}"




    def pesquisar_item(self):
        opcao_pesquisa = self.combobox_1.get()
        termo_pesquisa = self.entry_pesquisar.get().strip()
        self.tree_pesquisar.delete(*self.tree_pesquisar.get_children())  # Limpar resultados anteriores
        if opcao_pesquisa == "Nome":
            # Pesquisar por nome
            try:
                self.sistema_estoque.c.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + termo_pesquisa + '%',))
                produtos = self.sistema_estoque.c.fetchall()
                for produto in produtos:
                    self.tree_pesquisar.insert("", tk.END, values=produto)
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao buscar item no estoque: {e}")
        elif opcao_pesquisa == "Código de Barras":
            # Pesquisar por código de barras
            try:
                self.sistema_estoque.c.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (termo_pesquisa,))
                produto = self.sistema_estoque.c.fetchone()
                if produto:
                    self.tree_pesquisar.insert("", tk.END, values=produto)
                else:
                    
                    messagebox.showinfo("Atenção", "Item não encontrado.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao buscar item no estoque: {e}")
        elif opcao_pesquisa == "Grupo":
            # Pesquisar por grupo
            try:
                self.sistema_estoque.c.execute("SELECT * FROM produtos WHERE grupo LIKE ?", ('%' + termo_pesquisa + '%',))
                produtos = self.sistema_estoque.c.fetchall()
                for produto in produtos:
                    self.tree_pesquisar.insert("", tk.END, values=produto)
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao buscar item no estoque: {e}")
                








    def fechar_janela(self):
        if hasattr(self, 'root_edicao') and self.root_edicao:
            self.root_edicao.destroy()  # Destrói a janela de edição se existir
        self.destroy()  # Destrói a janela principal


    def abrir_edicao_item(self, event):
        item_selecionado = self.tree_pesquisar.selection()
        if item_selecionado:
            if not self.edicao_aberta:
                valores_item = self.tree_pesquisar.item(item_selecionado)['values']
                id_produto = valores_item[0]

                # Cria a janela de edição
                self.root_edicao = TelaEdicaoItem(self, "db/db_file.db", id_produto)
                self.edicao_aberta = True  # Marca a janela de edição como aberta

                # Atualiza a propriedade para fechar a janela de edição
                self.root_edicao.protocol("WM_DELETE_WINDOW", self.fechar_edicao)
                self.root_edicao.grab_set()  # Faz a janela de edição modal
            else:
                messagebox.showinfo("Atenção", "A janela de edição já está aberta.")
        else:
            messagebox.showinfo("Atenção", "Por favor, selecione um item para editar.")

    def fechar_edicao(self):
        self.edicao_aberta = False  # Marca a janela de edição como fechada
        self.root_edicao.destroy()  # Fecha a janela de edição
    def excluir_produto(self):
        selected_item = self.tree_pesquisar.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um item para excluir.")
            return

        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este item?")
        if confirmacao:
            item_data = self.tree_pesquisar.item(selected_item)
            id_produto = item_data['values'][0]

            self.tree_pesquisar.delete(selected_item)  # Remove o item da árvore

            self.sistema_estoque.excluir_produto(id_produto)  # Remove o item do banco de dados
            #self.atualizar_grupos()        




if __name__ == "__main__":
    db_file = "db/db_file.db"
    conn = sqlite3.connect(db_file)
    app = JanelaProduto(db_file)  # Passar root e db_file como argumentos
    app.mainloop()