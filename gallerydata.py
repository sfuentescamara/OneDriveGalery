import importlib.util
import os
import sys
from os.path import isfile, join
from pathlib import Path

import flet as ft

class NavigationBar(ft.Row):
    def __init__(self):
        super().__init__()
        self.destinations = [
            ft.NavigationBarDestination(icon=ft.icons.PERSON_ROUNDED, label="Perfil"),
            ft.NavigationBarDestination(icon=ft.icons.INSERT_PHOTO, label="Fotos"),
            ft.NavigationBarDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Explore"
            ),
        ]
    
        self.bar = ft.NavigationBar(
            destinations=self.destinations,
            on_change=self.on_change_nav
        )
    
    def get_bar(self):
        return self.bar

    def on_change_nav(self, e):
        selected_index = e.control.selected_index
        selected_destination = self.destinations[selected_index].label
        # self.container.content = ft.Column([self.navigation_bar, self.views[selected_destination]]) # Actualiza el contenido del contenedor
        # self.container.update()  # Fuerza la actualización del contenedor
        # self.page.update() # Actualiza la página
        e.page.go(selected_destination.lower())

class Container(ft.Container):
    def __init__(self, text): 
        super().__init__()
        self.content = ft.Text(text)

class PerfilContainer(ft.Container):
    def __init__(self, text): 
        super().__init__()
        self.content = ft.Text(text)
        self.logged = False
        if self.page.custom_auth.token is not None:
            logged = True

    
                
        # LOGIN
        def login_button_click(e):
            e.page.custom_auth.login_button_click(e)

        def logout_button_click(e):
            e.page.custom_auth.logout_button_click(e)

        def show_state(e):
            if e.page.custom_auth.token is None:
                logged.value = "No logged" 
            else:
                logged.value = "Logged" 
            e.page.update()

        logged = ft.Text()
        state_button = ft.ElevatedButton("State", on_click=show_state)
        logout_button = ft.ElevatedButton("Logout", on_click=logout_button_click)
        login_button = ft.ElevatedButton("Login OneDrive", on_click=login_button_click)

        self.controls = ft.Column(controls=[logged, state_button, login_button, logout_button])


class MainContainer(ft.Row):
    def __init__(self): 
        super().__init__()
        self.container = Container("MainContainer")
        self.views = {
            "perfil" : PerfilContainer("LOGIN"),
            "fotos": Container("fotos"),
            "explore": Container("explore")
        }
        self.expand = True
        self.controls = [
            self.container
        ]

    def display_contianer(self, name):
        """ Display contianer whit name """
        self.controls = []
        self.container = self.views[name]
        self.controls = [
            self.container
        ]
        self.page.update()


class GridItem:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.files = []
        self.description = None
