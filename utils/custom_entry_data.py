import customtkinter as ctk
import re

class CustomEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<KeyRelease>", self.format_date)

    def format_date(self, event):
        current_text = self.get()
        current_text = re.sub(r'[^0-9/]', '', current_text)  # Remove caracteres que não são números ou barras
        current_text = re.sub(r'/', '', current_text)  # Remove todas as barras existentes
        if len(current_text) > 8:  # Limita a quantidade máxima de caracteres para formar uma data
            current_text = current_text[:8]
        formatted_text = ""
        for i, char in enumerate(current_text):
            if i in [2, 4]:  # Adiciona uma barra nas posições corretas
                formatted_text += "/"
            formatted_text += char
        self.delete("0", "end")
        self.insert("0", formatted_text)
         