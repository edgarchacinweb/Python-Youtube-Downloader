import os
import shutil
from tkinter import PhotoImage
from PIL import Image, ImageTk
import io
import requests

def get_image(img_name):
  return PhotoImage(file=os.path.join(os.getcwd(), "assets", img_name))

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

def join_path(path):
  return os.path.join(os.getcwd(), path)

def remove_dir(path):
  if os.path.isdir(join_path(path)):
    shutil.rmtree(join_path(path))

def bytes_to_mb(bytes):
  return bytes / 1000000