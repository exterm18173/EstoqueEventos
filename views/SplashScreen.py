from assets.icons import carregar_imagens
import customtkinter as ctk

class SplashScreen:
    def __init__(self, master):
        self.splash = master
        self.splash.title("Splash Screen")
        self.splash.geometry("400x400")
        self.splash.configure(bg="white")
        self.splash.overrideredirect(True)
        
        self.icon_carregar = carregar_imagens()["carregar_sistema"]
        
        self.logo_label = ctk.CTkLabel(self.splash, text="", image=self.icon_carregar, fg_color="white")
        self.logo_label.pack(pady=20)
        
        self.barra_progresso = ctk.CTkProgressBar(self.splash, width=250, height=20, progress_color="green", mode="determinate")
        self.barra_progresso.pack(pady=20)
        
        self.label_percentual = ctk.CTkLabel(self.splash, text="0%", fg_color="white", font=("Arial", 14))
        self.label_percentual.pack(pady=5)
        
        self.progress_value = 0
        self.barra_progresso.set(self.progress_value / 100)
    
    def update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            self.barra_progresso.set(self.progress_value / 100)
            self.label_percentual.configure(text=f"{self.progress_value}%")
            self.splash.after(30, self.update_progress)
        else:
            self.splash.destroy()
