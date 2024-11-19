# **Booking Offers Scraper**

¡Bienvenido a **Booking Offers Scraper**! 🎉

**Booking Offers Scraper** es una herramienta poderosa diseñada para obtener las mejores ofertas en reservas de alojamiento y hoteles en tiempo real de Booking.com. Esta aplicación combina automatización avanzada con técnicas de scraping dinámico para identificar las opciones más económicas y convenientes, utilizando datos personalizados según la ubicación y las fechas seleccionadas.

---

## **Características principales**
- 🌐 **Scraping dinámico**: Obtiene información de precios y ofertas en tiempo real desde plataformas de reservas.
- 🛠️ **Automatización avanzada**: Automatiza procesos complejos como login, manejo de cookies, y rotación de proxies.
- 🔒 **Gestión segura**: Permite la integración con Google API para el manejo de enlaces de verificación que llegan a tu correo.
- 📊 **Análisis de datos**: Exporta y organiza los resultados en formatos amigables como Excel o CSV.
- 🕵️‍♂️ **Superación de restricciones**: Utiliza técnicas para evitar bloqueos y limitaciones.

---

## **Tecnologías utilizadas**
Este proyecto combina múltiples tecnologías para garantizar un desempeño eficiente:
- **Python**: Lenguaje principal para la automatización y el scraping.
- **Selenium**: Automatización de navegadores.
- **Requests**: Gestión de peticiones HTTP.
- **Pandas y OpenPyxl**: Manipulación y análisis de datos exportados.
- **Google API**: Integración para el manejo de correos y enlaces de verificación.

---

## **Uso previsto**
Este scraper está diseñado tanto para **viajeros frecuentes** como para **analistas de datos de turismo**, que buscan optimizar costos y mejorar sus decisiones de reservas. También es ideal para profesionales interesados en explorar técnicas avanzadas de web scraping y automatización.

---

¡Gracias por interesarte en **Booking Offers Scraper**! 🌍✨


## Cómo ejecutar 
Ejecución
Inicio de Sesión
Para iniciar sesión en Booking.com y guardar las cookies:

python main.py login

Scraping
Para realizar el scraping de ofertas de hoteles, asegúrate de tener un archivo tasks.txt con el siguiente formato: Lugar checkin checkout

Buenos_Aires 2024-12-01 2024-12-07
Ciudad_de_Mexico 2024-12-10 2024-12-15
Lima 2024-12-20 2024-12-25
Bogota 2024-12-05 2024-12-10
Santiago 2024-12-15 2024-12-20

Luego, ejecuta el siguiente comando:

python main.py scrape tasks.txt