import flet as ft
from controllers import FolderController, slider_changed
from . import utils
from typing import List

def create_image_grid_and_date(date_labels, image_grid):
    
    image_grid_and_date = [
        # Barra lateral con fechas
        # ft.Container(
        #     ft.Column(date_labels, spacing=10),
        #     width=100,  # Ancho fijo para las fechas
        #     alignment=ft.alignment.top_left
        # ),

        # Scroll de imágenes
        ft.Container(
            content=ft.ListView(
                controls=image_grid,
                spacing=10, 
                expand=True
            ),
            expand=True,
            # height=500,  # Altura del contenedor
            padding=10
        )
    ]

    return image_grid_and_date


def FoldersView(page: ft.Page):
    controller = FolderController(page)
    image_grid_and_date: ft.Column = ft.Column() # Contiene columna fechas e imágenes
    # date_labels: List[ft.Text] = [] # Contiene columna fechas 
    # image_grid: List[ft.ResponsiveRow] = [] # Contiene todas las imágenes
    # image_group: List[ft.Container] = [] # Contiene las imágenes de los grupos de fechas
    n_photos = 3
    grid_by_date = ft.GridView(expand=True, runs_count=n_photos)


    def items_collector(i, item, folders, files, images):
        if 'folder' in item.keys():
            folder = FolderItem(item, controller.navigate_to, update_folders, lambda x: print(f"Detalles de {x}"), page)
            folders.append(folder)
        if 'file' in item.keys():
            file = collect_file_group_image(item, images, i, page)
            if file is not None:
                files.append(file)

    def update_folders(items, current_folder):
        
        """Actualiza la vista con nuevas carpetas"""
        folders, files, images = [], [], {} # temporal store
        grid_items.controls.clear() # grid folders and files
        image_grid_and_date.controls.clear() # grid image and dates
        grid_by_date.controls.clear()
        date_labels = []
        image_grid = []
        slider_photos_size.controls.clear()

        if current_folder is not None:
            back_item = FolderBack(current_folder, controller.navigate_to, update_folders, lambda x: print(f"Detalles de {x}"), page)
            grid_items.controls.append(back_item)
        for i, item in enumerate(items):
            items_collector(i, item, folders, files, images)
            
        ######
        # Update Folder/items Grid
        if len(folders) > 0:
            grid_items.controls.extend(folders)
        if len(files) > 0:
            grid_items.controls.extend(files)
        ######
        # Update slider
        if len(images.keys()):
            slider_photos_size.controls.append(
                ft.Slider(value=3,
                    min=1, max=10, divisions=10, label="{value}%", on_change=lambda e: slider_changed(e, grid_by_date, n_photos)
                ))

        ######
        # Update images Grid
        for date, imgs in images.items():
            # date bar
            date_labels.append(ft.Text(date, size=16, weight=ft.FontWeight.BOLD))
            # images row
            grid_by_date.controls=imgs
            image_grid.append(ft.Column([ft.Text(date, size=20), grid_by_date], spacing=5))

        # # image_grid_and_date.controls.extend(create_image_grid_and_date(date_labels, image_grid))
        image_grid_and_date.controls.extend(image_grid)
        # if len(images) > 0:
            # TO DEBUG:
            # grid_by_date = ft.GridView(expand=True, runs_count=3, controls=[imgs[0],imgs[2]])
            # image_grid_and_date.controls = [ft.Column([ft.Text(date, size=20), grid_by_date], spacing=0), ft.Column([ft.Text(date, size=20), imgs[2]], spacing=0)]
        page.update()


    grid_items = ft.GridView(
        expand=True, 
        # height=50,
        runs_count=2,
        # max_extent=150,
        child_aspect_ratio=5.0,
        spacing=5,
        run_spacing=2
    )
    slider_photos_size = ft.Row([])
    image_grid_and_date = ft.Column([])

    grids = ft.Column([grid_items, slider_photos_size, image_grid_and_date],
        scroll="always",
        expand=True)

    page.run_task(controller.load_folders, update_folders)

    return grids


