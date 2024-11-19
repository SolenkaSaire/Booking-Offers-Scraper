import os
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración del Proxy de Bright Data
PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = "22225"
PROXY_USER = "brd-customer-hl_4c619868-zone-residential_proxy1"
PROXY_PASSWORD = "jlppy2v5y6zu"

def create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_password):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auth Extension",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_password}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """
    # Crear la extensión temporalmente
    plugin_file = "proxy_auth_plugin.zip"
    with zipfile.ZipFile(plugin_file, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file

def configure_driver_with_proxy_extension():
    proxy_plugin = create_proxy_extension(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASSWORD)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors") 
    options.add_extension(proxy_plugin)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if os.path.exists(proxy_plugin):
        os.remove(proxy_plugin)

    return driver

if __name__ == "__main__":
    driver = configure_driver_with_proxy_extension()
    if driver:
        try:
            print("Intentando acceder a Booking.com con Bright Data Proxy...")
            driver.get("https://www.booking.com/signin.es")
            time.sleep(10) 
            print("Página cargada con éxito.")
        except Exception as e:
            print(f"Error al navegar con Selenium: {e}")
        finally:
            driver.quit()
