# app/views/mostrar_productos.py
import flet as ft
from typing import Any
from app.services.transacciones_api_productos import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos_estilos, Card
from app.views.nuevo_editar import formulario_nuevo_editar_producto

def products_view(page: ft.Page) -> ft.Control:

    total_text = ft.Text("Total de productos: (cargando...)", style=Textos_estilos.H4)
    
    columnas = [
        ft.DataColumn(label=ft.Text("Nombre", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Min", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Max", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Acciones", style=Textos_estilos.H4)), 
    ]

    # Preparamos la tabla vacía
    tabla = ft.DataTable(
        columns=columnas,
        rows=[],
        width=900,
        heading_row_height=60,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
        data_row_min_height=48
    )

    def actualizar_data(is_init: bool = False):
        try:
            respuesta_api = list_products(limit=100)
            productos_reales = respuesta_api.get("items", [])
            total_text.value = f"Total de productos: {respuesta_api.get('total', 0)}"
            
            nuevas_filas = []
            # Agregamos las filas nuevas
            for prod in productos_reales:
                nuevas_filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(prod.get("name", "")), style=Textos_estilos.text)),
                            ft.DataCell(ft.Text(str(prod.get("quantity", "")), style=Textos_estilos.text)),
                            ft.DataCell(ft.Text(str(prod.get("ingreso_date", "")), style=Textos_estilos.text)),
                            ft.DataCell(ft.Text(str(prod.get("min_stock", "")), style=Textos_estilos.text)),
                            ft.DataCell(ft.Text(str(prod.get("max_stock", "")), style=Textos_estilos.text)),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, p=prod: inicio_editar_producto(p)),
                                        # 👉 AQUÍ YA ESTÁ DESCOMENTADO EL BOTÓN DE BORRAR:
                                        ft.IconButton(icon=ft.Icons.DELETE, tooltip="Borrar", on_click=lambda e, p=prod: inicio_borrar_producto(p))
                                    ]
                                )
                            )
                        ]
                    )
                )
            
            tabla.rows = nuevas_filas
            
            # Solo forzar repintado si no es la carga inicial
            if not is_init:
                if getattr(tabla, "page", None):
                    tabla.update()
                if getattr(total_text, "page", None):
                    total_text.update()
                
                # Prevenir error si la página ya cerró o aún no está montada
                if page:
                    page.update()

        except Exception as e:
            print(f"Error al actualizar la tabla: {e}")

   
    def inicio_nuevo_producto(_e):
        def crear_nuevo_producto(data: dict): 
            try:
                print(f"Llamando create_product con api: {data}")
                create_product(data)
                show_snackbar(page, "Éxito", "Producto creado.", bgcolor=Colors.SUCCESS)
                close() 
                actualizar_data() # Recarga la tabla automáticamente
            except ApiError as ex:
                print("ApiError en create_product:", repr(ex))
                show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                print("Exception en create_product:", repr(ex))
                show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None)
        open_()

 
    def inicio_editar_producto(p: dict[str, Any]):
        def editar_producto(data: dict):
            try:
                print(f"Llamando update_product con api para ID {p.get('id')}: {data}")
                update_product(p["id"], data)
                show_snackbar(page, "Éxito", "Producto actualizado.", bgcolor=Colors.SUCCESS)
                close()
                actualizar_data() # Recarga la tabla automáticamente
            except ApiError as ex:
                print("ApiError en update_product:", repr(ex))
                show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                print("Exception en update_product:", repr(ex))
                show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=editar_producto, initial=p)
        open_()

  
    def borrar_producto(p: dict[str, Any]):
        try:
            print(f"Llamando delete_product con api para ID {p.get('id')}")
            delete_product(p["id"])
            show_snackbar(page, "Éxito", "Producto borrado.", bgcolor=Colors.SUCCESS)
            actualizar_data() # Recarga la tabla automáticamente
        except ApiError as ex:
            print("ApiError en delete_product:", repr(ex))
            show_popup(page, "Error", api_error_to_text(ex))
        except Exception as ex:
            print("Exception en delete_product:", repr(ex))
            show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

    def inicio_borrar_producto(p: dict[str, Any]):
        # Se ejecuta directamente, ya sin el "async" ni el "run_task"
        borrar_producto(p)


    btn_nuevo = ft.Button("Nuevo producto", icon=ft.Icons.ADD, on_click=inicio_nuevo_producto)
    
    # Llenamos la tabla por primera vez al abrir la aplicación indicando que es inicio
    actualizar_data(is_init=True)

    # Ensamblamos la pantalla
    contenido = ft.Column(
        spacing=30,
        scroll=ft.ScrollMode.AUTO,
        controls=[btn_nuevo, total_text, ft.Container(content=tabla)]
    )

    tarjeta = ft.Container(content=contenido, **Card.tarjeta)
    final = ft.Container(expand=True, alignment=ft.Alignment(0, -1), content=tarjeta)
    
    return final