# Author -> Edgar Chacín

import tkinter as tk
from tkinter.messagebox import showerror
import utils
from tkinter import ttk
import commands
import os
from PIL import Image, ImageTk

# Global variables
program_version = "1.1.0"
w = 430
h = 450
thumbnail_width = 225
thumbnail_height = 150
video_data = dict()
window = None
bar = None

def create_video_controls(vid_details):
  # Frame
  frame = ttk.Frame(master=window, borderwidth=5, relief="ridge")
  
  frame.columnconfigure(0, weight=1)
  frame.columnconfigure(1, weight=1)
  frame.columnconfigure(2, weight=1)
  frame.columnconfigure(3, weight=1)
  
  frame.grid(column=0, row=3, columnspan=3, padx=10, pady=(15, 5), sticky=tk.EW)
  ttk.Label(
    master=frame,
    text="Información del vídeo:",
    font=("Helvetica", 14)
  ).grid(column=0, row=0, columnspan=4, sticky=tk.EW)
  
  # Video details
  t = vid_details["title"]
  if len(t) > 40: t = f"{t[0:40]}..."
  title = ttk.Label(master=frame, text=t, font="Helvetica 12 bold")
  title.grid(column=0, row=1, columnspan=4, sticky=tk.W)
  img = utils.fetch_img(vid_details["thumbnail"], thumbnail_width, thumbnail_height)
  if img is Exception:
    showerror(title="Error", message=f"Error: {img}")
  thumbnail = tk.Canvas(master=frame, width=thumbnail_width, height=thumbnail_height)
  thumbnail.create_image(0, thumbnail_height//2, image=img, anchor=tk.W)
  thumbnail.image = img
  thumbnail.grid(column=0, row=2, columnspan=2, rowspan=8, sticky=tk.EW)
  
  # Duration
  duration_lbl = ttk.Label(master=frame, text="Duración: ", font="Helvetica 10 bold", anchor=tk.CENTER)
  duration_lbl.grid(column=3, row=2, sticky=tk.EW)
  
  time = utils.seconds_to_hours(vid_details["duration"])
  time_lbl = ttk.Label(master=frame, text=utils.time_to_str(time), font="Helvetica 10", anchor=tk.CENTER)
  time_lbl.grid(column=3, row=3, sticky=tk.EW)
  
  # Resolution
  res_lbl = ttk.Label(master=frame, text="Resolución:", font="Helvetica 10 bold", anchor=tk.CENTER)
  res_lbl.grid(column=3, row=4, sticky=tk.EW, padx=5)
  
  resolution = tk.StringVar()
  res_combo = ttk.Combobox(master=frame, textvariable=resolution, values=tuple([*vid_details["resolutions"], "Solo audio"]), state="readonly")
  res_combo.grid(column=3, row=5)
  
  # Author
  author_str = vid_details["author"]
  if len(author_str) > 20: author_str = f"{author_str[0:17]}..."
  author_lbl = ttk.Label(master=frame, text="Autor:", font="Helvetica 10 bold", anchor=tk.CENTER)
  author_lbl.grid(column=3, row=6)
  author = ttk.Label(master=frame, text=author_str, font="Helvetica 10", anchor=tk.CENTER)
  author.grid(column=3, row=7)
  
  # Download
  btn_photo = utils.get_image("download.png")
  download_btn = ttk.Button(master=frame, text="Descargar", image=btn_photo, compound=tk.LEFT, state=tk.DISABLED, cursor="hand2")
  download_btn.image = btn_photo
  download_btn.grid(column=3, row=8, sticky=tk.EW, padx=5)
  
  # Status text
  status_lbl = ttk.Label(master=frame, text="Vídeo encontrado", compound=tk.LEFT, font="Helvetica 12 bold")
  status_lbl.grid(column=0, row=10, sticky=tk.EW, columnspan=4, pady=(5, 0), padx=(2, 2))

  # Progress Bar
  bar = ttk.Progressbar(master=frame, orient="horizontal", mode="determinate", length=100)
  bar.grid(column=0, row=11, sticky=tk.EW, columnspan=4, padx=(2, 2), pady=(0, 5))

  # Bindings
  res_combo.bind("<<ComboboxSelected>>", lambda event, btn=download_btn: commands.select_resolution(event, btn))
  download_btn.bind("<Button>", lambda event, res_combo=res_combo, progress=bar, url=vid_details["url"], status=status_lbl: commands.download(event, res_combo, progress, url, status))


if __name__ == "__main__":
  window = tk.Tk()
  px = (window.winfo_screenwidth() // 2) - (w // 2)
  py = (window.winfo_screenheight() // 2) - (h // 2)
  
  window.geometry(f"{w}x{h}+{px}+{py}")
  window.title("Python YT Downloader")
  icon = Image.open(os.path.join(os.getcwd(), "assets", "icon.png"))
  window.wm_iconphoto(False, ImageTk.PhotoImage(icon))
  window.resizable(0, 0)
  
  window.columnconfigure(0, weight=2)
  window.columnconfigure(1, weight=1)
  window.columnconfigure(2, weight=1)
  window.rowconfigure(3, weight=3)
  
  # .: Widgets :.
  # Banner
  banner_photo = utils.get_image("banner.png")
  banner = ttk.Label(master=window, image=banner_photo, anchor=tk.CENTER)
  banner.grid(column=0, row=0, columnspan=3)
  
  # search
  url_label = ttk.Label(master=window, text="Introduce la URL del vídeo:")
  url_label.grid(column=0, row=1, sticky=tk.W, padx=(15, 0))
  
  url_entry = ttk.Entry(master=window)
  url_entry.focus()
  url_entry.grid(column=0, row=2, columnspan=2, sticky=tk.EW, padx=(15, 0))
  
  magnifier = tk.PhotoImage(file="assets/magnifier.png")
  search_btn = ttk.Button(
    master=window,
    image=magnifier,
    text="Buscar...",
    compound=tk.LEFT,
    cursor="hand2",
    command=lambda: commands.find_video(url_entry.get(), create_video_controls)
  )
  search_btn.grid(column=2, row=2, sticky=tk.W, padx=(5, 0))

  # version
  version = ttk.Label(
    master=window,
    text=f"Versión {program_version}",
    anchor=tk.W,
    font=("Helvetica 8 bold"),
    background="#1AA7EC",
    foreground="white",
    padding=(10, 2)
  )
  version.grid(column=0, row=4, columnspan=3, sticky=tk.EW)
  
  # .: Run :.
  window.mainloop()
