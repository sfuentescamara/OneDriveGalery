import flet as ft
from controllers import login_button_click, logout_button_click, on_change_nav
from components import components

def nav_bar(page: ft.Page):
    destinations = [
        ft.NavigationBarDestination(icon=ft.icons.PERSON_ROUNDED, label="Perfil"),
        ft.NavigationBarDestination(icon=ft.icons.INSERT_PHOTO, label="Fotos"),
        ft.NavigationBarDestination(
            icon=ft.icons.BOOKMARK_BORDER,
            selected_icon=ft.icons.BOOKMARK,
            label="Explorar"
        ),
    ]

    nav_bar = ft.NavigationBar(
        destinations=destinations,
        on_change=lambda e: on_change_nav(e, destinations)
    )
    return nav_bar


def vista_login(page: ft.Page):
    boton_login = ft.ElevatedButton("Iniciar Sesión", on_click=lambda e: login_button_click(e, page))

    return ft.Column([boton_login], alignment=ft.MainAxisAlignment.CENTER)


def vista_principal(page: ft.Page):
    
    return ft.Column([
        ft.Text("Bienvenido a la App"),
        ft.ElevatedButton("Cerrar Sesión", on_click=lambda e: logout_button_click(e, page)),
        nav_bar(page)
    ], alignment=ft.MainAxisAlignment.CENTER)

def vista_explorador(page: ft.Page):
    grid = components.FoldersView(page)
    
    return ft.Column([
        grid,
        nav_bar(page)
    ], alignment=ft.MainAxisAlignment.CENTER)


def vista_explorador1(page: ft.Page):
    """Muestra un explorador de archivos basado en los datos de la API"""

    lista_archivos = ft.Column()

    def actualizar_vista():
        """Carga archivos desde la API y actualiza la vista"""
        files = cargar_archivos(page)
        lista_archivos.controls.clear()  # Limpiar lista anterior
        folders = []
        images = []
        others = []
        for file in files:
            if "folder" in file:
                folders.append(file)
                # icono = ft.icons.FOLDER
            else:
                others.append(file)
                # icono = ft.icons.INSERT_DRIVE_FILE

        container = components.folders_view(page, folders)
        lista_archivos.controls.append(container)
        page.update()

    actualizar_vista()  # Llamar una vez para cargar la vista

    return ft.Column([
        ft.Text("Explorador de Archivos", size=20, weight=ft.FontWeight.BOLD),
        lista_archivos,
        nav_bar(page)
    ], alignment=ft.MainAxisAlignment.CENTER)
