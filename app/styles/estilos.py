import flet as ft

class Colors:
    BG= "#EDEAEA"
    CARD = "#26378E"
    BORDER = "#26378E"
    TEXT = "#575758"
    PRIMARY = "#334ACA"
    SUCCESS = "047B08"
    INFO = "#04B4FA"
    DANGER = "#FF0000"
    WHITE = "#FFFFFF"
    BLACK = "#000000"

class Textos_estilos: # <-- Le cambiamos el nombre aquí
    H1=ft.TextStyle(size=26, height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H2=ft.TextStyle(size=20, height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H3=ft.TextStyle(size=14, height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H4=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color=Colors.TEXT) # <-- Agregamos el H4 que pide tu tabla
    text=ft.TextStyle(size=12, height=1.2, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)

class Inputs:
    INPUT_PRIMARY={
        "border_color": Colors.BORDER,
        "focused_border_color": Colors.PRIMARY,
        "cursor_color": Colors.PRIMARY,
        "width": 500,
        "text_style": Textos_estilos.text,  # <-- Actualizamos el nombre aquí también
        "label_style": Textos_estilos.text, # <-- Y aquí
        "bgcolor": Colors.BG,
    }

class Buttons:
    BUTTON_PRIMARY=ft.ButtonStyle(bgcolor=Colors.PRIMARY, color=Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8), padding=10)
    BUTTON_SUCCESS=ft.ButtonStyle(bgcolor=Colors.SUCCESS, color=Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8), padding=10)
    BUTTON_DANGER=ft.ButtonStyle(bgcolor=Colors.DANGER, color=Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8), padding=10)

class Card:
    tarjeta={
        "width": 6600,
        "padding": 16,
        "border_radius": 12,
        "bgcolor": Colors.BG,
        "border": ft.Border.all(2, Colors.BORDER)
    }