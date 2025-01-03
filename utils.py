# Author -> Edgar Chacín

from os import getcwd
from tkinter import PhotoImage
from platform import system
from PIL import Image, ImageTk
import io
import requests

def join_path(*paths):
  files = ""
  for p in paths:
    files += f"/{p}"
  return f"{getcwd()}{files}"

def get_image(img_name):
  return PhotoImage(file=join_path("assets", img_name))

def fetch_img(url, width=None, height=None):
  response = requests.get(url, stream=True)
  try:
    response.raise_for_status()
  except Exception as e:
    print(e)
    return e
  
  img_data = response.content
  image = Image.open(io.BytesIO(img_data))
  if width is not None and height is not None:
    image = image.resize((width, height))
  img = ImageTk.PhotoImage(image)
  return img
  
  
def seconds_to_hours(seconds):
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return hours, minutes, seconds

def time_to_str(time):
  return (f"{time[0]}".rjust(2, "0") + "h:" + f"{time[1]}".rjust(2, "0") + "m:" + f"{time[2]}".rjust(2, "0") + "s")