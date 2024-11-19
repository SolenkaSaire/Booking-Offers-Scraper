import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def human_scroll(driver, max_scroll=5):
    for _ in range(random.randint(1, max_scroll)):
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(random.uniform(0.5, 1.5))

def random_click(driver, xpath):
    elements = driver.find_elements(By.XPATH, xpath)
    if elements:
        random.choice(elements).click()
        time.sleep(random.uniform(1, 2))

def scroll_up(driver, max_scroll=5):
    for _ in range(random.randint(1, max_scroll)):
        driver.execute_script("window.scrollBy(0, -300);")
        time.sleep(random.uniform(0.5, 1.5))

def scroll_down(driver, max_scroll=5):
    for _ in range(random.randint(1, max_scroll)):
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(random.uniform(0.5, 1.5))

def random_typing(driver, xpath, text="Lorem ipsum dolor sit amet"):
    elements = driver.find_elements(By.XPATH, xpath)
    if elements:
        element = random.choice(elements)
        element.click()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
        time.sleep(random.uniform(1, 2))

def random_wait(min_wait=1, max_wait=5):
    time.sleep(random.uniform(min_wait, max_wait))

def random_click_on_page(driver):
    width = driver.execute_script("return document.body.scrollWidth")
    height = driver.execute_script("return document.body.scrollHeight")
    x = random.randint(0, width)
    y = random.randint(0, height)
    driver.execute_script(f"document.elementFromPoint({x}, {y}).click();")
    time.sleep(random.uniform(1, 2))

def simulate_human_actions(driver):
    actions = [
        lambda: human_scroll(driver),
        lambda: scroll_up(driver),
        lambda: scroll_down(driver),
        lambda: random_click_on_page(driver),
        lambda: random_typing(driver, "//input"),
        lambda: random_wait()
    ]
    random.choice(actions)()