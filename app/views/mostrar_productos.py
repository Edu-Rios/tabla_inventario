import flet as ft
from typing import Any
from app.services.transacciones_api_productos import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos_estilos, Card

def products_view(page:ft.Page) -> ft.Control:
    rows_data: list[dict[str, Any]]=[]
    total_items=0
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos_estilos.H4)
    #Encabezados
    columnas=[
        ft.DataColumn(label=ft.Text("Nombre", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Min", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Max", style=Textos_estilos.H4)),
    ]

    #Se definen las filas de la tabla
    #Cada data.append agrega
    # Se define la lista de datos vacía
    data = []
    try:
        # Mandamos a llamar a tu API
        respuesta_api = list_products()
        
        # Extraemos la lista de productos que viene guardada dentro de 'items'
        productos_reales = respuesta_api.get("items", [])
        
        # Actualizamos el texto usando el 'total' que ya te manda tu API
        total_text.value = f"Total de productos: {respuesta_api.get('total', 0)}"

        # Hacemos el ciclo ahora sí sobre los productos reales
        for prod in productos_reales:
            data.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(prod.get("name", "")))),
                        ft.DataCell(ft.Text(str(prod.get("quantity", "")))),
                        ft.DataCell(ft.Text(str(prod.get("ingreso_date", "")))),
                        ft.DataCell(ft.Text(str(prod.get("min_stock", "")))),
                        ft.DataCell(ft.Text(str(prod.get("max_stock", "")))),
                    ]
                )
            )
                
    except Exception as e:
        total_text.value = f"Error al cargar productos: {e}"




    #Se crea la tabla con los encabezados(columnas) y los datos de prueba(data)
    tabla=ft.DataTable(
        columns=columnas,
        rows=data,
        width=900,
        heading_row_height=60,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
        data_row_min_height=48
    )

    # return tabla

    # Regresa la tabla con los datos
    # return tabla

    # Se prepara un sistema de columnas para mostrar tanto el total de registros y
    # la tabla y con un mejor formato
    # Cuando se necesita el scroll también se muestra
    contenido = ft.Column(
        # Se crea un espacio entra cada elemento
        spacing=30,
        # Cuando no caben los elementos se genera el scroll
        scroll=ft.ScrollMode.AUTO,
        # Se establecen tanto el total como la tabla para mostrar
        controls=[total_text, ft.Container(content=tabla)]
    )

    # Se muestra esa columna
    return contenido