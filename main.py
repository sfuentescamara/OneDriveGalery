import asyncio
import logging

import flet as ft
import flet.version
import flet.fastapi as flet_fastapi
from fastapi import Request
from fastapi.responses import RedirectResponse
import uvicorn

from routes import configurar_rutas
from services.auth_api import esta_autenticado, handle_token, guardar_token

# from v1.services.auth import Auth
from gallerydata import NavigationBar, MainContainer

logging.basicConfig(level=logging.INFO)

app = flet_fastapi.FastAPI()
app.state.page = None

@app.get("/oauth_callback")
async def oauth_callback(request: Request):
    token = await handle_token(request)

    if app.state.page:
        guardar_token(app.state.page, token)
    
    return RedirectResponse("http://localhost:8550/home")

def main(page: ft.Page):
    # Guardamos la referencia a page en FastAPI
    app.state.page = page  

    page.title = "Flet controls gallery"
    # page.custom_auth = auth
    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        "RobotoSlab": "RobotoSlab[wght].ttf",
    }

    page.on_route_change = lambda _: configurar_rutas(page)

    
    if esta_autenticado(page):
        page.go("/home")  # Si ya hay sesión, ir directo a Home
    else:
        page.go("/login")  # Si no hay sesión, ir a Login

    # def get_route_list(route):
    #     route_list = [item for item in route.split("/") if item != ""]
    #     return route_list

    # def route_change(e):
    #     route_list = get_route_list(page.route)
    #     if len(route_list) == 0:
    #         pass
    #     elif len(route_list) == 1:
    #         container.display_contianer(route_list[0])
    #         # container.update()
    #     elif len(route_list) == 2:
    #         pass
    #     print(f"RUTA CAMBIADA A : {route_list}")

    page.appbar = ft.AppBar(
        leading=ft.Container(padding=5, content=ft.Image(src=f"logo.svg")),
        leading_width=40,
        title=ft.Text("OneDrive"),
        center_title=True,
        bgcolor=ft.Colors.INVERSE_PRIMARY,
        actions=[
            ft.Container(
                padding=10, content=ft.Text(f"Flet version: {flet.version.version}")
            )
        ],
    )

    page.theme_mode = ft.ThemeMode.LIGHT
    page.on_error = lambda e: print("Page error:", e.data)
    
    # page.on_login = auth.on_login
    # page.on_logout = auth.on_logout
    # page.navigation_bar = NavigationBar().get_bar()
    # container = MainContainer()
    # page.add(container)
    # page.on_route_change = route_change
    # print(f"Initial route: {page.route}")
    # page.go(page.route)

app.mount("/", flet_fastapi.app(main))

uvicorn.run(app=app, host="localhost", port=8550)
