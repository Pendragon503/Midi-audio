import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
import json
import os

# Inicializar pygame mixer
mixer.init()

# Ruta del archivo de perfiles
profiles_file = "profiles.json"

# Cargar perfiles desde el archivo JSON
def load_profiles():
    if os.path.exists(profiles_file):
        with open(profiles_file, "r") as f:
            return json.load(f)
    return []

# Guardar perfiles en el archivo JSON
def save_profiles():
    with open(profiles_file, "w") as f:
        json.dump(profiles, f)

# Variables para almacenar las rutas de los archivos de audio y perfiles
profiles = load_profiles()
green_audio_path = None
red_audio_path = None

# Funciones para manejar la reproducción de audio
def play_green_audio():
    if green_audio_path:
        mixer.music.load(green_audio_path)
        mixer.music.play()

def play_red_audio():
    if red_audio_path:
        mixer.music.load(red_audio_path)
        mixer.music.play()

# Función para seleccionar el archivo de audio para el botón verde
def select_green_audio():
    global green_audio_path
    green_audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    green_canvas.itemconfig(green_circle, fill="green" if green_audio_path else "grey")

# Función para seleccionar el archivo de audio para el botón rojo
def select_red_audio():
    global red_audio_path
    red_audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    red_canvas.itemconfig(red_circle, fill="red" if red_audio_path else "grey")

# Función para guardar el perfil actual
def save_profile():
    if not green_audio_path or not red_audio_path:
        messagebox.showwarning("Advertencia", "Debe seleccionar ambos archivos de audio antes de guardar un perfil.")
        return
    profile_name = profile_entry.get()
    if not profile_name:
        messagebox.showwarning("Advertencia", "Debe ingresar un nombre para el perfil.")
        return
    # Verificar si el perfil ya existe
    for profile in profiles:
        if profile["name"] == profile_name:
            messagebox.showwarning("Advertencia", "El nombre del perfil ya existe. Elija un nombre diferente.")
            return
    profiles.append({"name": profile_name, "green_audio": green_audio_path, "red_audio": red_audio_path})
    profile_listbox.insert(tk.END, profile_name)
    save_profiles()  # Guardar los perfiles después de añadir uno nuevo
    clear_audio_paths()

# Función para cargar un perfil seleccionado
def load_profile(event):
    global green_audio_path, red_audio_path
    selection = profile_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    profile = profiles[index]
    green_audio_path = profile["green_audio"]
    red_audio_path = profile["red_audio"]
    green_canvas.itemconfig(green_circle, fill="green")
    red_canvas.itemconfig(red_circle, fill="red")
    profile_entry.delete(0, tk.END)
    profile_entry.insert(0, profile["name"])
    # Resaltar el perfil seleccionado
    profile_listbox.selection_clear(0, tk.END)
    profile_listbox.selection_set(index)
    profile_listbox.activate(index)

# Función para eliminar un perfil seleccionado
def delete_profile():
    selection = profile_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    # Confirmar eliminación
    confirm = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este perfil?")
    if confirm:
        profile_listbox.delete(index)
        profiles.pop(index)
        save_profiles()  # Guardar los perfiles después de eliminar uno
        clear_audio_paths()

# Función para limpiar las rutas de audio actuales
def clear_audio_paths():
    global green_audio_path, red_audio_path
    green_audio_path = None
    red_audio_path = None
    green_canvas.itemconfig(green_circle, fill="grey")
    red_canvas.itemconfig(red_circle, fill="grey")
    profile_entry.delete(0, tk.END)

# Función para limpiar el escenario y comenzar un nuevo perfil
def new_profile():
    clear_audio_paths()
    profile_entry.delete(0, tk.END)
    profile_listbox.selection_clear(0, tk.END)

# Función para salir de la aplicación
def exit_app():
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Reproductor de Audio con Perfiles")

# Configuración para pantalla completa y desactivar la capacidad de cambiar tamaño de la ventana
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: None)  # Desactivar la funcionalidad de la tecla Escape

# Desactivar la capacidad de redimensionar la ventana
root.resizable(False, False)

# Crear los widgets
frame_center = tk.Frame(root)
select_green_button = tk.Button(frame_center, text="Seleccionar Audio Verde", command=select_green_audio)
select_red_button = tk.Button(frame_center, text="Seleccionar Audio Rojo", command=select_red_audio)
green_canvas = tk.Canvas(root, width=400, height=400, highlightthickness=0)  # Tamaño del Canvas aumentado
red_canvas = tk.Canvas(root, width=400, height=400, highlightthickness=0)    # Tamaño del Canvas aumentado
green_circle = green_canvas.create_oval(50, 50, 350, 350, fill="grey", outline="")  # Tamaño del círculo aumentado
red_circle = red_canvas.create_oval(50, 50, 350, 350, fill="grey", outline="")     # Tamaño del círculo aumentado
profile_label = tk.Label(frame_center, text="Nombre del Perfil:")
profile_entry = tk.Entry(frame_center)
save_profile_button = tk.Button(frame_center, text="Guardar Perfil", command=save_profile)
delete_profile_button = tk.Button(frame_center, text="Eliminar Perfil", command=delete_profile)
new_profile_button = tk.Button(frame_center, text="Nuevo Perfil", command=new_profile)  # Nuevo botón para crear un nuevo perfil
profile_listbox = tk.Listbox(root, width=40, selectmode=tk.SINGLE, font=("Helvetica", 14))  # Aumentar el tamaño de la letra en el Listbox
profile_listbox.bind('<<ListboxSelect>>', load_profile)
exit_button = tk.Button(root, text="Salir", bg="blue", fg="white", command=exit_app)  # Botón de salir

# Estilo para el perfil seleccionado
profile_listbox.configure(selectbackground="blue", selectforeground="white")

# Crear el Label para GitHub en la esquina inferior derecha
github_label = tk.Label(root, text="GitHub: Pendragon503", bg="white", font=("Helvetica", 12))

# Asociar eventos de clic a los círculos
green_canvas.tag_bind(green_circle, "<Button-1>", lambda event: play_green_audio() if green_audio_path else None)
red_canvas.tag_bind(red_circle, "<Button-1>", lambda event: play_red_audio() if red_audio_path else None)

# Colocar los widgets en el frame central usando grid
select_green_button.grid(row=0, column=0, padx=10, pady=10)
select_red_button.grid(row=1, column=0, padx=10, pady=10)
profile_label.grid(row=2, column=0, pady=5)
profile_entry.grid(row=3, column=0, pady=5)
save_profile_button.grid(row=4, column=0, pady=10)
delete_profile_button.grid(row=5, column=0, pady=10)
new_profile_button.grid(row=6, column=0, pady=10)  # Ubicar el botón "Nuevo Perfil" debajo de los demás botones

# Colocar los widgets en la ventana usando grid
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

green_canvas.grid(row=1, column=0, padx=20, pady=10, sticky="n")
frame_center.grid(row=1, column=1, padx=20, pady=10)
red_canvas.grid(row=1, column=2, padx=20, pady=10, sticky="n")
profile_listbox.grid(row=2, column=0, columnspan=3, pady=10)
exit_button.grid(row=3, column=0, columnspan=3, pady=10)  # Ubicar el botón de salida en la parte inferior

# Colocar el Label para GitHub en la esquina inferior derecha
github_label.grid(row=4, column=2, padx=10, pady=10, sticky="se")

# Cargar perfiles en el Listbox
for profile in profiles:
    profile_listbox.insert(tk.END, profile["name"])

# Iniciar el bucle principal de la aplicación
root.mainloop()
