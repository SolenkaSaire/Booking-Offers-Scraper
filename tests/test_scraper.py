import unittest
from unittest.mock import patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

from scraping.scraper import scrape_offers, collect_hotel_data
from bots.captchas import solve_aws_waf_captcha

class TestScraper(unittest.TestCase):

    @patch('scraping.scraper.WebDriverWait')
    @patch('scraping.scraper.webdriver.Chrome')
    def test_scrape_offers(self, MockChrome, MockWebDriverWait):
        # Configurar el mock del driver
        mock_driver = MockChrome.return_value
        mock_driver.find_elements.return_value = []

        # Configurar el mock de WebDriverWait
        mock_wait = MockWebDriverWait.return_value
        mock_wait.until.return_value = True

        # Llamar a la función de scraping
        result = scrape_offers(mock_driver, '2024-12-01', '2024-12-07', 'Buenos_Aires')

        # Verificar que el resultado es una lista vacía (ya que no hay elementos)
        self.assertEqual(result, [])

    @patch('scraping.scraper.WebDriverWait')
    @patch('scraping.scraper.webdriver.Chrome')
    def test_collect_hotel_data(self, MockChrome, MockWebDriverWait):
        # Configurar el mock del driver
        mock_driver = MockChrome.return_value
        mock_card = MagicMock()
        mock_card.find_element.side_effect = [
            MagicMock(text='Hotel Test'),
            MagicMock(text='COP 100.000'),
            MagicMock(text='Puntuación: 8,5'),
            MagicMock(text='100 comentarios')
        ]
        mock_driver.find_elements.return_value = [mock_card]

        # Llamar a la función de recolección de datos
        result = collect_hotel_data(mock_driver)

        # Verificar que el resultado contiene los datos esperados
        expected_result = [{
            "Hotel": 'Hotel Test',
            "Precio": 'COP 100.000',
            "Puntuación": '8,5',
            "Opiniones": 100
        }]
        self.assertEqual(result, expected_result)

    @patch('bots.captchas.requests.post')
    @patch('bots.captchas.requests.get')
    def test_solve_aws_waf_captcha(self, mock_get, mock_post):
        # Configurar el mock de requests.get
        mock_get.return_value.content = b'captcha_image_data'

        # Configurar el mock de requests.post para createTask
        mock_post.side_effect = [
            MagicMock(json=lambda: {"errorId": 0, "taskId": 123}),
            MagicMock(json=lambda: {"status": "ready", "solution": {"text": "captcha_solution"}})
        ]

        # Configurar el mock del driver
        mock_driver = MagicMock()
        mock_captcha_element = MagicMock()
        mock_captcha_element.get_attribute.return_value = 'http://example.com/captcha.jpg'
        mock_driver.find_element.return_value = mock_captcha_element

        # Llamar a la función de resolución de captcha
        result = solve_aws_waf_captcha(mock_driver, 'http://example.com')

        # Verificar que el resultado es la solución del captcha
        self.assertEqual(result, 'captcha_solution')

if __name__ == '__main__':
    unittest.main()