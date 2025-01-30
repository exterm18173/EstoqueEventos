

import sqlite3
import xml.etree.ElementTree as ET
from db.database import SistemaEstoque





def extrair_salvar_nfe(arquivo_nome):
        
        tree = ET.parse(arquivo_nome)
        root = tree.getroot()
        namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        
        # Extrai as informações necessárias do XML
        dhEmi = root.find('.//nfe:infNFe/nfe:ide/nfe:dhEmi', namespace).text
        xFant = root.find('.//nfe:infNFe/nfe:emit/nfe:xFant', namespace)
        xNome = root.find('.//nfe:infNFe/nfe:emit/nfe:xNome', namespace)
        vPag = root.find('.//nfe:infNFe/nfe:pag/nfe:detPag/nfe:vPag', namespace).text
        
        # Definir o nome do fornecedor
        if xFant is None:
            nome_fornecedor = xNome.text
        else:
            nome_fornecedor = xFant.text
        
        # Chama a função para salvar no banco de dados
        print(dhEmi, nome_fornecedor, vPag, arquivo_nome)
        SistemaEstoque.salvar_nfe_no_banco(dhEmi, nome_fornecedor, vPag, arquivo_nome)