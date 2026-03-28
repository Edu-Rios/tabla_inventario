# app/views/nuevo_editar.py
import flet as ft
from app.components.popup import show_popup

def formulario_nuevo_editar_producto(page: ft.Page, on_submit, initial: dict | None = None):
    initial = initial or {}
    titulo = ft.Text("Editar producto" if initial.get("id") else "Nuevo producto")

    name = ft.TextField(label="Nombre", value=initial.get("name", ""))
    quantity = ft.TextField(label="Cantidad", value=str(initial.get("quantity", 0)))
    ingreso_date = ft.TextField(label="Ingreso (YYYY-MM-DD)", value=initial.get("ingreso_date", ""))
    min_stock = ft.TextField(label="Stock mínimo", value=str(initial.get("min_stock", 0)))
    max_stock = ft.TextField(label="Stock máximo", value=str(initial.get("max_stock", 0)))

    def close():
        dlg.open = False
        page.update()

    # ¡Fíjate que ya no dice "async def", solo "def"!
    def save(e):
        print("1. Botón guardar presionado") # Esto saldrá en tu terminal
        if not name.value.strip():
            show_popup(page, "Validación", "El nombre es obligatorio.")
            return

        try:
            data = {
                "name": name.value.strip(),
                "quantity": int(quantity.value),
                "ingreso_date": ingreso_date.value.strip(),
                "min_stock": int(min_stock.value),
                "max_stock": int(max_stock.value),
            }
        except ValueError:
            show_popup(page, "Validación", "Cantidad y stocks deben ser números enteros.")
            return

        print("2. Datos listos, enviando a la base de datos...") # Esto saldrá en tu terminal
        on_submit(data)

    btn_cancelar = ft.TextButton("Cancelar", on_click=lambda e: close())
    # Le quitamos el run_task, ahora el botón llama a save directamente
    btn_guardar = ft.Button("Guardar", on_click=save)

    dlg = ft.AlertDialog(
        modal=False, 
        title=titulo, 
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True,
                controls=[name, quantity, ingreso_date, min_stock, max_stock],
            ),
        ),
        actions=[btn_cancelar, btn_guardar],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_():
        page.show_dialog(dlg)

    return dlg, open_, close