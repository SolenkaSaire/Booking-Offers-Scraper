import sys
import os
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from bots.login_bot import login_to_booking
from scraping.scraper import scrape_offers
from scraping.proxies import configure_driver_with_proxy_extension 

def configure_driver_without_proxy():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")  
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def read_scraping_tasks(file_path):
    tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                location, checkin_date, checkout_date = parts
                tasks.append((location, checkin_date, checkout_date))
    return tasks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py [login|scrape] <archivo_tareas>")
        sys.exit(1)

    command = sys.argv[1]

    # Inicializar el driver con proxy
    #driver = configure_driver_with_proxy_extension()
    driver = configure_driver_without_proxy()
    if not driver:
        print("Error al configurar el driver con proxy. Verifica la configuración.")
        sys.exit(1)

    try:
        if command == "login":
            print("Iniciando el proceso de inicio de sesión...")
            login_to_booking(driver)
            print("Proceso de inicio de sesión finalizado.")
        elif command == "scrape":
            if len(sys.argv) < 3:
                print("Uso: python main.py scrape src/config/<archivo_tareas>")
                sys.exit(1)

            tasks_file = sys.argv[2]
            tasks = read_scraping_tasks(tasks_file)
            all_hotels_data = []

            for location, checkin_date, checkout_date in tasks:
                print(f"Iniciando el proceso de scraping para {location} del {checkin_date} al {checkout_date}...")
                hotels_data = scrape_offers(driver, checkin_date, checkout_date, location)
                all_hotels_data.extend(hotels_data)
                print(f"Proceso de scraping finalizado para {location} del {checkin_date} al {checkout_date}.")

            df = pd.DataFrame(all_hotels_data)
            df.to_csv('src/data/hotels_data.csv', index=False)
            df.to_excel('src/data/hotels_data.xlsx', index=False)
            print("Todos los datos de hoteles guardados en 'src/data/hotels_data.csv'.")
        else:
            print("Comando no reconocido. Uso: python main.py [login|scrape] <archivo_tareas>")
            sys.exit(1)
    except Exception as e:
        print(f"Error durante la ejecución del comando '{command}': {e}")
    finally:
        driver.quit()