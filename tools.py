from __future__ import unicode_literals
from cv2 import VideoCapture, imwrite, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, CAP_PROP_FPS
from os import makedirs
from os.path import join
from pyrogram.types import InputMediaPhoto
from yt_dlp import YoutubeDL
from requests import get

def extractSeconds(file: str) -> int:
    """
    La función `extractInfoVideo` toma un archivo de video y un nombre de usuario como entrada, extrae
    información sobre el video (como el número de fotogramas y la duración), genera una imagen en
    miniatura con una marca de agua basada en el nombre de usuario y devuelve la ruta a la imagen en
    miniatura y la duración del video en segundos.

    :param file: El parámetro `archivo` es la ruta al archivo de video del que desea extraer
    información. Debe ser una cadena que represente la ruta del archivo
    :param USERNAME: El parámetro `USERNAME` es una cadena que representa el nombre de usuario del
    usuario que solicita la extracción de la miniatura del video
    :return: el nombre de archivo de la imagen en miniatura del video generado y la duración del video
    en segundos.
    """
    VIDEO = VideoCapture(file)  # RUTA DEL VIDEO
    frames = VIDEO.get(CAP_PROP_FRAME_COUNT)
    fps = int(VIDEO.get(CAP_PROP_FPS))
    return int(frames / fps)

def extractImg(File: str, message: str) -> list:
    """
    La función `extractImg` toma un archivo de video y un nombre de usuario como entrada, extrae 10
    imágenes del video a intervalos regulares y devuelve una lista de las rutas de los archivos extraídos. imágenes

    :param File: El parámetro `Archivo` es el nombre del archivo de video del que desea extraer
    imágenes. Debe ser una cadena que represente el nombre del archivo, incluida la extensión del
    archivo.

    :param Username: El nombre de usuario es una cadena que representa el nombre del usuario. Se utiliza
    para crear un directorio con el nombre de usuario como nombre.

    :return: una lista de rutas de archivo de imagen.
    """
    try:
        makedirs(join(message.from_user.username, "IMG"))
    except:
        pass
   
    VIDEO = VideoCapture(File)
    TOTALFRAME = int(VIDEO.get(CAP_PROP_FRAME_COUNT))
    RESULTADO = TOTALFRAME//10

    count = 1
    ListaImg = []

    for i in range(RESULTADO//2, TOTALFRAME, RESULTADO):
        VIDEO.set(CAP_PROP_POS_FRAMES, i)
        frame = VIDEO.read()[1]
        imwrite(f"./{message.from_user.username}/IMG/IMG-{count}.jpg", frame)
        ListaImg.append(InputMediaPhoto(join(message.from_user.username, "IMG", f"IMG-{count}.jpg")))
        count += 1

    return ListaImg

def download(url:str) -> str:
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url)
        video_filename = ydl.prepare_filename(info_dict)
        with open(info_dict['title']+'.jpeg', 'wb') as f: f.write(get(info_dict['thumbnail']).content)
        return video_filename, info_dict['title']+'.jpeg'