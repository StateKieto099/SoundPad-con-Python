# En la terminal instalar el tkinter con "pip install tkinter" para que funcione
import tkinter as tk
from tkinter import filedialog, simpledialog
import pygame
import os
import json

# Archivo donde se guardan los datos
ARCHIVO_DATOS = "sonidos.json"

# se inicializa el pygame para el mixer
pygame.mixer.init()

def reproducir_sonido(ruta):
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.play()

def guardar_sonidos():
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(lista_sonidos, f)

def cargar_sonidos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    return []

def crear_boton(nombre, ruta):
    nuevo_btn = tk.Button(frame_botones, text=nombre,
                          command=lambda r=ruta: reproducir_sonido(r))
    nuevo_btn.pack(pady=5)

def agregar_boton():
    # Se elige el archivo de sonido
    ruta = filedialog.askopenfilename(
        title="Seleccionar sonido",
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg")]
    )
    
    if ruta:
        # Pide el nombre del boton
        nombre = simpledialog.askstring("Nombre", "Nombre del botón: ")

        if not nombre:
            nombre = os.path.basename(ruta)

        # Guardar en lista
        lista_sonidos.append({"nombre": nombre, "ruta": ruta})
        guardar_sonidos()

        # Crear botón automaticamente
        crear_boton(nombre, ruta)

# Ventana
ventana = tk.Tk()
ventana.title("Botonera para Discord")

# Frame para organizar los botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

# Cargar sonidos guardados
lista_sonidos = cargar_sonidos()

# Crear botones guardados
for sonido in lista_sonidos:
    crear_boton(sonido["nombre"], sonido["ruta"])

# Botón para agregar nuevos sonidos
btn_agregar = tk.Button(ventana, text="➕ Agregar sonido", command=agregar_boton)
btn_agregar.pack(pady=10)

ventana.mainloop()

# Lo más importante para que les suene por el microfono es que se descarguen el VB-Audio Virtual cable
# 1. Instalás VB-Cable "https://vb-audio.com/Cable/"
# 2. En Windows:
#      .Ponés "CABLE Input" como dispositivo para que se reproduzca.
#      .Ponés "CABLE Output" como microfono en el discord.
# 3. Python reproduce sonido -> entra al CABLE -> sale como microfono.