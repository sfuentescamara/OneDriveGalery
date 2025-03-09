from views import vista_login, vista_principal, vista_explorador

def configurar_rutas(page):
    page.views.clear()  # Limpiar historial de navegación

    if page.route == "/login":
        page.views.append(vista_login(page))
    elif page.route == "/home" or page.route == "/":
        page.views.append(vista_principal(page))
    elif page.route == "/fotos":
        page.views.append(vista_principal(page))
    elif page.route == "/perfil":
        page.views.append(vista_principal(page))
    elif page.route == "/explorar":
        page.views.append(vista_explorador(page))

    
    page.update()
