from tkinter import messagebox


def validar_quantidade(quantidade):
    """Valida se a quantidade inserida é um número válido e maior que zero."""
    try:
        quantidade = float(quantidade)
        if quantidade <= 0:
            raise ValueError
        return quantidade
    except ValueError:
        return None

def format_number(num):
    parte_inteira = int(abs(num))

    if parte_inteira < 10:
        code = num * 100000000000
        bar_code = f"0{int(code):012}"
        return bar_code
    elif parte_inteira < 100:
        code = num * 100000000000
        bar_code = f"{int(code):012}"
        return bar_code
    else:
        messagebox.showinfo("Erro", "Peso inválido")
        return None