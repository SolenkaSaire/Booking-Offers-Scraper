import json

def save_cookies(driver, file_path):
    cookies = driver.get_cookies()
    with open(file_path, 'w') as file:
        json.dump(cookies, file)

def load_cookies(driver, file_path):
    try:
        with open(file_path, 'r') as file:
            cookies = json.load(file)
            if not isinstance(cookies, list):
                raise ValueError("El archivo de cookies no contiene una lista válida.")
            return cookies
    except Exception as e:
        print(f"Error al cargar las cookies desde el archivo: {e}")
        return [] 