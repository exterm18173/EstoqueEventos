import tkinter as tk
import customtkinter as ctk
from assets.icons import carregar_imagens

# Função para criar a Splash Screen
def show_splash_screen():
    icon = carregar_imagens()
    icon_carregar = icon["carregar_sistema"]  # Logo da Splash Screen
    
    splash = tk.Tk()
    splash.title("Splash Screen")
    
    splash_width = 400
    splash_height = 400
    splash.geometry(f"{splash_width}x{splash_height}")
    splash.configure(bg="white")
    
    splash.overrideredirect(True)
    
    # Carregar logo
    logo_label = ctk.CTkLabel(splash, text="", image=icon_carregar, fg_color="white")
    logo_label.pack(pady=20)
    
    # Barra de progresso
    barra_progresso = ctk.CTkProgressBar(splash, width=250, height=20, progress_color="green", mode="determinate")
    barra_progresso.pack(pady=20)
    
    # Label de porcentagem
    label_percentual = ctk.CTkLabel(splash, text="0%", fg_color="white", font=("Arial", 14))
    label_percentual.pack(pady=5)
    
    barra_progresso.set(0)
    
    splash.attributes("-topmost", True)
    splash.attributes("-transparentcolor", "white")
    
    # Centralizar a janela
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    position_top = int(screen_height / 2 - splash_height / 2)
    position_left = int(screen_width / 2 - splash_width / 2)
    splash.geometry(f"+{position_left}+{position_top}")
    
    progress_value = 0

    def update_progress():
        nonlocal progress_value
        if progress_value < 100:
            progress_value += 1
            barra_progresso.set(progress_value / 100)
            label_percentual.configure(text=f"{progress_value}%")
            splash.after(30, update_progress)
        else:
            splash.destroy()

    splash.after(100, update_progress)

    splash.mainloop()

# Função principal (aplicação)
def main_application():
    root = tk.Tk()
    root.title("Sistema Principal")
    root.geometry("400x300")

    label = tk.Label(root, text="Sistema Principal Carregado", font=("Helvetica", 14))
    label.pack(expand=True)

    root.mainloop()

# Exibir a Splash Screen
show_splash_screen()

# Iniciar a aplicação principal
main_application()
