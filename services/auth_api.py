
from fastapi import Request 
import flet as ft
import urllib.parse
import requests

import configparser
config = configparser.ConfigParser()
try:
    config.read('./config.cfg')
    azure_settings = config['azure1']
except Exception:
    config.read('./OneDriveSDK/config.cfg')
    azure_settings = config['azure1']


CLIENT_ID = azure_settings['clientId']
CLIENT_SECRET = azure_settings['client_credential']
REDIRECT_URI = azure_settings['REDIRECT_URI']
graphUserScopes = ["User.Read"] #azure_settings['graphUserScopes'].split()
AUTHORIZE_ENDPOINT = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"

token = None


def obtener_token(page: ft.Page):
    """Obtiene el token almacenado localmente"""
    return page.client_storage.get("token")

def guardar_token(page: ft.Page, token: str):
    """Guarda el token de sesión y en almacenamiento local"""
    page.session.set("token", token)
    # page.client_storage.set("token", token)

def eliminar_token():
    """Elimina el token del usuario"""
    global token
    token = None
    # os.environ.pop("USER_TOKEN", None)
    # if os.path.exists(TOKEN_FILE):
    #     os.remove(TOKEN_FILE)

def esta_autenticado(page: ft.Page):
    """Retorna True si hay un token guardado"""
    return obtener_token(page) is not None

def on_login(event, page):
    toggle_login_buttons(event, page)

def on_logout(event, page):
    token = None
    toggle_login_buttons(event, page)
    page.go('/login')

def toggle_login_buttons(event, page):
    event.visible = token is None
    event.visible = token is not None

def build_authorize_url(event, page):
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(graphUserScopes)#, # Scopes separados por espacio
        # "state": "your_state_value_random" # Reemplaza con un valor state real para seguridad
    }
    authorize_url = AUTHORIZE_ENDPOINT + "?" + urllib.parse.urlencode(params)
    return authorize_url


def exchange_code_for_token(code):
    token_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'} # Importante para el endpoint /token
    try:
        response = requests.post(TOKEN_ENDPOINT, headers=headers, data=token_params) # Petición POST a /token
        response.raise_for_status() # Lanza una excepción para códigos de error HTTP (4xx o 5xx)
        return response.json() # Parsea la respuesta JSON
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for token: {e}") # Log de errores
        return {"error_description": str(e)} # Devuelve info de error para mostrar en la UI

# def guardar_token(token):
    # page.client_storage.set("access_token", token)


async def handle_token(request: Request):
    global token
    code = request.query_params.get("code")
    if code:
        print(f"Authorization code received!") # Log
        token_response = exchange_code_for_token(code) # Intercambia el código por tokens
        if token_response and "access_token" in token_response:
            token = token_response["access_token"] # Guarda el access token
            print("Login Successful (manual requests)!")
        else:
            print(f"Token exchange failed: {token_response.get('error_description', 'Unknown error')}")
    return token
