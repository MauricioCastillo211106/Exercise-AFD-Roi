import locale
import io
import textwrap
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import *
import numpy as np
from Automata import *
import math

sentenciasValidas = []

def openfile():
    fileopen = filedialog.askopenfilename(
        initialdir="/",
        title="Seleccione su archivo de texto",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    print(fileopen)
    create_query_string(fileopen)

def guess_encoding(fileopen):
    with io.open(fileopen, "rb") as f:
        data = f.read(5)
    if data.startswith(b"\xEF\xBB\xBF"):
        return "utf-8-sig"
    elif data.startswith(b"\xFF\xFE") or data.startswith(b"\xFE\xFF"):
        return "utf-16"
    else:  
        try:
            with io.open(fileopen, encoding="utf-8") as f:
                return "utf-8"
        except UnicodeDecodeError:
            return locale.getdefaultlocale()[1]

def create_query_string(sql_file):
    with open(sql_file, 'r', encoding=guess_encoding(sql_file)) as f_in:
        lines = f_in.read()
        query_string = textwrap.dedent("""{}""".format(lines))
    try:
        with open('data.txt', 'w') as f:
            f.write(query_string)
            f.close()

    except:
        verdad = False

    with open('data.txt') as archivo:
        for linea in archivo:
            lin = linea.replace("\n", "")
            print(lin)
            ruta, cadena_procesada, es_aceptable = automata.procesar_cadena(lin)  # Corregir esta línea
            if es_aceptable:
                sentenciasValidas.append(lin)
                print(sentenciasValidas)
    cont = str(sentenciasValidas)
    cal = cont.replace("[", "")
    lista = cal.replace("]", "")
    limp = lista.replace("'", "")
    limpio = limp.replace(",", "\n")
    with open('sentenciasValidas.txt', 'w') as f:
        f.write(limpio)
        f.close()
    sentenciasValidas.clear()
    with open('sentenciasValidas.txt') as f:
        vacio = f.readlines()
        print(vacio)
        if vacio == []:
            mb.showerror("Mensaje", "Sentencias no validas")
        else:
            showData(ruta)

def inicio():
    scene = tk.Tk()
    scene.title("Seleccion de archivo txt")
    scene['bg'] = '#2C0D8E'
    scene.geometry('400x300')
    scene.resizable(width=False, height=False)
    canvas = Canvas(scene, width=320, height=320, bg="#CEAB00")
    canvas.create_text(160, 100, text="Busque su archivo txt", fill="black", font=('Helvetica 15'))
    Button(scene, text="Agregar archivo", command=openfile).place(relx=0.5, rely=0.5, width=100, anchor='c')
    canvas.pack()
    scene.mainloop()

def draw_loop(canvas, state, state_radius, loop_radius, label):
    x, y = state
    # Dibujar un bucle sobre el estado
    canvas.create_arc(x - loop_radius, y - loop_radius - state_radius,
                      x + loop_radius, y + state_radius - loop_radius,
                      start=0, extent=180, style=tk.ARC)
    # Dibujar la flecha del bucle
    canvas.create_oval(x - 2, y - state_radius - 15,
                       x + 2, y - state_radius - 11, fill='black')
    # Etiqueta del bucle
    canvas.create_text(x, y - state_radius - 25, text=label, font=("Helvetica", 8))

def draw_arc(canvas, start, end, inflection, state_radius, label):
    # Genera dos puntos de control para la curva
    control1_x = start[0] + (inflection[0] - start[0]) / 2
    control1_y = start[1] + (inflection[1] - start[1]) / 2
    control2_x = end[0] + (inflection[0] - end[0]) / 2
    control2_y = end[1] + (inflection[1] - end[1]) / 2
    
    # Dibujar la curva usando la función create_line con la opción smooth
    canvas.create_line(
        start[0], start[1], 
        control1_x, control1_y, 
        inflection[0], inflection[1],
        control2_x, control2_y,
        end[0], end[1],
        smooth=True,
        arrow=tk.LAST
    )
    
    # Etiqueta para la transición
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    canvas.create_text(mid_x, mid_y, text=label, font=("Helvetica", 8))

def draw_automata(canvas, ruta):
    # Definición de los estados y sus posiciones
    states = {
        'q0': (50, 100), 'q1': (150, 100), 'q2': (250, 100),
        'q3': (150, 250), 'q4': (250, 250), 'q5': (350, 250)
    }
    state_radius = 30
    loop_radius = 20  # Radio para los bucles

    # Dibujar los estados
    for state, position in states.items():
        canvas.create_oval(position[0] - state_radius, position[1] - state_radius,
                           position[0] + state_radius, position[1] + state_radius)
        canvas.create_text(position[0], position[1], text=state)

    # Definición de las transiciones
    transitions = {
        ("q0", "a"): "q1",
        ("q0", "b"): "q3",
        ("q0", "c"): "q3",
        ("q1", "c"): "q2",
        ("q1", "b"): "q5",
        ("q1", "a"): "q4",
        ("q2", "a"): "q2",
        ("q2", "b"): "q2",
        ("q2", "c"): "q2",
        ("q3", "b"): "q3",
        ("q3", "c"): "q3",
        ("q3", "a"): "q4",
        ("q4", "a"): "q4",  # Ejemplo de un bucle
        ("q4", "c"): "q3",
        ("q4", "b"): "q5",
        ("q5", "a"): "q4",
        ("q5", "b"): "q3",
        ("q5", "c"): "q3",
    }

    # Dibujar las transiciones regulares y los bucles
    for (start_state, input_char), end_state in transitions.items():
        start = states[start_state]
        end = states[end_state]
        if start_state == end_state:
            draw_loop(canvas, start, state_radius, loop_radius, input_char)
        else:
            # Dibujar transiciones regulares
            angle = math.atan2(end[1] - start[1], end[0] - start[0])
            start_x = start[0] + state_radius * math.cos(angle)
            start_y = start[1] + state_radius * math.sin(angle)
            end_x = end[0] - state_radius * math.cos(angle)
            end_y = end[1] - state_radius * math.sin(angle)
            canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST)
            label_x = (start_x + end_x) / 2
            label_y = (start_y + end_y) / 2
            canvas.create_text(label_x, label_y, text=input_char, font=("Helvetica", 8))

    # Dibujar una curva especial para la transición de q5 a q3
    inflection = (states['q5'][0], states['q5'][1] - 200)  # Punto de inflexión para la curva
    draw_arc(canvas, states['q5'], states['q3'], inflection, state_radius, "b,c")

    # Dibujar la ruta
    for i in range(len(ruta) - 1):
        start_state = ruta[i]
        end_state = ruta[i + 1]
        start = states[start_state]
        end = states[end_state]
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        start_x = start[0] + state_radius * math.cos(angle)
        start_y = start[1] + state_radius * math.sin(angle)
        end_x = end[0] - state_radius * math.cos(angle)
        end_y = end[1] - state_radius * math.sin(angle)
        canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=2)



def showData(ruta):
    scene = Tk()
    scene.title('AFD Visualization')
    scene.geometry('800x600')
    scene['bg'] = '#2C0D8E'

    # Crear un canvas para dibujar el autómata
    canvas = Canvas(scene, width=800, height=600, bg="white")
    canvas.pack(pady=15, padx=10)

    # Llamar a la función para dibujar el autómata
    draw_automata(canvas, ruta)

    scene.mainloop()

if __name__ == '__main__':
    inicio()