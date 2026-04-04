# app/views/nuevo_editar.py
import flet as ft
from app.components.popup import show_popup, show_snackbar
from app.styles.estilos import Colors

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

    def save(e):
        print("1. Validando formulario...")
        if not name.value.strip():
            print("ERROR DE VALIDACIÓN: El nombre está vacío")
            show_snackbar(page, "Validación", "El nombre es obligatorio.", bgcolor=Colors.DANGER)
            return

        try:
            data = {
                "name": name.value.strip(),
                "quantity": int(quantity.value),
                "ingreso_date": ingreso_date.value.strip(),
                "min_stock": int(min_stock.value),
                "max_stock": int(max_stock.value),
            }
        except ValueError as exc:
            print(f"ERROR DE VALIDACIÓN: Un valor numérico es inválido. Detalles: {exc}")
            show_snackbar(page, "Validación", "Cantidad y stocks deben ser números enteros.", bgcolor=Colors.DANGER)
            return

        print("2. Formulario correcto, enviando a procesar...")
        # Ejecuta la función que se mandó desde mostrar_productos
        on_submit(data)

    btn_cancelar = ft.TextButton("Cancelar", on_click=lambda e: close())
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