import time
import os
import pandas as pd
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import WAIT_TIME, SEARCH_URL
from scraping.cookies import save_cookies, load_cookies
from bots.user_actions import simulate_human_actions

def verify_and_inject_cookies(driver):
    try:
        cookies_file = 'src/data/cookies.json'
        if os.path.exists(cookies_file):
            print("Cargando cookies desde el archivo...")
            cookies = load_cookies(driver, cookies_file)

            if not cookies:
                print("No se encontraron cookies válidas.")
                return
            
            for cookie in cookies:
                cookie_domain = cookie.get("domain", "")
                driver_domain = driver.current_url.split('/')[2] 
                
                if driver_domain.startswith('www.'):
                    driver_domain = driver_domain[4:]

                #print("cookie domain ", cookie_domain)
                #print("driver domain", driver_domain)

                if cookie_domain and driver_domain in cookie_domain:
                    driver.add_cookie(cookie)
                else:
                    print(f"Dominio no coincide para la cookie: {cookie_domain}")
            print("Cookies inyectadas con éxito.")
        else:
            print("No se encontraron cookies guardadas.")
    except Exception as e:
        print(f"Error al verificar o inyectar cookies: {e}")

def build_search_url(checkin_date, checkout_date, location):
    """
    Construye dinámicamente el URL de búsqueda con las fechas y ubicación.
    """
    search_url = SEARCH_URL.format(location=location, checkin=checkin_date, checkout=checkout_date)
    return search_url

def collect_hotel_data(driver, checkin_date, checkout_date, location):
    """
    Recoge la información de las ofertas de hoteles en la página actual.
    """
    hotel_cards = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
    hotels_list = []

    for card in hotel_cards:
        try:
            name = card.find_element(By.XPATH, './/div[@data-testid="title"]').text
            price = card.find_element(By.XPATH, './/span[@data-testid="price-and-discounted-price"]').text
            
            try:
                score_element = card.find_element(By.XPATH, './/div[@data-testid="review-score"]/div[1]')
                score = score_element.text.split(':')[-1].strip()
            except:
                try:
                    score_element = card.find_element(By.XPATH, './/div[@data-testid="external-review-score"]/div[1]')
                    score = score_element.text.split()[-1].strip()
                except:
                    score = "N/A"

            try:
                review_count_element = card.find_element(By.XPATH, './/div[@data-testid="review-score"]/div[2]/div[2]')
                review_count = int(review_count_element.text.split()[0])
            except:
                try:
                    review_count_element = card.find_element(By.XPATH, './/div[@data-testid="external-review-score"]/div[2]/div[2]')
                    review_count = int(review_count_element.text.split()[0])
                except:
                    try:
                        new_booking_element = card.find_element(By.XPATH, './/span[contains(text(), "Nuevo en Booking.com")]')
                        review_count = 0  
                    except:
                        review_count = 0  

            hotels_list.append({
                "Localizacion": location,
                "Fecha de entrada": checkin_date,
                "Fecha de salida": checkout_date,
                "Hotel": name,
                "Precio": price,
                "Puntuación": score,
                "Opiniones": review_count
            })
        except Exception as e:
            print(f"Error al procesar una tarjeta: {e}")
    
    return hotels_list

def verify_login_success(driver):
    """
    Verifica si el inicio de sesión fue exitoso.
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Mi cuenta" and @data-testid="header-profile"]'))
        )
        print("Inicio de sesión exitoso. Guardando cookies...")
        return True
    except Exception:
        print("No se encontró el elemento 'Mi cuenta', verificando otras opciones...")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@aria-label, "Menú de tu cuenta:")]'))
        )
        print("Se encontró Menú de la cuenta. Guardando cookies...")
        return True
    except Exception as e:
        print("Error al verificar el inicio de sesión:", e)
        return False

def click_search_button(driver):
    """
    Hace clic en el botón de buscar en la página de resultados.
    """
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="e22b782521 d12ff5f5bf"]/button[@type="submit"]'))
        )
        search_button.click()
        print("Clic en el botón de buscar.")
    except Exception as e:
        print(f"Error al hacer clic en el botón de buscar: {e}")

def get_search_location(driver):
    """
    Obtiene el valor del campo de entrada de búsqueda si no está vacío.
    """
    try:
        search_input = driver.find_element(By.XPATH, '//input[@name="ss"]')
        location_value = search_input.get_attribute("value")
        if location_value:
            return location_value
    except Exception as e:
        print(f"Error al obtener el valor del campo de búsqueda: {e}")
    return None

def scrape_offers(driver, checkin_date, checkout_date, location):
    """
    Realiza el scraping de ofertas de hoteles después de iniciar sesión y cargar las cookies.
    """
    driver.get("https://www.booking.com")
    time.sleep(WAIT_TIME)

    verify_and_inject_cookies(driver)

    search_url = build_search_url(checkin_date, checkout_date, location)
    print(f"Buscando ofertas en: {search_url}")
    driver.get(search_url)
    time.sleep(WAIT_TIME)

    click_search_button(driver)

    if not verify_login_success(driver):
        driver.quit()
        return []

    save_cookies(driver, 'src/data/cookies.json')

    hotels_list = collect_hotel_data(driver, checkin_date, checkout_date, location)

    search_location = get_search_location(driver)
    if search_location:
        location = search_location

    file_name = f"{location}-{checkin_date.replace('-', '')}-{checkout_date.replace('-', '')}.xlsx"
    file_path = os.path.join('src/data', file_name)

    df = pd.DataFrame(hotels_list)
    df.to_excel(file_path, index=False)
    print(f"Datos guardados en '{file_path}'.")

    return hotels_list