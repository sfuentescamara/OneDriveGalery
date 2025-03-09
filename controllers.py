from services.auth_api import build_authorize_url, on_logout
from services.graph_api import get_folders, get_url

def logout_button_click(event, page):
    on_logout(event, page)

def login_button_click(event, page):
    authorize_url = build_authorize_url(event, page)
    page.launch_url(authorize_url, web_window_name="_self")

def on_change_nav(e, destinations):
    selected_index = e.control.selected_index
    selected_destination = destinations[selected_index].label
    e.page.go(f"/{selected_destination.lower()}")

class FolderController:
    def __init__(self, page):
        self.page = page
        self.current_path = ["/"]

    async def load_folders(self, update_ui, all_info=None):
        """Carga las carpetas de la API y actualiza la vista"""
        if all_info is None:
            folders = await get_folders(self.page, self.current_path)
        else:
            folders = await get_folders(self.page, self.current_path, all_info)
        update_ui(folders, all_info)

    def navigate_to(self, all_info, update_ui):
        """Navega dentro de una carpeta y vuelve a cargar su contenido"""
        if all_info['name'] == "..":
            self.current_path.pop()
            if self.current_path == ['/']:
                all_info = None
        else:
            path = get_url(all_info, self.current_path)
            self.current_path.append(path)

        # print(self.current_path)
        self.page.update()
        self.page.run_task(self.load_folders, update_ui, all_info)


def slider_changed(e, grid_by_date, n_photos):
    print(f"Slider changed to {e.control.value}")
    grid_by_date.runs_count = int(e.control.value)
    grid_by_date.update()