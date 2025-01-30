import customtkinter as ctk

def mostrar_tela_carregamento(master, maximo=100):
    """Exibe uma tela de carregamento com uma barra de progresso usando customtkinter, adaptada ao tema (claro ou escuro)"""
    
    # Verifica o tema atual
    tema_atual = ctk.get_appearance_mode()  # 'light' ou 'dark'

    # Cria a janela de carregamento
    tela = ctk.CTkToplevel(master)
    tela.title("Carregando...")
    
    # Tamanho menor da tela
    largura_tela = 300
    altura_tela = 100
    tela.geometry(f"{largura_tela}x{altura_tela}")
    tela.resizable(False, False)
    tela.grab_set()  # Desabilita interação com a janela principal
    
    # Centraliza a janela de carregamento no centro da tela do computador
    largura_master = master.winfo_screenwidth()
    altura_master = master.winfo_screenheight()
    pos_x = int((largura_master - largura_tela) / 2)
    pos_y = int((altura_master - altura_tela) / 2)
    tela.geometry(f"{largura_tela}x{altura_tela}+{pos_x}+{pos_y}")

    # Adiciona um fundo mais bonito à janela, dependendo do tema
    if tema_atual == "dark":
        tela.configure(bg="#2f2f2f")  # Fundo escuro para tema escuro
    else:
        tela.configure(bg="#f5f5f5")  # Fundo claro para tema claro

    # Barra de progresso adaptada ao tema
    barra_progresso = ctk.CTkProgressBar(tela, width=250, height=20, progress_color="green", mode="determinate")
    barra_progresso.grid(row=0, column=0, padx=20, pady=20)

    # Exibe a porcentagem ao lado da barra de progresso, com a cor adaptada ao tema
    if tema_atual == "dark":
        label_percentual = ctk.CTkLabel(tela, text="0%", fg_color="#2f2f2f", text_color="white", font=("Arial", 14))
    else:
        label_percentual = ctk.CTkLabel(tela, text="0%", fg_color="#f5f5f5", text_color="black", font=("Arial", 14))
    
    label_percentual.grid(row=1, column=0)

    # Inicializa a barra de progresso com 0%
    barra_progresso.set(0)

    tela.update()  # Garante que a tela seja desenhada antes de continuar
    return tela, barra_progresso, label_percentual
