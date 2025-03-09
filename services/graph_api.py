import httpx

async def get_drive(headers):
    """ Obtiene los archivos de las carpetas root personal y compatidos """
    files = []
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    urlShared = "https://graph.microsoft.com/v1.0/me/drive/sharedWithMe"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{url}", headers=headers)
        responseShared = await client.get(f"{urlShared}", headers=headers)
    try:
        data = response.json() if response.status_code == 200 else []
        files = data["value"]  # La lista de archivos está en la clave "value"
        dataShared = responseShared.json() if response.status_code == 200 else []
        filesShared = dataShared["value"] 
        files.extend(filesShared)
        # for file in files:
        #     print(f"Nombre: {file['name']}")
        #     print(f"Tipo: {file.get('file', {}).get('mimeType', 'Carpeta')}")  # Maneja el caso de carpetas
        #     print(f"Tamaño: {file.get('size', 'Desconocido')}")
        #     print(f"ID: {file['id']}")
        #     print("-" * 20)
    except Exception as error:
        print("ERROR: ", error)

    return files

def get_url(all_info, current_path):
    """ Busca que tipo de url tiene que enviar """
    if 'parentReference' in all_info and all_info['parentReference']['driveType'] == 'personal':
        print(all_info['parentReference']['path'])
        root = all_info['parentReference']['path'].split('/')[1]
        item_id = all_info['id']
        if root == "drives":
            # Shared folders
            drive_id = all_info['parentReference']['driveId']
            url = f"drives/{drive_id}/items/{item_id}/children?$expand=thumbnails"
        else:
            # Personal
            url = f"me/drive/items/{item_id}/children?$expand=thumbnails"
    elif 'remoteItem' in all_info:
        # Shared root
        drive_id = all_info['remoteItem']['parentReference']['driveId']
        item_id = all_info['remoteItem']['id']
        url = f"drives/{drive_id}/items/{item_id}/children?$expand=thumbnails"
    return url


async def get_folders(page, path="/", all_info=""):
    """Obtiene las carpetas dentro de una ruta dada"""
    headers = {
    "Authorization": f"Bearer {page.session.get("token")}"
    }
    if path[-1] == "/":
        # Retorna los archivos del directorio principal
        files = await get_drive(headers)
        return files
    
    # Retorna los archivos de las subcarpetas
    url = "https://graph.microsoft.com/v1.0/"
    url += f"{path[-1]}"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{url}", headers=headers)
        # print(f"Status code: {response.status_code}")
        data = response.json() if response.status_code == 200 else []
        files = data["value"]

    return files
