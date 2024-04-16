from pytube import YouTube
from moviepy.editor import *
import os
import sys

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video_file = video.download(output_path)
        # Renombrar el archivo descargado a "audio.mp4"
        os.rename(video_file, os.path.join(output_path, "audio.mp4"))
        return "audio.mp4"
    except Exception as e:
        print("Error al descargar el video:", str(e))
        return None

def convert_to_mp3(video_file, output_path):
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(output_path)
        video.close()
        audio.close()
        os.remove(video_file)  # Elimina el archivo de video después de la conversión
    except Exception as e:
        print("Error al convertir el video a MP3:", str(e))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <URL_del_video_de_Youtube> <ruta_de_salida_para_el_archivo_MP3>")
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2]

    # Descargar el video
    video_file = download_video(url, '.')

    if video_file:
        # Convertir a MP3
        output_file = os.path.join(output_path, "audio.mp3")
        convert_to_mp3(video_file, output_file)
        print("¡La conversión a MP3 ha sido completada!")
    else:
        print("No se pudo descargar el video.")
