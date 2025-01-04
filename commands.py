import tkinter as tk
import threading
from tkinter import filedialog
from pytubefix import YouTube, exceptions
from tkinter.messagebox import showinfo, showerror
import os
import re
from utils import join_path, remove_dir, bytes_to_mb

def on_progress(stream, chunk, bytes_remaining, progress_bar, status_lbl, progress_lbl):
  total_size = stream.filesize
  bytes_downloaded = total_size - bytes_remaining
  percentage = bytes_downloaded / total_size * 100
  rounded = round(percentage, 0)
  print(f"{percentage}% | {bytes_downloaded} bytes | {bytes_remaining} bytes")
  progress_bar["value"] = rounded
  status = status_lbl["text"]
  text = status[0:status.index(" [")]
  
  mb_downloaded = round(bytes_to_mb(bytes_downloaded), 2)
  total_mb = round(bytes_to_mb(total_size), 2)
  status_lbl.config(text = f"{text} [{int(rounded)}%]...")
  progress_lbl.config(text= f"{mb_downloaded} MB | {total_mb} MB")

def on_complete(stream, filepath, btn, lbl):
  btn["state"] = tk.NORMAL
  lbl.config(text = "Descarga completada")

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

def download(event, url, widgets):
  selected_resolution = widgets["res_combo"].get()
  directory = filedialog.askdirectory()
  if directory:
    try:
      btn = event.widget
      btn["state"] = tk.DISABLED
      yt = YouTube(
        url,
        on_progress_callback=lambda stream=None, chunk=None, bytes=None: on_progress(stream, chunk, bytes, widgets["progress_bar"], widgets["status_lbl"], widgets["progress_lbl"]),
        on_complete_callback=lambda stream=None, filepath=None, button=btn, lbl=widgets["status_lbl"]: on_complete(stream, filepath, button, lbl)
      )
      if selected_resolution == widgets["res_combo"]["values"][-1]:
        widgets["status_lbl"].config(text = "Descargando audio [0%]...")
        showinfo(title="Descarga iniciada", message="Descargando audio, por favor espere...")
        thread = threading.Thread(target=download_audio, args=(yt, directory, widgets["status_lbl"], widgets["progress_lbl"]))
      else:
        showinfo(title="Descargando", message="Descargando vídeo, por favor espere...\nNo cierre el programa hasta que se complete la descarga.")
        thread = threading.Thread(target=download_video, args=(yt, selected_resolution, directory, widgets["status_lbl"], widgets["progress_lbl"]))
      thread.start()
    except Exception as e:
      showerror(title="Error", message="Ocurrió un error desconocido al intentar descargar el vídeo.")
      print(type(e), "->", e)
    
def download_video(yt, selected_resolution, directory, lbl, progress_lbl):
  video = yt.streams.filter(file_extension="mp4", resolution=selected_resolution).first()
  audio = yt.streams.get_audio_only()
  if video:
    if os.path.exists(os.path.join(directory, f"{video.title}.mp4")):
      showerror(title="Error", message=f"El vídeo \"{video.title}.mp4\" ya existe")
      return
  
    progress_lbl.config(text = f"0.00 MB | {round(bytes_to_mb(video.filesize), 2)} MB")
    if not os.path.isdir(join_path(".temp")):
      os.mkdir(join_path(".temp"))
    lbl.config(text = "Descargando vídeo [0%]...")
    video.download(filename="video", output_path=".temp")
    lbl.config(text = "Descargando audio [0%]...")
    audio.download(filename="audio", output_path=".temp")
    lbl.config(text = "Uniendo audio y vídeo...")

    path = f"{directory}/video.mp4"
    print(path)
    video_path = f"{directory}/{re.sub(r"[\/\":\*\?<>\|]", "", video.title)}.mp4"
    os.system(f"ffmpeg -y -i ./.temp/video -i ./.temp/audio -c copy {path}")
  
    os.remove(join_path(".temp/video"))
    os.remove(join_path(".temp/audio"))
    os.rename(f"{directory}/video.mp4", video_path)
    showinfo(title="¡Descarga completada!", message=f"El vídeo {video.title} se ha descargado correctamente en la ruta {video_path}")
    remove_dir(join_path(".temp"))
  else:
    showerror(title="Error", message="No se encontró el vídeo específicado.")

def download_audio(yt, directory, lbl, progress_lbl):
  try:
    audio = yt.streams.get_audio_only()

    if os.path.exists(os.path.join(directory, f"{audio.title}.mp3")):
      showerror(title="Error", message=f"El audio \"{audio.title}.mp3\" ya existe")
      return

    progress_lbl.config(text = f"0.00 MB | {round(bytes_to_mb(audio.filesize), 2)} MB")
    audio.download(output_path=directory, filename=f"{audio.title}.mp3")
    audio_path = f"{directory}/{audio.title}.mp3"
    lbl.config(text="Audio descargado")
    showinfo(title="¡Descarga completada!", message=f"El audio {audio.title} se ha descargado correctamente en la ruta {audio_path}")
  except Exception:
    showerror(title="Error", message="Ocurrió un error desconocido al intentar descargar el audio.")
