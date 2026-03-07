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

def show_snackbar(page: ft.Page, message: str):
    snack = ft.SnackBar(content=ft.Text(message))
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