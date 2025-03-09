import flet as ft

def update_images(image_listview, date_bar, new_images, page):
    """Actualiza la galería de imágenes y la barra de fechas"""

    image_listview.controls.clear()
    date_bar.controls.clear()
    grouped_images = {}

    # Agrupar imágenes por fecha (mes-año)
    for img in new_images:
        date = img["date"][:7]  # Extrae YYYY-MM
        if date not in grouped_images:
            grouped_images[date] = []
        grouped_images[date].append(img)

    # Crear la galería con Responsive Grid
    for date, imgs in grouped_images.items():
        row = ft.ResponsiveRow(
            [
                ft.Container(
                    content=ft.Image(src=img["src"], fit=ft.ImageFit.COVER),
                    width=150, height=150, border_radius=10, margin=5
                )
                for img in imgs
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        image_listview.controls.append(ft.Column([ft.Text(date, size=14), row], spacing=5))

    # Crear botones de fechas en la barra lateral
    for date in grouped_images.keys():
        btn = ft.IconButton(
            icon=ft.icons.CIRCLE,
            icon_color=ft.colors.BLUE,
            tooltip=date,
            on_click=lambda e, d=date: show_date_info(d, page)
        )
        date_bar.controls.append(btn)

    image_listview.update()
    date_bar.update()

def show_date_info(date, page):
    """Muestra un pequeño mensaje flotante con la fecha"""
    page.snack_bar = ft.SnackBar(
        content=ft.Text(f"📅 {date}", size=16),
        bgcolor=ft.Colors.BLACK,
        duration=1500  # Se muestra por 1.5 segundos
    )
    page.snack_bar.open = True
    page.update()

def main(page: ft.Page):
    page.title = "Galería de Imágenes"

    # Contenedor de imágenes (ListView con scroll)
    image_listview = ft.ListView(expand=True, spacing=5, padding=10)

    # Barra lateral de fechas
    date_bar = ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    # Contenedor principal con galería y barra lateral
    layout = ft.Row(
        [
            ft.Container(content=image_listview, expand=True),
            ft.Container(
                content=date_bar,
                width=50,
                alignment=ft.alignment.center_right,
                bgcolor=ft.colors.GREY_200,
                border_radius=ft.border_radius.all(10),
                padding=5
            )
        ],
        expand=True
    )

    page.add(layout)

    # Simulación de imágenes con fechas
    images = [
        {"src": "https://picsum.photos/200", "date": "2024-02-10"},
        {"src": "https://picsum.photos/201", "date": "2024-02-10"},
        {"src": "https://picsum.photos/202", "date": "2024-03-15"},
        {"src": "https://picsum.photos/203", "date": "2024-04-20"},
    ]

    update_images(image_listview, date_bar, images, page)

ft.app(target=main)
