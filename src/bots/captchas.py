from selenium.webdriver.common.by import By 
import requests
import time

API_KEY = 'dcd85933530c4a0c9d2fe6c78ad5c09d'

def solve_aws_waf_captcha(driver, url):
    try:
        captcha_element = driver.find_element(By.CSS_SELECTOR, 'awswaf-captcha')
        if not captcha_element:
            print("No se encontró el elemento del CAPTCHA.")
            return None
        print("Elemento by css CAPTCHA encontrado.")
        time.sleep(70)

        captcha_image_url = captcha_element.get_attribute("src")
        print("URL de la imagen CAPTCHA:", captcha_image_url)

    except Exception as e:
        print("Error al obtener el CAPTCHA:", e)
        return None

    print("Enviando CAPTCHA a Anti-Captcha...")
    response = requests.post(
        "https://api.anti-captcha.com/createTask",
        json={
            "clientKey": API_KEY,
            "task": {
                "type": "ImageToTextTask",
                "body": requests.get(captcha_image_url).content.decode('base64')
            }
        }
    )

    if response.json().get("errorId") != 0:
        print("Error al enviar CAPTCHA:", response.json())
        return None

    task_id = response.json().get("taskId")
    print("CAPTCHA enviado con Task ID:", task_id)

    for _ in range(20):  
        time.sleep(5)
        result = requests.post(
            "https://api.anti-captcha.com/getTaskResult",
            json={
                "clientKey": API_KEY,
                "taskId": task_id
            }
        )
        result_json = result.json()

        if result_json.get("status") == "ready":
            print("CAPTCHA resuelto:", result_json.get("solution").get("text"))
            return result_json.get("solution").get("text")

        print("Esperando resolución del CAPTCHA...")

    print("Error: Tiempo de espera agotado.")
    return None
