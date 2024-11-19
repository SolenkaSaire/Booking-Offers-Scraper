from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import LOGIN_URL, USER_EMAIL, USER_PASS
from scraping.cookies import load_cookies, save_cookies
from .email_reader import get_verification_link
from .pulse_hold import Bots as pulse_hold
from .user_actions import simulate_human_actions
import random
import time
import os

def load_cookies_if_exist(driver, cookies_file):
    if os.path.exists(cookies_file):
        driver.get(LOGIN_URL)
        load_cookies(driver, cookies_file)
        driver.refresh()
        print("Cookies cargadas, sesión iniciada automáticamente.")
        return True
    return False

def navigate_to_login_page(driver):
    driver.get(LOGIN_URL)
    time.sleep(random.uniform(2, 5))
    print("Accediendo a inicio de sesión...")

    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Inicia sesión")]'))
        )
        login_button.click()
    except Exception as e:
        print(f"Error al encontrar el botón de inicio de sesión: {e}")
        return False
    return True

def enter_email(driver):
    try:
        simulate_human_actions(driver)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_input.send_keys(USER_EMAIL)
        print("Email ingresado.")

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        print("Clic en continuar.")
        continue_button.click()
    except Exception as e:
        print(f"Error al ingresar el email o hacer clic en continuar: {e}")
        return False
    return True

def handle_captcha(driver):
    try:
        time.sleep(5)
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'awswaf-captcha'))
        )
        print("Captcha detectado, esperando 30 segundos para que lo resuelvas manualmente...")
        time.sleep(30)
    except Exception as e:
        print("Captcha no presente o error al manejar el captcha:")
    return True

def handle_verification(driver):
    try:
        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "nw-link-sign-in-without-pass")]//span[contains(text(), "Iniciar sesión con enlace de verificación")]'))
        )
        print("Botón de iniciar sesion con enlace de verificación encontrado.")
        verify_button.click()
        print("Clic en enviar enlace de verificación.")
    except Exception as e:
        print(f"Error al hacer clic en el botón de verificación: {e}")
        return False

    try:
        # Opción 1: bandeja
        inbox_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@class="osvS4MYxeSR4s9RPRMlw nw-step-header" and contains(text(), "Mira tu bandeja de entrada")]'))
        )
        if inbox_message:
            print("Enlace de verificación enviado al correo.")
            return True
    except Exception as e:
        print("No se encontró el mensaje de 'Mira tu bandeja de entrada', verificando otras opciones...")

    try:
        # Opción 2: número de intentos
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Has superado el número de intentos. Vuelve a probar más tarde.")]'))
        )
        if error_message:
            print("Número de intentos superado. Intentar con contraseña.")
            return False
    except Exception as e:
        print("No se encontró el mensaje de 'Has superado el número de intentos', continuando con el proceso de verificación por enlace.")

    return True

def enter_password(driver):
    try:
        
        simulate_human_actions(driver)
        time.sleep(10)
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password_input.send_keys(USER_PASS)
        print("Contraseña ingresada.")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        print("Clic en iniciar sesión.")
        time.sleep(5)
        login_button.click()

        try:
            time.sleep(5)
            error_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="password-note" and contains(@class, "error-block")]'))
            )
            if error_message:
                print("Error al ingresar la contraseña. Intentando nuevamente...")
                time.sleep(5)
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
                )
                login_button.click()
        except Exception as e:
            print("No se encontró el mensaje de error por combinación de email o contraseña.")
    except Exception as e:
        print(f"Error al ingresar la contraseña: {e}")
        return False
    
    try:
        time.sleep(5)
        print("Verificando si hay comprobación de robot...")
        pulse_hold.handle_robot_verification(driver)
    except Exception as e:
        print(f"Error al manejar la verificación de robot: {e}")
        return False
    return True

def handle_email_verification(driver):
    #pulse_hold.handle_robot_verification(driver)
    try:
        time.sleep(random.uniform(2, 5))
        time.sleep(random.uniform(2, 5))
        print("Esperando a que se envíe el enlace de verificación...")
        
        verification_link = get_verification_link(USER_EMAIL)
        if not verification_link:
            print("No se pudo recuperar el enlace de verificación.")
            return False

        driver.get(verification_link)
        print(f"Accediendo al enlace de verificación: {verification_link}")
    except Exception as e:
        print(f"Error al acceder al enlace de verificación: {e}")
        return False

    time.sleep(random.uniform(2, 5))
    return True

def login_to_booking(driver):
    cookies_file = 'src/data/cookies.json'

    if load_cookies_if_exist(driver, cookies_file):
        return

    if not navigate_to_login_page(driver):
        return

    if not enter_email(driver):
        return

    if not handle_captcha(driver):
        return

    #if not handle_verification(driver):
        
    if not enter_password(driver):
        return

    #if not handle_email_verification(driver):
    #    return

    save_cookies(driver, cookies_file)
    print("Inicio de sesión completado. Cookies guardadas.")