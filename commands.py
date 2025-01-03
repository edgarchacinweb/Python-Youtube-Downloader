import tkinter as tk
import threading
from tkinter import filedialog
from pytubefix import YouTube, exceptions
from tkinter.messagebox import showinfo, showerror
import os
from utils import join_path
import re
import pathlib

def on_progress(stream, chunk, bytes_remaining, progress_bar, status_lbl):
  total_size = stream.filesize
  bytes_downloaded = total_size - bytes_remaining
  percentage = round(bytes_downloaded / total_size * 100, 0)
  print(f"{percentage}%")
  progress_bar["value"] = percentage
  status = status_lbl["text"]
  text = status[0:status.index(" [")]
  status_lbl.config(text = f"{text} [{int(percentage)}%]...")

def on_complete(stream, filepath, btn):
  btn["state"] = tk.NORMAL

def find_video(url, cb):
  showinfo(title="Información", message="Buscando vídeo, espere un momento...")
  try:
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
    resolutions = set()
    for stream in yt.streams:
      r = stream.resolution
      if r is not None:
        resolutions.add(r)
    resolutions = sorted([int(r[0:-1]) for r in resolutions], reverse=True)
    data = {
      "title": yt.title,
      "resolutions": list(map(lambda r: f"{r}p", resolutions)),
      "author": yt.author,
      "url": url,
      "thumbnail": yt.thumbnail_url,
      "duration": yt.length
    }
    cb(data)
  except exceptions.RegexMatchError as e:
    showerror(title="Error", message="introduce una URL válida")
  except Exception as e:
    showerror("Error", "Error al obtener la información del vídeo")
    print(type(e))
    
def select_resolution(event, btn):
  btn["state"]=tk.NORMAL

def download(event, res, progress, url, status_lbl):
  selected_resolution = res.get()
  directory = filedialog.askdirectory()
  if directory:
    try:
      btn = event.widget
      btn["state"] = tk.DISABLED
      yt = YouTube(
        url,
        on_progress_callback=lambda stream=None, chunk=None, bytes=None, bar=progress: on_progress(stream, chunk, bytes, bar, status_lbl),
        on_complete_callback=lambda stream=None, filepath=None, button=btn: on_complete(stream, filepath, button)
      )
      if selected_resolution == res["values"][-1]:
        status_lbl.config(text = "Descargando audio [0%]...")
        showinfo(title="Descarga iniciada", message="Descargando audio, por favor espere...")
        thread = threading.Thread(target=download_audio, args=(yt, directory, status_lbl))
      else:
        showinfo(title="Descargando", message="Descargando vídeo, por favor espere...\nNo cierre el programa hasta que se complete la descarga.")
        thread = threading.Thread(target=download_video, args=(yt, selected_resolution, directory, status_lbl))
      thread.start()
    except Exception as e:
      showerror(title="Error", message="Ocurrió un error desconocido al intentar descargar el vídeo.")
      print(type(e), "->", e)
    finally:
      if os.path.isdir(".temp/"):
        os.rmdir(os.path.join(os.getcwd(), ".temp"))
        pathlib.Path.rmdir("./.temp")
    
def download_video(yt, selected_resolution, directory, lbl):
  video = yt.streams.filter(file_extension="mp4", resolution=selected_resolution).first()
  audio = yt.streams.get_audio_only()
  if video:
    os.mkdir(join_path(".temp"))
    lbl.config(text = "Descargando vídeo [0%]...")
    video.download(filename="video", output_path=".temp")
    lbl.config(text = "Descargando audio [0%]...")
    audio.download(filename="audio", output_path=".temp")
    lbl.config(text = "Uniendo audio y vídeo...")

    path = f"{directory}/video.mp4"
    print(path)
    video_path = f"{directory}/{re.sub(r"[\/\":\*\?<>\|]", "", video.title)}.mp4"
    os.system(f"ffmpeg -i ./.temp/video -i ./.temp/audio -c copy {path}")
  
    os.remove(join_path(".temp", "video"))
    os.remove(join_path(".temp", "audio"))
    os.rename(f"{directory}/video.mp4", video_path)
    lbl.config(text = video_path)
    showinfo(title="¡Descarga completada!", message=f"El vídeo {video.title} se ha descargado correctamente en la ruta {video_path}")
  else:
    showerror(title="Error", message="No se encontró el vídeo específicado.")

def download_audio(yt, directory, lbl):
  try:
    audio = yt.streams.get_audio_only()
    audio.download(output_path=directory, filename=f"{audio.title}.mp3")
    audio_path = f"{directory}/{audio.title}.mp3"
    lbl.config(text = audio_path)
    showinfo(title="¡Descarga completada!", message=f"El audio {audio.title} se ha descargado correctamente en la ruta {audio_path}")
  except Exception:
    showerror(title="Error", message="Ocurrió un error desconocido al intentar descargar el audio.")
