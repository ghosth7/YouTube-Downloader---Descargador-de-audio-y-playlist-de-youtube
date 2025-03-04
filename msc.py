import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
from pydub import AudioSegment

# --- Funciones comunes ---
def seleccionar_carpeta(dest_var):
    carpeta = filedialog.askdirectory(title="Seleccione Carpeta")
    if carpeta:
        dest_var.set(carpeta)

# --- Funciones para la pestaña de Descarga ---
def descargar():
    url = url_entry.get().strip()
    carpeta = carpeta_var.get().strip()
    formato = formato_combo.get().strip()
    tipo = download_type_var.get()

    if not url:
        messagebox.showerror("Error", "Debe ingresar una URL.")
        return
    if not carpeta:
        messagebox.showerror("Error", "Debe seleccionar una carpeta de descarga.")
        return
    if not formato:
        messagebox.showerror("Error", "Debe seleccionar un formato de descarga.")
        return

    # Configurar opciones según el tipo seleccionado:
    if tipo == "Audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': '192',
            }]
        }
    elif tipo == "Playlist":
        # Si el formato es de audio, extrae audio; de lo contrario, descarga video
        if formato in ["mp3", "wav", "flac", "aac", "ogg"]:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
                'noplaylist': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': formato,
                    'preferredquality': '192',
                }]
            }
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio',
                'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
                'noplaylist': False
            }
    else:
        messagebox.showerror("Error", "Tipo de descarga no reconocido.")
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Éxito", "Descarga completada con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar: {e}")

# --- Funciones para la pestaña de Conversión ---
def seleccionar_archivo_convertir():
    global input_file
    file_path = filedialog.askopenfilename(
        title="Seleccione archivo de audio",
        filetypes=[("Audio Files", "*.mp3;*.wav;*.flac;*.ogg;*.aac")]
    )
    if file_path:
        input_file = file_path
        archivo_label.config(text=os.path.basename(input_file))
    else:
        input_file = ""
        archivo_label.config(text="Ningún archivo seleccionado")

def convertir():
    global input_file
    if not input_file:
        messagebox.showerror("Error", "Seleccione un archivo de audio para convertir.")
        return
    carpeta_salida = carpeta_salida_var.get().strip()
    if not carpeta_salida:
        messagebox.showerror("Error", "Seleccione una carpeta de salida.")
        return
    formato_salida = formato_salida_combo.get().strip()
    if not formato_salida:
        messagebox.showerror("Error", "Seleccione el formato de salida.")
        return

    nombre_base = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(carpeta_salida, f"{nombre_base}.{formato_salida}")

    try:
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format=formato_salida)
        messagebox.showinfo("Éxito", f"Conversión completada:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al convertir: {e}")

# --- Configuración de la ventana principal ---
root = tk.Tk()
root.title("YouTube Downloader & Audio Converter")
root.geometry("500x450")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

# === Pestaña 1: Descarga ===
tab_descarga = ttk.Frame(notebook)
notebook.add(tab_descarga, text="Descarga")

# URL del video o playlist
ttk.Label(tab_descarga, text="URL del video/playlist:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
url_entry = ttk.Entry(tab_descarga, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# Tipo de descarga: Audio o Playlist
ttk.Label(tab_descarga, text="Tipo de descarga:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
download_type_var = tk.StringVar(value="Audio")
tipo_combo = ttk.Combobox(tab_descarga, textvariable=download_type_var, values=["Audio", "Playlist"], state="readonly", width=15)
tipo_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Carpeta de descarga
carpeta_var = tk.StringVar()
ttk.Button(tab_descarga, text="Seleccionar Carpeta de Descarga", command=lambda: seleccionar_carpeta(carpeta_var)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
ttk.Label(tab_descarga, textvariable=carpeta_var).grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Formato de descarga
ttk.Label(tab_descarga, text="Formato de descarga:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
formato_combo = ttk.Combobox(tab_descarga, values=["mp3", "wav", "flac", "aac", "ogg", "mp4"], state="readonly", width=10)
formato_combo.set("mp3")
formato_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Botón para iniciar descarga
ttk.Button(tab_descarga, text="Descargar", command=descargar).grid(row=4, column=0, columnspan=2, pady=10)

# === Pestaña 2: Conversión ===
tab_conversion = ttk.Frame(notebook)
notebook.add(tab_conversion, text="Conversión")

# Seleccionar archivo a convertir
global input_file
input_file = ""
ttk.Button(tab_conversion, text="Seleccionar Archivo", command=seleccionar_archivo_convertir).grid(row=0, column=0, padx=10, pady=5, sticky="w")
archivo_label = ttk.Label(tab_conversion, text="Ningún archivo seleccionado")
archivo_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Seleccionar carpeta de salida para la conversión
carpeta_salida_var = tk.StringVar()
ttk.Button(tab_conversion, text="Seleccionar Carpeta de Salida", command=lambda: seleccionar_carpeta(carpeta_salida_var)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
ttk.Label(tab_conversion, textvariable=carpeta_salida_var).grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Formato de salida
ttk.Label(tab_conversion, text="Formato de salida:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
formato_salida_combo = ttk.Combobox(tab_conversion, values=["mp3", "wav", "flac", "aac", "ogg"], state="readonly", width=10)
formato_salida_combo.set("mp3")
formato_salida_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Botón para convertir
ttk.Button(tab_conversion, text="Convertir", command=convertir).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