class FolderItem(ft.Container):
    """Componente de Carpeta"""
    def __init__(self, details, on_open, update_folders, on_details, page):
        super().__init__()
        self.all_info = details
        self.folder_name = details['name']
        self.on_open = on_open
        self.update_folders = update_folders
        self.on_details = on_details
        self.page = page

        self.content = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.MORE_VERT,  # Icono de tres puntos ⋮
                    on_click=lambda e: self.on_details(self.folder_name),
                ),
                ft.Text(self.folder_name, size=self.page.width * 0.02, weight=ft.FontWeight.BOLD, expand=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.padding = 10
        self.width = self.page.width / 2
        # self.height = 2
        self.border_radius = 10
        self.bgcolor = ft.colors.BLUE_300
        self.alignment = ft.alignment.center
        self.on_click = lambda e: self.on_open(self.all_info, self.update_folders)

class FolderBack(FolderItem):
    def __init__(self, current_folder, on_open, update_folders, on_details, page):
        if current_folder is not None:
            current_folder['name'] = ".."
            self.details = current_folder
        else:
            self.details = {'name': "..",
                            'parentReference': {'path': '/'}}
        # print(f"Current folder: {self.details['name']}")
        super().__init__(self.details, on_open, update_folders, on_details, page)

def collect_file_group_image(item, image_dict, i, page):
    try:
        if item['file']['mimeType'].split("/")[0] == 'image':
            img = FileImage(page, item, i)
            if 'photo' in item and 'takenDateTime' in item['photo']:
                date = item['photo']['takenDateTime'].split('T')[0]
            elif 'createdDateTime' in item:
                date = item['createdDateTime'].split('T')[0]
            else:
                date = ""
            date = utils.nice_dates(date)
            if date not in image_dict:
                image_dict[date] = []
            image_dict[date].append(img)
            return None
        else:
            item = FileItem(item, None, None, lambda x: print(f"Detalles de {x}"), page)
        return item
    except Exception as error:
        print(f"Error: {error}")

class FileItem(ft.Container):
    """Componente de Carpeta"""
    def __init__(self, details, on_open, update_folders, on_details, page):
        super().__init__()
        self.all_info = details
        self.folder_name = details['name']
        # self.on_open = on_open
        # self.update_folders = update_folders
        self.on_details = on_details
        self.page = page

        self.content = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.MORE_VERT,  # Icono de tres puntos ⋮
                    on_click=lambda e: self.on_details(self.folder_name),
                    scale=ft.transform.Scale(0.5),
                    alignment=ft.alignment.center
                ),
                ft.Text(self.folder_name, size=self.page.width * 0.02, expand=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.padding = 10
        self.width = self.page.width / 2
        # self.height = 2
        self.border_radius = 10
        self.bgcolor = ft.colors.GREY_300
        self.alignment = ft.alignment.center
        # self.on_click = lambda e: self.on_open(self.all_info, self.update_folders)

class FileImage(ft.Container):
    def __init__(self, page, item, i=0):
        super().__init__()
        thumbnail_medium = FileImage.get_image_thumbnail(item, "medium")
        thumbnail_large = FileImage.get_image_thumbnail(item, "large")
        self.content = ft.Image (
            src = thumbnail_medium, # Miniatura de tamaño medio
            data = thumbnail_large, # Imagen de mayor resolución
            fit = ft.ImageFit.COVER,
        )
        # self.col={"md": 4}
        # self.col={"xs": 6, "sm": 4, "md": 3}
        # self.expand=True
        # self.width = page.photo_size
        self.border_radius = ft.border_radius.all(2)
        self.page = page  # Guardar referencia a la página
        self.on_click = self.open_image  # Asignar directamente la función
        self.bgcolor="#44CCCC00"

    @staticmethod
    def get_image_thumbnail(item, scale):
        """ Obtiene la URL de la imagen en resolución baja (si existe). """
        if "thumbnails" in item and item["thumbnails"]:
            return item["thumbnails"][0].get(scale, {}).get("url", "")
        return ""
    
    def open_image(self, e):
        print("On_click working!")
        """Abre un diálogo con la imagen en alta resolución"""
        self.page.dialog = ft.AlertDialog(
            content=ft.Image(src=self.data, fit=ft.ImageFit.CONTAIN),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: close_dialog(e))]
        )
                
        def close_dialog(e):
            self.page.dialog.open = False
            e.control.page.update()

        self.page.dialog.open = True
        self.page.update()

        
        # e.control.page.overlay.append(dialog)
        # dialog.open = True
        # e.control.page.update()
