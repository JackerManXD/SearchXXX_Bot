# XNXX Bot
 ## Descripción
XNXX Bot es un bot de Telegram que te permite buscar y compartir enlaces de videos desde el sitio web xnxx.com. Puedes utilizar el bot en conversaciones o en modo inline para compartir enlaces de videos de manera rápida y sencilla.
 ## Funcionalidades
- Buscar videos en xnxx.com y obtener enlaces, imágenes y títulos de los resultados de búsqueda.
- Compartir enlaces de videos en conversaciones.
- Compartir enlaces de videos en modo inline.
 ## Requisitos
- Python 3.7 o superior
- [Pyrogram](https://github.com/pyrogram/pyrogram)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [requests](https://docs.python-requests.org/en/latest/)
 ## Instalación
1. Clona el repositorio o descarga los archivos del bot.
2. Instala las dependencias ejecutando el siguiente comando en la terminal:
pip install -r requirements.txt
3. Configura las variables de entorno en un archivo  `.env`  con la siguiente estructura:
PORT=<puerto>
NAME_APP=<nombre_de_la_aplicacion>
API_HASH=<API_hash>
API_ID=<API_ID>
BOT_TOKEN=<token_del_bot>
4. Ejecuta el bot con el siguiente comando:
python bot.py
## Uso
- En conversaciones, envía un enlace de xnxx.com para obtener información de metadatos del video.
- En modo inline, escribe  `@xnxxbot <término_de_búsqueda>`  para buscar videos en xnxx.com y compartir enlaces en la conversación.
 ## Contribución
Si deseas contribuir al desarrollo de XNXX Bot, puedes hacerlo de las siguientes maneras:
- Reportando errores o problemas en la sección de [Issues](https://github.com/tu_usuario/tu_repositorio/issues).
- Sugerir mejoras o nuevas funcionalidades en la sección de [Issues](https://github.com/tu_usuario/tu_repositorio/issues).
- Enviando un [Pull Request](https://github.com/tu_usuario/tu_repositorio/pulls) con tus cambios propuestos.
 ## Licencia
Este proyecto está licenciado bajo la [Licencia MIT](https://opensource.org/licenses/MIT).
