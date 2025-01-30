import sqlite3

def selecionar_data(data_saida,label_data,group_var,combo_cliente_saida):
    # Obtém a data selecionada
    date = data_saida.get_date()
    label_data.configure(text=date)

    # Converte a data para o formato desejado (dd/mm/yyyy)
    formatted_date = date  # Certifique-se de formatar a data

    # Carrega eventos correspondentes ao banco de dados
    carregar_eventos(formatted_date, group_var,combo_cliente_saida)

    
def carregar_eventos(data, group_var,combo_cliente_saida):
    # Conecta ao banco de dados
    conn = sqlite3.connect('db/db_file.db')
    c = conn.cursor()
        
    # Busca eventos com a data selecionada ou "Todas as datas"
    c.execute("SELECT nome FROM eventos WHERE data = ? OR data = ?", (data, "Todas as datas"))
    eventos = c.fetchall()
    # Atualiza o OptionMenu com os eventos encontrados
    group_var.set("NEW PALACE EVENTOS")  # Reseta o valor padrão
    menu = combo_cliente_saida["menu"]
    menu.delete(0, "end")  # Limpa as opções existentes

    for evento in eventos:
        menu.add_command(label=evento[0], command=lambda value=evento[0]: group_var.set(value))
        
    if not eventos:
        group_var.set("Nenhum evento encontrado")

    conn.close()
def selecionar_data_entrada (data_entrada, label_data_entrada):
    date = data_entrada.get_date()
    label_data_entrada.configure(text=date)