class Produto:
    def __init__(self, id_produto, nome, codigo_barras, preco_unitario, quantidade_estoque, grupo, sub_grupo):
        self.id_produto = id_produto
        self.nome = nome
        self.codigo_barras = codigo_barras
        self.preco_unitario = preco_unitario
        self.quantidade_estoque = quantidade_estoque
        self.grupo = grupo
        self.sub_grupo = sub_grupo
