import os
import queue
import sqlite3
from tkinter import messagebox
class SistemaEstoque:
    def __init__(self, db_file, parent=None):
        self.parent = parent
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.c = self.conn.cursor()
        self._criar_tabelas()
        self.result_queue = queue.Queue()
        
    def _criar_tabelas(self):
        # Criar as tabelas no banco de dados
        self.c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            codigo_barras TEXT NOT NULL,
                            preco_unitario REAL NOT NULL,
                            quantidade_estoque INTEGER NOT NULL,
                            grupo TEXT NOT NULL,
                            sub_grupo TEXT NOT NULL
                        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS movimentacoes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome_item TEXT NOT NULL,
                            codigo_barras TEXT NOT NULL,
                            valor_movimento INTEGER NOT NULL,
                            quantidade_movimento INTEGER NOT NULL,
                            tipo_movimento TEXT,
                            data_movimento TEXT,
                            grupo_movimento TEXT NOT NULL,
                            sub_grupo_movimento TEXT NOT NULL,
                            cliente_movimento TEXT
                        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS grupo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL
                        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS sub_grupo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sub_nome TEXT NOT NULL
                        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT NOT NULL,
                            senha TEXT NOT NULL,
                            email TEXT NOT NULL,
                            tipo_usuario TEXT NOT NULL,
                            ipv4_usuario TEXT NOT NULL
                        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS eventos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            tipo TEXT NOT NULL,
                            data TEXT NOT NULL
                        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS xml_import (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome_arquivo TEXT,
                            nome_fantasia TEXT,
                            data_emissao TEXT,
                            valor_total TEXT,
                            conteudo_xml BLOB
                        )''')
        self.conn.commit()

    def saida_produto(self, produto, quantidade, data, cliente_selecionado):
        try:
            self.c.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (produto.codigo_barras,))
            produto_db = self.c.fetchone()
            if produto_db:
                id_produto, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo = produto_db
                if quantidade_estoque >= quantidade:
                    self.c.execute("INSERT INTO movimentacoes (nome_item, codigo_barras, valor_movimento, quantidade_movimento, tipo_movimento, data_movimento, grupo_movimento, sub_grupo_movimento, cliente_movimento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (nome, codigo_barras, preco_unitario, quantidade, 'saida', data, grupo, sub_grupo, cliente_selecionado))
                    self.conn.commit()
                    nova_quantidade_estoque = round(quantidade_estoque - quantidade, 3)
                    self.c.execute("UPDATE produtos SET quantidade_estoque = ? WHERE codigo_barras = ?",
                                    (nova_quantidade_estoque, produto.codigo_barras))
                    self.conn.commit()
                else:
                    messagebox.showinfo("Atenção", f"Quantidade insuficiente em estoque para o produto <b>{nome}</b>.")
            else:
                messagebox.showinfo("Atenção", "Produto não encontrado.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao registrar saída de produto: {e}")

    def entrada_produto(self, produto, quantidade, data, cliente_selecionado):
        try:
            self.c.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (produto.codigo_barras,))
            produto_db = self.c.fetchone()
            if produto_db:
                id_produto, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo = produto_db
                self.c.execute("INSERT INTO movimentacoes (nome_item, codigo_barras, valor_movimento, quantidade_movimento, tipo_movimento, data_movimento, grupo_movimento, sub_grupo_movimento, cliente_movimento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (nome, codigo_barras, preco_unitario, quantidade, 'entrada', data, grupo, sub_grupo, cliente_selecionado))
                self.conn.commit()
                nova_quantidade_estoque = round(quantidade_estoque + quantidade, 3)
                self.c.execute("UPDATE produtos SET quantidade_estoque = ? WHERE codigo_barras = ?",
                                (nova_quantidade_estoque, produto.codigo_barras))
                self.conn.commit()
            else:
                messagebox.showinfo("Atenção", "Produto não encontrado.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao registrar entrada de produto: {e}")

    def devolucao_produto(self, produto, quantidade, data, cliente_selecionado_dev):
        try:
            self.c.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (produto.codigo_barras,))
            produto_db = self.c.fetchone()
            if produto_db:
                id_produto, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo = produto_db
                self.c.execute("INSERT INTO movimentacoes (nome_item, codigo_barras, valor_movimento, quantidade_movimento, tipo_movimento, data_movimento, grupo_movimento, sub_grupo_movimento, cliente_movimento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (nome, codigo_barras, preco_unitario, quantidade, 'devolucao', data, grupo, sub_grupo, cliente_selecionado_dev))
                self.conn.commit()
                nova_quantidade_estoque = round(quantidade_estoque + quantidade, 3)
                self.c.execute("UPDATE produtos SET quantidade_estoque = ? WHERE codigo_barras = ?",
                                (nova_quantidade_estoque, produto.codigo_barras))
                self.conn.commit()
            else:
                messagebox.showinfo("Atenção", "Produto não encontrado.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao registrar devolução de produto: {e}")
    def adicionar_produto(self, produto):
        # Verifica se o código de barras já existe no banco de dados
        self.c.execute("SELECT * FROM produtos WHERE codigo_barras=?", (produto.codigo_barras,))
        if self.c.fetchone() is not None:
            # Se encontrar um registro, mostra mensagem de erro
            messagebox.showinfo("Atenção", "Código de barras duplicado. Produto não adicionado.", parent=self.parent)
        else:
            # Se não encontrar, realiza a inserção
            try:
                self.c.execute("INSERT INTO produtos (nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo) VALUES (?, ?, ?, ?, ?, ?)",
                               (produto.nome, produto.codigo_barras, produto.preco_unitario, produto.quantidade_estoque, produto.grupo, produto.sub_grupo))
                self.conn.commit()
                messagebox.showinfo("Atenção", "Produto adicionado com sucesso.", parent=self.parent)
            except sqlite3.IntegrityError:
                messagebox.showinfo("Atenção", "Erro ao adicionar produto.", parent=self.parent)

    def gerar_codigo_barras(self, entry_codigo_barras):
        self.c.execute("SELECT codigo_barras FROM produtos WHERE codigo_barras LIKE '77_________' ORDER BY codigo_barras DESC LIMIT 1")
        ultimo_codigo = self.c.fetchone()
        if ultimo_codigo:
            ultimo_numero = int(ultimo_codigo[0][2:])
            novo_numero = ultimo_numero + 1
        else:
            novo_numero = 1
        novo_codigo = f"77{str(novo_numero).zfill(9)}"
        entry_codigo_barras.delete(0, 'end')
        entry_codigo_barras.insert(0, novo_codigo)

    def gerar_codigo_barras_kg(self, entry_codigo_barras):
        self.c.execute("SELECT codigo_barras FROM produtos WHERE codigo_barras LIKE '77_____' ORDER BY codigo_barras DESC LIMIT 1")
        ultimo_codigo = self.c.fetchone()
        if ultimo_codigo:
            ultimo_numero = int(ultimo_codigo[0][2:])
            novo_numero = ultimo_numero + 1
        else:
            novo_numero = 1
        novo_codigo = f"77{str(novo_numero).zfill(5)}"
        entry_codigo_barras.delete(0, 'end')
        entry_codigo_barras.insert(0, novo_codigo)
    def consultar_produto(self, codigo_barras):
        """Consulta o banco de dados para obter as informações de um produto pelo código de barras."""
        if not codigo_barras.startswith("2") and 4 <= len(codigo_barras) <= 14:
           self.c.execute("SELECT nome, preco_unitario, grupo, sub_grupo FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
        else:
            codigo_barras = codigo_barras[:7]
            self.c.execute("SELECT nome, preco_unitario, grupo, sub_grupo FROM produtos WHERE codigo_barras LIKE ?", (f"{codigo_barras}%",))
        return self.c.fetchone()
    def obter_preco_por_kg_saida(self, codigo_item):
        try:
            self.c.execute("SELECT preco_unitario FROM produtos WHERE codigo_barras = ?", (codigo_item,))
            preco_unitario = self.c.fetchone()
            if preco_unitario:
                return preco_unitario[0]
            else:
                return None
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar preço por kg: {e}")
            return None
        
    def filtrar_movimentacoes(self, nome_item, tipo_movimentacao, data):
        try:
            query = "SELECT id, nome_item, codigo_barras, quantidade_movimento, tipo_movimento, data_movimento, grupo_movimento, sub_grupo_movimento, cliente_movimento FROM movimentacoes WHERE nome_item LIKE ? AND tipo_movimento LIKE ? AND data_movimento LIKE ?"
            self.c.execute(query, ('%' + nome_item + '%', tipo_movimentacao, data))
            movimentacoes_filtradas = self.c.fetchall()
            return movimentacoes_filtradas
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao filtrar movimentações: {e}")

    def _obter_movimentacao_original(self, item_id):
        self.c.execute("SELECT tipo_movimento, quantidade_movimento, codigo_barras FROM movimentacoes WHERE id = ?", (item_id,))
        return self.c.fetchone()

    def _atualizar_movimentacao(self, item_id, tipo_movimento, data_movimento):
        query_atualizacao = "UPDATE movimentacoes SET tipo_movimento = ?, data_movimento = ? WHERE id = ?"
        self.c.execute(query_atualizacao, (tipo_movimento, data_movimento, item_id))
        self.conn.commit()
    def _ajustar_estoque_entrada_devolucao(self, quantidade_movimento_original, codigo_barras):
        ajuste_estoque = 2 * quantidade_movimento_original
        self.c.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque + ? WHERE codigo_barras = ?", (ajuste_estoque, codigo_barras))
        self.conn.commit()

    def _ajustar_estoque_saida(self, quantidade_movimento_original, codigo_barras):
        ajuste_estoque = 2 * quantidade_movimento_original
        self.c.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque - ? WHERE codigo_barras = ?", (ajuste_estoque, codigo_barras))
        self.conn.commit()
    def excluir_produto(self, id_produto):
        try:
            self.c.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
            self.conn.commit()
            messagebox.showinfo("Atenção", "Item excluído com sucesso.", parent=self.parent)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir item do banco de dados: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao excluir item do banco de dados: {e}") 
    

    def obter_grupos(self):
        """Obtém a lista de grupos diretamente do banco de dados."""
        self.c.execute("SELECT nome FROM grupo")
        itens = [item[0] for item in self.c.fetchall()]
        return itens
    def obter_subgrupos(self):
        """Obtém a lista de grupos diretamente do banco de dados."""
        self.c.execute("SELECT sub_nome FROM sub_grupo")
        itens = [item[0] for item in self.c.fetchall()]
        return itens



    def salvar_nfe_no_banco(dhEmi, nome_fornecedor, vPag, arquivo_nome):
        conn = sqlite3.connect('db/db_file.db')
        c = conn.cursor()
        
        # Salvar o conteúdo do XML como Blob
        with open(arquivo_nome, 'rb') as file:
            blob_data = file.read()
        
        # Inserir os dados na tabela xml_import
        c.execute(''' 
            INSERT INTO xml_import (nome_arquivo, nome_fantasia, data_emissao, valor_total, conteudo_xml) 
            VALUES (?, ?, ?, ?, ?)
        ''', (os.path.basename(arquivo_nome), nome_fornecedor, dhEmi, vPag, blob_data))
        
        conn.commit()
        conn.close()

    def adicionar_atualizar_produto(self, nome, codigo_barras, preco_unitario, quantidade, grupo, sub_grupo):
        conn = sqlite3.connect('db/db_file.db')
        c = conn.cursor()
        try:
            if codigo_barras == "SEM GTIN":
                # Verificar se o produto já existe no estoque pelo nome
                c.execute("SELECT COUNT(*) FROM produtos WHERE nome = ?", (nome,))
                if c.fetchone()[0] > 0:
                    # Produto já existe, então apenas atualize a quantidade em estoque
                    c.execute('''UPDATE produtos SET quantidade_estoque = quantidade_estoque + ?, preco_unitario = ?
                                WHERE nome = ?''', (quantidade, preco_unitario,nome))
                else:
                    # Produto não existe, então adicione um novo produto
                    c.execute('''INSERT INTO produtos (nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo)
                                VALUES (?, ?, ?, ?, ?, ?)''', (nome, codigo_barras, preco_unitario, quantidade, grupo, sub_grupo))
            else:
                # Verificar se o produto já existe no estoque pelo código de barras
                c.execute("SELECT COUNT(*) FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
                if c.fetchone()[0] > 0:
                    # Produto já existe, então apenas atualize a quantidade em estoque
                    c.execute('''UPDATE produtos SET quantidade_estoque = quantidade_estoque + ?, preco_unitario = ?
                                WHERE codigo_barras = ?''', (quantidade, preco_unitario, codigo_barras))
                else:
                    # Produto não existe, então adicione um novo produto
                    c.execute('''INSERT INTO produtos (nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo)
                                VALUES (?, ?, ?, ?, ?, ?)''', (nome, codigo_barras, preco_unitario, quantidade, grupo, sub_grupo))
        except sqlite3.Error as e:
            print("Erro ao adicionar ou atualizar produto:", e)
        finally:
            conn.commit()
            conn.close()




    def verificar_produto(self, nome, codigo_barras):
        

        if codigo_barras == "SEM GTIN":
            self.c.execute("SELECT COUNT(*) FROM produtos WHERE nome = ?", (nome,))
            if self.c.fetchone()[0] > 0:
                self.c.execute("SELECT codigo_barras, preco_unitario, grupo, sub_grupo FROM produtos WHERE nome = ?", (nome,))
                produto = self.c.fetchone()
                
                return "atualizar", produto  # Produto encontrado, precisa ser atualizado
            else:
                
                return "novo", None  # Produto não encontrado, precisa ser inserido
        elif str(codigo_barras).startswith("2") and len(str(codigo_barras)) == 13:
            codigo_item = "2" + str(codigo_barras)[6:12]
            self.c.execute("SELECT COUNT(*) FROM produtos WHERE nome = ?", (nome,))
            if self.c.fetchone()[0] > 0:
                self.c.execute("SELECT codigo_barras, preco_unitario, grupo, sub_grupo FROM produtos WHERE nome = ?", (nome,))
                produto = self.c.fetchone()
               
                return "atualizar", produto
            else:
                
                return "novo", None
        else:
            self.c.execute("SELECT COUNT(*) FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
            if self.c.fetchone()[0] > 0:
                self.c.execute("SELECT nome, preco_unitario, grupo, sub_grupo FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
                produto = self.c.fetchone()
                
                return "atualizar", produto
                
            else:
                
                return "novo", None
    def persistir_produtos(self, items_novos, items_atualizados):
        # Inserir novos produtos
        for item in items_novos:
            self.c.execute(''' 
                INSERT INTO produtos (nome, codigo_barras, preco_unitario, quantidade, grupo, sub_grupo) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', item)

        # Atualizar produtos existentes
        for item in items_atualizados:
            self.c.execute(''' 
                UPDATE produtos 
                SET codigo_barras = ?, preco_unitario = ?, quantidade_estoque = ?, grupo = ?, sub_grupo = ? 
                WHERE nome = ?
            ''', (item[1], item[2], item[3], item[4], item[5], item[0]))
