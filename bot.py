from pyrogram.methods.utilities.idle import idle
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from bs4 import BeautifulSoup
from asyncio import sleep as asyncsleep
from aiohttp import ClientSession
from aiohttp import web
from os import getenv
from shutil import rmtree
from os.path import exists
from requests import get
import re
from tools import download, extractImg, extractSeconds

PORT = getenv('PORT')
NAME_APP = getenv("NAME_APP")
API_HASH = getenv("API_HASH")
API_ID = getenv("API_ID")
BOT_TOKEN = getenv("BOT_TOKEN")

if exists('./Debug.py'):
    from Debug import BOT_TOKEN, PORT, API_HASH, API_ID
    print("MODO DEBUG")
    DEBUG = True
else:
    print("MODO ONLINE")
    DEBUG = False

app = Client(name='searchxxx', api_hash=API_HASH,
             api_id=API_ID, bot_token=BOT_TOKEN)

# =============================================================== RESPUESTAS

@app.on_message(filters.regex('https://www.xnxx.com') & filters.user('KOD_16'))
def mostrar_info(app, message):
    """
    La función `mostrar_info` descarga un video, lo sube a un canal de Telegram, extrae imágenes del
    video, envía las imágenes a otro canal de Telegram y elimina los archivos temporales.
    
    :param app: El parámetro "app" es probablemente una instancia de un cliente de Telegram, como la
    clase `TelegramClient` de la biblioteca `Telethon`. Se utiliza para interactuar con la API de
    Telegram y realizar acciones como enviar mensajes, cargar medios, etc
    :param message: El parámetro `mensaje` es un objeto que representa el mensaje recibido por la
    aplicación. Contiene información como el texto del mensaje, el remitente y otros metadatos
    """
    sms = message.reply('**Downloading video...**')
    file = download(message.text)
    
    sms.edit_text('Uploading video...')
    video = app.send_video(-1001515779942, file[0], duration=extractSeconds(file[0]), thumb=file[1])

    sms.edit_text('**Extracting images...**')
    list_img = extractImg(file[0], message)
    
    caption = show_metadata(message.text)
    caption += f"\n\n**🔥 [DOWNLOAD VIDEO](https://t.me/c/{1515779942}/{video.id}) 🔥**"
    
    sms.edit_text('**Sending images...**')
    media = app.send_media_group(message.chat.id, list_img)
    media[-1].edit_caption(caption)
    
    sms.delete()
    rmtree(message.from_user.username)

@app.on_inline_query()
async def handle_inline_query(client, query):
    """
    La función `handle_inline_query` toma una consulta de búsqueda, realiza web scraping para obtener
    enlaces y crea resultados de consultas en línea con los enlaces obtenidos.

    :param client: El parámetro `cliente` es una instancia de la clase de cliente que se utiliza para
    interactuar con la API de Telegram. Es responsable de enviar y recibir mensajes, realizar llamadas
    API y manejar otras interacciones con la plataforma Telegram
    :param query: El parámetro `query` es un objeto que representa la consulta en línea realizada por un
    usuario. Contiene información como el texto de la consulta, el usuario que realizó la consulta y
    otros detalles relevantes
    """
    results = []
    search_query = query.query.strip()

    # Verifica si la consulta no está vacía
    if search_query:
        # Realiza el web scraping y obtiene los enlaces
        enlaces = scrape_links(search_query)

        # Crea los resultados de la consulta inline con los enlaces obtenidos
        for i, data in enumerate(enlaces[0]):
            results.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=data[2],
                    description=f'Page: {enlaces[1]}',
                    input_message_content=InputTextMessageContent(data[0]),
                    thumb_url=data[1]
                )
            )
    try:
        await client.answer_inline_query(query.id, results)
    except:
        pass


def scrape_links(search_query):
    """
    La función `scrape_links` toma una consulta de búsqueda como entrada y extrae enlaces e imágenes de
    los resultados de búsqueda en xnxx.com.

    :param search_query: La consulta de búsqueda es el término o frase que desea buscar en el sitio web.
    Puede ser cualquier valor de cadena que desee utilizar como consulta de búsqueda
    :return: La función `scrape_links` devuelve una lista de tuplas. Cada tupla contiene tres elementos:
    el enlace a un video en xnxx.com, la imagen asociada con el video y el título del video.
    """
    pag = 0
    if search_query.split(' ')[-1].isdigit():
        pag = search_query.split(' ')[-1]
        url = f"https://www.xnxx.com/search/{search_query.lower().split(' ')[0]}/{pag}"

    else:
        url = f"https://www.xnxx.com/search/{search_query.lower()}"

    html = get(url).content
    soup = BeautifulSoup(html, "html.parser")
    all = set()
    elements = soup.find_all("a")
    for element in elements:
        if 'href="/video' in str(element) and 'data-src=' in str(element):
            link = 'https://www.xnxx.com' + \
                str(element).split('<a href="')[-1].split('"')[0]
            img = str(element).split('data-src="')[-1].split('"')[0]
            name = link.split('/')[-1].replace('_', ' ').capitalize()

            all.add((link, img, name))

    return all, pag


def show_metadata(url: str):
    """
    La función `show_metadata` toma una URL como entrada, recupera el contenido HTML de la URL, extrae
    información de metadatos como el título, la duración, la resolución y las vistas del HTML utilizando
    BeautifulSoup y devuelve una cadena formateada que contiene los metadatos extraídos.

    :param url: El parámetro `url` es la URL de una página web que contiene metadatos sobre un video
    :return: La función `show_metadata` devuelve una cadena que contiene los metadatos de una URL dada.
    Los metadatos incluyen el título, la duración, la resolución, las vistas y las etiquetas del video.
    """
    html = get(url).content
    soup = BeautifulSoup(html, "html.parser")
    info = soup.find('div', class_='clear-infobar')
    txt = ''
    txt += '🎬 **Title: ' + f"`{info.find('strong').text}`**\n"

    patronmin = r'(\d+)\s*(min)'
    patronsec = r'(\d+)\s*(sec)'

    metadata = info.find('span', class_='metadata').text.replace(
        '\t', '').split('-')

    if metadata[0].replace('\n', '').endswith('min'):
        txt += '⏱️ **Duration: ' + '`' + \
            re.findall(patronmin, metadata[0])[0][0] + ' Min`**\n'
    elif metadata[0].replace('\n', '').endswith('sec'):
        txt += '⏱️ **Duration: ' + '`' + \
            re.findall(patronsec, metadata[0])[0][0] + ' Sec`**\n'

    txt += '**📺 Resolution: ' + '`' + metadata[1].replace(' ', '') + '`**\n'
    txt += '**🌎 Views: ' + '`' + metadata[2].replace(' ', '') + '`**\n\n'

    txt += '**🏷️ Tags: **'
    for i in soup.find_all('a', class_='is-keyword'):
        txt += '#' + i.text.replace(' ', '_') + ' '

    return txt


# =============================================================== SERVER
server = web.Application()
runner = web.AppRunner(server)


async def despertar(sleep_time=10 * 60):
    while True:
        await asyncsleep(sleep_time)
        async with ClientSession() as session:
            async with session.get(f'https://{NAME_APP}.onrender.com/' + "/Despiertate"):
                pass


async def run_server():
    await app.start()
    print('Bot Iniciado')
    # Iniciando User Bot
    await runner.setup()
    print('Iniciando Server')
    await web.TCPSite(runner, host='0.0.0.0', port=PORT).start()
    print('Server Iniciado')

if __name__ == '__main__':
    app.loop.run_until_complete(run_server())
    if not DEBUG:
        app.loop.run_until_complete(despertar())
    idle()
