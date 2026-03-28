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

# Guardamos los sonidos activos para frenarlos
sonidos_activos = {}

def reproducir_sonido(nombre, ruta, volumen=1.0):
    sonido = pygame.mixer.Sound(ruta)
    sonido.set_volume(volumen)
    canal = sonido.play()

    sonidos_activos[nombre] = canal

def detener_sonido(nombre):
    if nombre in sonidos_activos and sonidos_activos[nombre]:
        sonidos_activos[nombre].stop()

def guardar_sonidos():
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(lista_sonidos, f)

def cargar_sonidos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    return []

def eliminar_sonido(nombre, frame):
    global lista_sonidos
    lista_sonidos = [s for s in lista_sonidos if s["nombre"] != nombre]
    guardar_sonidos()
    frame.destroy()

def actualizar_volumen(nombre, valor):
    for sonido in lista_sonidos:
        if sonido["nombre"] == nombre:
            sonido["volumen"] = float(valor)
    guardar_sonidos()



def crear_boton(nombre, ruta, volumen_inicial=1.0):
    frame = tk.Frame(frame_botones, bg="#1e1e1e", bd=2, relief="ridge")
    frame.pack(pady=6, padx=10, fill="x")

    volumen = tk.DoubleVar(value=volumen_inicial)

    # Nombre
    lbl = tk.Label(frame, text=nombre, fg="white", bg="#1e1e1e", width=15)
    lbl.pack(side="left", padx=5)

    # Botón de play
    btn_play = tk.Button(
        frame, text="▶️", bg="#4CAF50", fg="white",
        command=lambda: reproducir_sonido(nombre, ruta, volumen.get())
    )
    btn_play.pack(side="left", padx=5)

    # Botón de stop
    btn_stop = tk.Button(
        frame, text="⏹", bg="#f39c12", fg="white",
        command=lambda: detener_sonido(nombre)
    )
    btn_stop.pack(side="left", padx=5)
    

    # Slider de volumen
    slider = tk.Scale(frame, from_=0, to=1, resolution=0.05,
                      orient="horizontal", variable=volumen,
                      bg="#1e1e1e", fg="white", highlightthickness=0,
                      command=lambda val: actualizar_volumen(nombre, val),
                      length=120
    )
    slider.pack(side="left", padx=10)

    # Botón eliminar
    btn_eliminar = tk.Button(
        frame, text="❌", bg="#e74c3c", fg="white",
        command=lambda: eliminar_sonido(nombre, frame))
    btn_eliminar.pack(side="right", padx=5)

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

        nuevo = {
            "nombre": nombre,
            "ruta": ruta,
            "volumen": 1.0
        }

        # Guardar en lista
        lista_sonidos.append(nuevo)
        guardar_sonidos()

        # Crear botón automaticamente
        crear_boton(nombre, ruta, 1.0)

# Ventana
ventana = tk.Tk()
ventana.title("Botonera para Discord")
ventana.geometry("500x500")
ventana.configure(bg="#121212")

titulo = tk.Label(
    ventana, text="Botonera para Discord",
    font=("Arial", 16, "bold"),
    bg="#121212", fg="white"
)
titulo.pack(pady=10)


# Frame para organizar los botones
frame_botones = tk.Frame(ventana, bg="#121212")
frame_botones.pack(fill="both", expand=True)

# Cargar sonidos guardados
lista_sonidos = cargar_sonidos()

# Crear botones guardados
for sonido in lista_sonidos:
    crear_boton(
        sonido["nombre"], 
        sonido["ruta"],
        sonido.get("volumen", 1.0)
    )

# Botón para agregar nuevos sonidos
btn_agregar = tk.Button(
    ventana,
    text="➕ Agregar sonido",
    bg="#3498db",
    fg="white",
    font=("Arial", 10, "bold"),
    command=agregar_boton
)
btn_agregar.pack(pady=10)

ventana.mainloop()