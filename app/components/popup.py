import flet as ft

def show_popup(page: ft.Page, title: str, message: str):
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
    )
    page.dialog = dialog
    dialog.open = True
    page.update()

def show_popup_auto_close(page: ft.Page, title: str, message: str):
    show_popup(page, title, message)

def show_snackbar(page: ft.Page, title: str, message: str, bgcolor: str = None):
    # Combinamos el título y el mensaje para que se vea bien en la barrita
    texto = f"{title}: {message}" if title else message
    
    snack = ft.SnackBar(content=ft.Text(texto), bgcolor=bgcolor)
    page.snack_bar = snack
    snack.open = True
    page.update()

def confirm_dialog(page: ft.Page, title: str, message: str, on_confirm):
    def close_dialog(e):
        dialog.open = False
        page.update()

    def confirm(e):
        close_dialog(e)
        if on_confirm:
            on_confirm()

    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Sí", on_click=confirm),
            ft.TextButton("No", on_click=close_dialog),
        ],
    )
    page.dialog = dialog
    dialog.open = True
    page.update()


def close_popup(page: ft.Page):
    # Verificamos si existe la propiedad dialog tradicional
    if hasattr(page, "dialog") and page.dialog:
        page.dialog.open = False
        page.update()
    else:
        # Si se abrió usando page.show_dialog, se cierra así:
        try:
            page.close_dialog()
        except:
            pass