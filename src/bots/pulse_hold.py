from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class Bots:
    @staticmethod
    def handle_robot_verification(driver):
        try:
            time.sleep(20)
            hold_button = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@role="button" and @aria-label="Pulsa y mantén"]'))
            )
            
            actions = ActionChains(driver)
            actions.click_and_hold(hold_button).perform()
            print("Manteniendo presionado el botón...")
            
            time.sleep(10)  
            actions.release().perform()
            print("Botón liberado.")
            
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element(hold_button)
            )
            print("Verificación completada exitosamente.")

        except Exception as e:
            print(f"No se encontró botón o Error al manejar el botón de verificación adicional")
