#importamos todo lo necesario para que funcione
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import random
import unicodedata
import os
import sys
import pygame
import sqlite3
from datetime import datetime

#arrancar la musica y la base de datos
def ejecutar_zona_safari():
    global conn, cursor 
    pygame.mixer.init()
    pygame.mixer.music.load("audio/musica.mp3")
    pygame.mixer.music.play(-1)

    # Iniciar la conexión a la base de datos
    conn = sqlite3.connect("zona_safari.db")
    cursor = conn.cursor()
    
    #inicializar las tablas
    inicializar_base_datos()
    cargar_datos_iniciales()


# Datos iniciales para cuando la bbdd no esta ya creada
pokemones = [
    # Pokemon de la pradera
    {"nombre": "Charmander", "tipo": "Fuego", "habitat": "Pradera"},
    {"nombre": "Charmeleon", "tipo": "Fuego", "habitat": "Pradera"},
    {"nombre": "Charizard", "tipo": "Fuego/Volador", "habitat": "Pradera"},
    {"nombre": "Dratini", "tipo": "Dragón", "habitat": "Pradera"},
    {"nombre": "Dragonair", "tipo": "Dragón", "habitat": "Pradera"},
    {"nombre": "Dragonite", "tipo": "Dragón/Volador", "habitat": "Pradera"},
    {"nombre": "Eevee", "tipo": "Normal", "habitat": "Pradera"},
    {"nombre": "Vaporeon", "tipo": "Agua", "habitat": "Pradera"},
    {"nombre": "Jolteon", "tipo": "Eléctrico", "habitat": "Pradera"},
    {"nombre": "Flareon", "tipo": "Fuego", "habitat": "Pradera"},
    {"nombre": "Growlithe", "tipo": "Fuego", "habitat": "Pradera"},
    {"nombre": "Arcanine", "tipo": "Fuego", "habitat": "Pradera"},
    {"nombre": "Growlithe de Hisui", "tipo": "Fuego/Roca", "habitat": "Pradera"},
    {"nombre": "Arcanine de Hisui", "tipo": "Fuego/Roca", "habitat": "Pradera"},
    {"nombre": "Togepi", "tipo": "Hada", "habitat": "Pradera"},
    {"nombre": "Togetic", "tipo": "Hada/Volador", "habitat": "Pradera"},
    {"nombre": "Togekiss", "tipo": "Hada/Volador", "habitat": "Pradera"},

    # Pokemon del lago
    {"nombre": "Squirtle", "tipo": "Agua", "habitat": "Lago"},
    {"nombre": "Wartortle", "tipo": "Agua", "habitat": "Lago"},
    {"nombre": "Blastoise", "tipo": "Agua", "habitat": "Lago"},
    {"nombre": "Lapras", "tipo": "Agua/Hielo", "habitat": "Lago"},
    {"nombre": "Feebas", "tipo": "Agua", "habitat": "Lago"},
    {"nombre": "Milotic", "tipo": "Agua", "habitat": "Lago"},

    # Pokemon del bosque
    {"nombre": "Bulbasaur", "tipo": "Planta/Veneno", "habitat": "Bosque"},
    {"nombre": "Ivysaur", "tipo": "Planta/Veneno", "habitat": "Bosque"},
    {"nombre": "Venusaur", "tipo": "Planta/Veneno", "habitat": "Bosque"},
    {"nombre": "Scyther", "tipo": "Bicho/Volador", "habitat": "Bosque"},

    # Pokemon de la montaña
    {"nombre": "Machop", "tipo": "Lucha", "habitat": "Montaña"},
    {"nombre": "Machoke", "tipo": "Lucha", "habitat": "Montaña"},
    {"nombre": "Machamp", "tipo": "Lucha", "habitat": "Montaña"},
    {"nombre": "Larvitar", "tipo": "Roca/Tierra", "habitat": "Montaña"},
    {"nombre": "Pupitar", "tipo": "Roca/Tierra", "habitat": "Montaña"},
    {"nombre": "Tyranitar", "tipo": "Roca/Siniestro", "habitat": "Montaña"},
    {"nombre": "Beldum", "tipo": "Acero/Psíquico", "habitat": "Montaña"},
    {"nombre": "Metang", "tipo": "Acero/Psíquico", "habitat": "Montaña"},
    {"nombre": "Metagross", "tipo": "Acero/Psíquico", "habitat": "Montaña"},
    {"nombre": "Riolu", "tipo": "Lucha", "habitat": "Montaña"},
    {"nombre": "Lucario", "tipo": "Lucha/Acero", "habitat": "Montaña"},

    # Pokemon de la mansión oscura
    {"nombre": "Honedge", "tipo": "Acero/Fantasma", "habitat": "Mansión oscura"},
    {"nombre": "Doublade", "tipo": "Acero/Fantasma", "habitat": "Mansión oscura"},
    {"nombre": "Aegislash", "tipo": "Acero/Fantasma", "habitat": "Mansión oscura"},
    {"nombre": "Litwick", "tipo": "Fantasma/Fuego", "habitat": "Mansión oscura"},
    {"nombre": "Lampent", "tipo": "Fantasma/Fuego", "habitat": "Mansión oscura"},
    {"nombre": "Chandelure", "tipo": "Fantasma/Fuego", "habitat": "Mansión oscura"},
    
    # Pokemon del Templo legendario
    {"nombre": "Zapdos", "tipo": "Eléctrico/Volador", "habitat": "Templo legendario"},
    {"nombre": "Articuno", "tipo": "Hielo/Volador", "habitat": "Templo legendario"},
    {"nombre": "Moltres", "tipo": "Fuego/Volador", "habitat": "Templo legendario"},
    {"nombre": "Rayquaza", "tipo": "Dragón/Volador", "habitat": "Templo legendario"},
    {"nombre": "Suicune", "tipo": "Agua", "habitat": "Templo legendario"},
    {"nombre": "Entei", "tipo": "Fuego", "habitat": "Templo legendario"},
    {"nombre": "Raikou", "tipo": "Eléctrico", "habitat": "Templo legendario"},
    {"nombre": "Lugia", "tipo": "Psíquico/Volador", "habitat": "Templo legendario"},
    {"nombre": "Ho-Oh", "tipo": "Fuego/Volador", "habitat": "Templo legendario"},
    {"nombre": "Reshiram", "tipo": "Dragón/Fuego", "habitat": "Templo legendario"},
    {"nombre": "Zekrom", "tipo": "Dragón/Eléctrico", "habitat": "Templo legendario"},
    {"nombre": "Kyurem", "tipo": "Dragón/Hielo", "habitat": "Templo legendario"},
    {"nombre": "Groudon", "tipo": "Tierra", "habitat": "Templo legendario"},
    {"nombre": "Kyogre", "tipo": "Agua", "habitat": "Templo legendario"},
]

# Lista de empleados
empleados = [
    # Veterinarios
    {"nombre": "Julia Estrada", "cargo": "Veterinaria", "turno": "Mañana"},
    {"nombre": "Luis Caballero", "cargo": "Veterinaria", "turno": "Tarde"},
    {"nombre": "Ana Ríos", "cargo": "Veterinaria", "turno": "Noche"},

    # Cuidadores de dragones
    {"nombre": "Carlos Rivera", "cargo": "Cuidador de dragones", "turno": "Tarde"},
    {"nombre": "David Soto", "cargo": "Cuidador de dragones", "turno": "Mañana"},
    {"nombre": "Rosa Jiménez", "cargo": "Cuidador de dragones", "turno": "Noche"},

    # Guías turísticos
    {"nombre": "Elena Torres", "cargo": "Guía turística", "turno": "Mañana"},
    {"nombre": "Sergio López", "cargo": "Guía turística", "turno": "Tarde"},
    {"nombre": "Clara Ramírez", "cargo": "Guía turística", "turno": "Tarde"},

    # Investigadores
    {"nombre": "Miguel Paredes", "cargo": "Investigador de legendarios", "turno": "Noche"},
    {"nombre": "Alberto Vega", "cargo": "Investigador de legendarios", "turno": "Mañana"},
    {"nombre": "Natalia Fuentes", "cargo": "Investigador de legendarios", "turno": "Tarde"},

    # Cuidadores de fantasmas
    {"nombre": "Sara Muñoz", "cargo": "Cuidadora de fantasmas", "turno": "Tarde"},
    {"nombre": "Manuel Herrera", "cargo": "Cuidadora de fantasmas", "turno": "Mañana"},
    {"nombre": "Patricia Cano", "cargo": "Cuidadora de fantasmas", "turno": "Noche"},

    # Encargados del lago
    {"nombre": "Tomás Navarro", "cargo": "Encargado del lago", "turno": "Mañana"},
    {"nombre": "Andrea Morales", "cargo": "Encargado del lago", "turno": "Tarde"},
    {"nombre": "Iván Delgado", "cargo": "Encargado del lago", "turno": "Noche"},

    # Supervisores generales
    {"nombre": "Lucía Blanco", "cargo": "Supervisora general", "turno": "Rotativo"},
    {"nombre": "Hugo Gómez", "cargo": "Supervisora general", "turno": "Rotativo"},
    {"nombre": "Isabel Méndez", "cargo": "Supervisora general", "turno": "Rotativo"},
]

#Historial médico de Pokémon creado ya para no tenerlo vacio
historial_medico = [
    {"pokemon": "Riolu", "fecha": "2023-05-10", "diagnostico": "Quemaduras leves", "tratamiento": "Pomada para quemaduras"},
    {"pokemon": "Charizard", "fecha": "2023-05-15", "diagnostico": "Ala fracturada", "tratamiento": "Reposo y vendaje"},
    {"pokemon": "Bulbasaur", "fecha": "2023-05-20", "diagnostico": "Intoxicación", "tratamiento": "Antídoto y reposo"},
]

# variables de colores de fondo para llamarlos cuando hagan falta
COLOR_FONDO = "#E3F2FD"
COLOR_PRIMARIO = "#2196F3"
COLOR_SECUNDARIO = "#0D47A1"
COLOR_EXITO = "#4CAF50"
COLOR_PELIGRO = "#F44336"

# Funciones principales
def inicializar_base_datos():
    #creamos la informacion de la bbdd si no esta hecho ya
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemones (
            nombre TEXT PRIMARY KEY,
            tipo TEXT,
            habitat TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            nombre TEXT PRIMARY KEY,
            cargo TEXT,
            turno TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_medico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pokemon TEXT,
            fecha TEXT,
            diagnostico TEXT,
            tratamiento TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos_parque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento TEXT,
            fecha TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS informes_parque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            informe TEXT,
            fecha TEXT
        )
    """)
    conn.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemones (
            nombre TEXT PRIMARY KEY,
            tipo TEXT,
            habitat TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            nombre TEXT PRIMARY KEY,
            cargo TEXT,
            turno TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_medico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pokemon TEXT,
            fecha TEXT,
            diagnostico TEXT,
            tratamiento TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos_parque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento TEXT,
            fecha TEXT
        )
    """)
    conn.commit()



def cargar_datos_iniciales():
    # Verifica si ya hay datos en la tabla de Pokémon
    cursor.execute("SELECT COUNT(*) FROM pokemones")
    if cursor.fetchone()[0] == 0:
        for p in pokemones:
            cursor.execute("INSERT INTO pokemones (nombre, tipo, habitat) VALUES (?, ?, ?)", (p["nombre"], p["tipo"], p["habitat"]))
        print("✅ Pokemones cargados")

    # Verifica si ya hay empleados
    cursor.execute("SELECT COUNT(*) FROM empleados")
    if cursor.fetchone()[0] == 0:
        for e in empleados:
            cursor.execute("INSERT INTO empleados (nombre, cargo, turno) VALUES (?, ?, ?)", (e["nombre"], e["cargo"], e["turno"]))
        print("✅ Empleados cargados")

    # Verifica si ya hay historial médico
    cursor.execute("SELECT COUNT(*) FROM historial_medico")
    if cursor.fetchone()[0] == 0:
        for h in historial_medico:
            cursor.execute("INSERT INTO historial_medico (pokemon, fecha, diagnostico, tratamiento) VALUES (?, ?, ?, ?)", (h["pokemon"], h["fecha"], h["diagnostico"], h["tratamiento"]))
        print("✅ Historial médico cargado")

    conn.commit()

def mostrar_informes_anteriores():
    # Abre una ventana nueva para mostrar los informes guardados
    ventana = tk.Toplevel(root)
    ventana.title("📋 Registros de Informes Anteriores")
    ventana.geometry("1000x700")
    ventana.configure(bg=COLOR_FONDO)
    
    # Establecer icono si existe
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    # Frame principal donde se mostrará la lista
    frame_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_principal.pack(pady=20, padx=10, fill="both", expand=True)

    # Lista con scroll
    frame_lista = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_lista.pack(fill="both", expand=True)
    scrollbar = ttk.Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")

    lista_informes = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, width=100, height=20, font=("Courier", 10))
    scrollbar.config(command=lista_informes.yview)

    # Obtener las fechas de los informes en orden descendente
    cursor.execute("SELECT fecha FROM informes_parque ORDER BY fecha DESC")
    fechas = [fecha[0] for fecha in cursor.fetchall()]
    
    # Insertar cada informe en la lista
    for fecha in fechas:
        lista_informes.insert(tk.END, f"📅 Informe del {fecha}")
    lista_informes.pack(fill="both", expand=True)

    # Botones para ver detalle o cerrar
    frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_botones.pack(pady=10)

    def mostrar_informe_seleccionado():
        # Mostrar contenido del informe seleccionado
        seleccion = lista_informes.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un informe")
            return
        
        indice = seleccion[0]
        cursor.execute("SELECT informe FROM informes_parque ORDER BY fecha DESC LIMIT 1 OFFSET ?", (indice,))
        informe = cursor.fetchone()[0]

        ventana_informe = tk.Toplevel(ventana)
        ventana_informe.title("Informe completo")
        ventana_informe.geometry("700x500")

        texto_informe = tk.Text(ventana_informe, wrap="word", font=("Courier", 10))
        scrollbar_informe = ttk.Scrollbar(ventana_informe, command=texto_informe.yview)
        texto_informe.configure(yscrollcommand=scrollbar_informe.set)
        
        scrollbar_informe.pack(side="right", fill="y")
        texto_informe.pack(fill="both", expand=True)

        texto_informe.insert("1.0", informe)
        texto_informe.config(state="disabled")  # Solo lectura

    # Botones para interactuar
    tk.Button(frame_botones, text="Ver Informe Completo", command=mostrar_informe_seleccionado, bg=COLOR_PRIMARIO, fg="white").pack(side="left", padx=5)

    tk.Button(frame_botones, text="Cerrar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white").pack(side="left", padx=5)


def mostrar_eventos_parque():
    # Ventana para ver eventos registrados (apertura, cierre, etc.)
    ventana = tk.Toplevel(root)
    ventana.title("📅 Eventos del Parque")
    ventana.geometry("1000x700")
    ventana.configure(bg=COLOR_FONDO)

    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=20, padx=10, fill="both", expand=True)

    # Scroll para la tabla
    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    # Tabla con columnas: Evento, Fecha
    tabla = ttk.Treeview(frame, columns=("Evento", "Fecha"), show="headings", yscrollcommand=scrollbar.set)
    scrollbar.config(command=tabla.yview)

    tabla.heading("Evento", text="Evento")
    tabla.heading("Fecha", text="Fecha")
    tabla.column("Evento", width=150)
    tabla.column("Fecha", width=300)

    # Llenar la tabla con eventos de la base de datos
    cursor.execute("SELECT evento, fecha FROM eventos_parque ORDER BY fecha DESC")
    for evento, fecha in cursor.fetchall():
        tabla.insert("", "end", values=(evento, fecha))

    tabla.pack(fill="both", expand=True)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white").pack(pady=10)


def simular_entrada_salida():
    # Simula entradas de visitantes mientras el parque esté abierto
    if estado_parque["abierto"]:
        tipo = random.choice(list(precios_entradas.keys()))
        estadisticas["entradas"][tipo] += 1
        estadisticas["ingresos"][tipo] += precios_entradas[tipo]
        estadisticas["total_personas"] += 1
        estadisticas["total_ingresos"] += precios_entradas[tipo]
        # Repetir cada segundo
        estado_parque["simulacion"] = root.after(1000, simular_entrada_salida)


def registrar_evento(evento):
    # Guarda en la base de datos eventos como apertura y cierre
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO eventos_parque (evento, fecha) VALUES (?, ?)", (evento, ahora))
    conn.commit()


def abrir_cerrar_parque():
    # Alterna entre abrir y cerrar el parque
    estado_parque["abierto"] = not estado_parque["abierto"]
    if estado_parque["abierto"]:
        simular_entrada_salida()
        btn_abrir.config(bg=COLOR_EXITO, text="Cerrar Parque")
        registrar_evento("Apertura")
        messagebox.showinfo("Zona Safari", "¡Parque abierto al público!")
    else:
        if estado_parque["simulacion"]:
            root.after_cancel(estado_parque["simulacion"])
        btn_abrir.config(bg=COLOR_PELIGRO, text="Abrir Parque")
        registrar_evento("Cierre")
        messagebox.showinfo("Zona Safari", "Parque cerrado")


def mostrar_informe():
    # Genera un resumen de visitas e ingresos
    informe = "📊 INFORME DEL PARQUE 📊\n\n"
    informe += f"👥 Visitantes totales: {estadisticas['total_personas']}\n"
    informe += f"💰 Ingresos totales: {estadisticas['total_ingresos']} €\n\n"
    
    for tipo, cantidad in estadisticas["entradas"].items():
        informe += f"🎟️ {tipo}: {cantidad} entradas ({estadisticas['ingresos'][tipo]} €)\n"
    
    # Guarda el informe en la base de datos
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO informes_parque (informe, fecha) VALUES (?, ?)", (informe, ahora))
    conn.commit()
    
    messagebox.showinfo("Informe General", informe)


# Funciones relacionadas con Pokémon 
def mostrar_pokemon_por_habitat():
    # Muestra una ventana con botones para cada hábitat
    ventana = tk.Toplevel(root)
    ventana.title("🌍 Hábitats Pokémon")
    ventana.geometry("1000x700")
    ventana.configure(bg=COLOR_FONDO)

    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    # Lista única de hábitats disponibles
    habitats = sorted(list({p["habitat"] for p in pokemones}))

    frame_habitats = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_habitats.pack(pady=20, fill="both", expand=True)

    tk.Label(frame_habitats, text="Selecciona un hábitat:", font=("Arial", 12, "bold"), bg=COLOR_FONDO).pack()

    # Asignación de colores personalizados a cada hábitat
    colores_habitats = {
        "Montaña": "#FF5722",
        "Lago": "#2196F3",
        "Bosque": "#4CAF50",
        "Pradera": "#8BC34A",
        "Mansión oscura": "#673AB7",
        "Templo legendario": "#FFC107"
    }

    # Crear un botón para cada hábitat
    for habitat in habitats:
        color = colores_habitats.get(habitat, COLOR_PRIMARIO)
        btn = tk.Button(frame_habitats, text=habitat, width=20, command=lambda h=habitat: mostrar_pokemon_de_habitat(h), bg=color, fg="white", font=("Arial", 10))
        btn.pack(pady=5)


def mostrar_pokemon_de_habitat(habitat):
    # Recupera los Pokémon de ese hábitat desde la BBDD
    cursor.execute("SELECT nombre, tipo FROM pokemones WHERE habitat = ?", (habitat,))
    pokemones_habitat = [{"nombre": nombre, "tipo": tipo, "habitat": habitat} for nombre, tipo in cursor.fetchall()]
    num_pokemon = len(pokemones_habitat)

    # Cálculo de tamaño de ventana según cantidad de Pokémon
    columnas = 3
    filas = (num_pokemon + columnas - 1) // columnas
    ancho_ventana = 700
    alto_ventana = min(800, 200 + filas * 130)

    ventana = tk.Toplevel(root)
    ventana.title(f"Pokémon de {habitat}")
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
    ventana.resizable(False, False)

    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    # Fondo de la ventana (si existe imagen correspondiente)
    ruta_fondo = os.path.join("imagenes", f"{normalizar_nombre(habitat)}.png")
    if os.path.exists(ruta_fondo):
        try:
            imagen_fondo = Image.open(ruta_fondo).resize((ancho_ventana, alto_ventana))
            fondo = ImageTk.PhotoImage(imagen_fondo)
            label_fondo = tk.Label(ventana, image=fondo)
            label_fondo.image = fondo
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error al cargar fondo: {e}")

    # Título
    tk.Label(ventana, text=f"Pokémon en {habitat} ({num_pokemon} encontrados):", font=("Arial", 14, "bold"), bg=COLOR_FONDO).place(x=20, y=20)

    # Botones para cada Pokémon del hábitat
    ancho_btn = 180
    alto_btn = 80
    separacion_x = 20
    separacion_y = 20
    margen_superior = 70

    for i, pokemon in enumerate(pokemones_habitat):
        fila = i // columnas
        columna = i % columnas
        x = separacion_x + columna * (ancho_btn + separacion_x)
        y = margen_superior + fila * (alto_btn + separacion_y)

        tk.Button(ventana, text=f"{pokemon['nombre']}\n({pokemon['tipo']})", command=lambda p=pokemon: mostrar_imagen_pokemon(p), bg="#4CAF50", fg="white", font=("Arial", 11), width=18, height=3, 
                wraplength=150).place(x=x, y=y)

    # Botón para cerrar
    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white", font=("Arial", 11), width=15).place(x=(ancho_ventana - 150) // 2, y=alto_ventana - 60)


def normalizar_nombre(nombre):
    # Transforma un nombre en un formato compatible para archivos
    nombre = nombre.lower().replace(" ", "_").replace("de_", "")
    nombre = unicodedata.normalize("NFD", nombre).encode("ascii", "ignore").decode("utf-8")
    return nombre


def mostrar_imagen_pokemon(pokemon):
    # Ventana con imagen y sonido del Pokémon seleccionado
    ventana = tk.Toplevel(root)
    ventana.title(pokemon["nombre"])
    ventana.geometry("900x900")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    frame_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

    try:
        # Detener música general, reproducir sonido del Pokémon
        pygame.mixer.music.stop()
        nombre_archivo_audio = normalizar_nombre(pokemon['nombre'])
        ruta_audio = os.path.join("audio", f"{nombre_archivo_audio}.mp3")
        if os.path.exists(ruta_audio):
            sonido = pygame.mixer.Sound(ruta_audio)
            sonido.play()
            # Reanudar música general al terminar
            ventana.after(int(sonido.get_length() * 1000), lambda: pygame.mixer.music.play(-1))

        # Mostrar imagen del Pokémon
        nombre_archivo_img = pokemon['nombre'].lower().replace(" ", "_").replace("de_", "")
        img_path = os.path.join("imagenes", f"{nombre_archivo_img}.png")

        if os.path.exists(img_path):
            img = PhotoImage(file=img_path)
            label_imagen = tk.Label(frame_principal, image=img, bg=COLOR_FONDO)
            label_imagen.image = img
            label_imagen.pack(pady=20)
        else:
            tk.Label(frame_principal, text="Imagen no encontrada", font=("Arial", 12), bg=COLOR_FONDO, fg="red").pack(pady=20)

    except Exception as e:
        tk.Label(frame_principal, text="Error cargando imagen", font=("Arial", 12), bg=COLOR_FONDO, fg="red").pack(pady=20)

    # Mostrar datos del Pokémon
    info = f"Nombre: {pokemon['nombre']} Tipo: {pokemon['tipo']} Hábitat: {pokemon['habitat']}"
    tk.Label(frame_principal, text=info, font=("Arial", 12), bg=COLOR_FONDO).pack(pady=10)

    # Botón cerrar y reanudar música
    def cerrar_y_reanudar():
        ventana.destroy()
        pygame.mixer.music.play(-1)

    tk.Button(frame_principal, text="Cerrar", command=cerrar_y_reanudar, bg=COLOR_PELIGRO, fg="white").pack(pady=10)


#Funciones para el menú de Enfermera Joy
def mostrar_historial_medico():
    #muestra los acontecimientos medicos ya existentes
    ventana = tk.Toplevel(root)
    ventana.title("🏥 Historial Médico - Enfermera Joy")
    ventana.geometry("800x500")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_principal.pack(pady=20, padx=10, fill="both", expand=True)
    
    # Frame para los botones de acción
    frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_botones.pack(fill="x", pady=10)
    
    tk.Button(frame_botones, text="Añadir Registro", command=agregar_registro_medico, bg=COLOR_EXITO, fg="white", font=("Arial", 10)).pack(side="left", padx=5)
    tk.Button(frame_botones, text="Eliminar Registro", command=eliminar_registro_medico, bg=COLOR_PELIGRO, fg="white", font=("Arial", 10)).pack(side="left", padx=5)
    
    # Tabla de historial médico
    frame_tabla = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_tabla.pack(fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")
    
    tabla = ttk.Treeview(frame_tabla, columns=("Pokémon", "Fecha", "Diagnóstico", "Tratamiento"), yscrollcommand=scrollbar.set, height=15)
    scrollbar.config(command=tabla.yview)
    
    tabla.heading("#0", text="ID")
    tabla.heading("Pokémon", text="Pokémon")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Diagnóstico", text="Diagnóstico")
    tabla.heading("Tratamiento", text="Tratamiento")
    
    tabla.column("#0", width=50, stretch=tk.NO)
    tabla.column("Pokémon", width=120)
    tabla.column("Fecha", width=100)
    tabla.column("Diagnóstico", width=250)
    tabla.column("Tratamiento", width=250)
    
    cursor.execute("SELECT pokemon, fecha, diagnostico, tratamiento FROM historial_medico")
    for i, (pokemon, fecha, diagnostico, tratamiento) in enumerate(cursor.fetchall(), start=1):
        tabla.insert("", "end", text=str(i), values=(pokemon, fecha, diagnostico, tratamiento))

    
    tabla.pack(fill="both", expand=True)
    
    tk.Button(frame_principal, text="Cerrar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white", font=("Arial", 10)).pack(pady=10)

def agregar_registro_medico():
    #funcion para agregar nuevos registros medicos
    ventana = tk.Toplevel(root)
    ventana.title("➕ Añadir Registro Médico")
    ventana.geometry("400x300")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    tk.Label(frame, text="Pokémon:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
    entry_pokemon = tk.Entry(frame, width=30)
    entry_pokemon.grid(row=0, column=1, pady=5, padx=5)
    
    tk.Label(frame, text="Fecha (YYYY-MM-DD):", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
    entry_fecha = tk.Entry(frame, width=30)
    entry_fecha.grid(row=1, column=1, pady=5, padx=5)
    
    tk.Label(frame, text="Diagnóstico:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=5)
    entry_diagnostico = tk.Entry(frame, width=30)
    entry_diagnostico.grid(row=2, column=1, pady=5, padx=5)
    
    tk.Label(frame, text="Tratamiento:", bg=COLOR_FONDO).grid(row=3, column=0, sticky="w", pady=5)
    entry_tratamiento = tk.Entry(frame, width=30)
    entry_tratamiento.grid(row=3, column=1, pady=5, padx=5)
    
    def guardar_registro():
        #funcion que guarda el nuevo registro medico
        nuevo_registro = {
            "pokemon": entry_pokemon.get(),
            "fecha": entry_fecha.get(),
            "diagnostico": entry_diagnostico.get(),
            "tratamiento": entry_tratamiento.get()
        }
        cursor.execute("INSERT INTO historial_medico (pokemon, fecha, diagnostico, tratamiento) VALUES (?, ?, ?, ?)", (entry_pokemon.get(), entry_fecha.get(), entry_diagnostico.get(), entry_tratamiento.get()))
        conn.commit()
        messagebox.showinfo("Éxito", "Registro médico añadido correctamente")

        ventana.destroy()
        mostrar_historial_medico()
    
    tk.Button(frame, text="Guardar", command=guardar_registro, bg=COLOR_EXITO, fg="white").grid(row=4, column=1, pady=10, sticky="e")
    tk.Button(frame, text="Cancelar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white").grid(row=4, column=0, pady=10, sticky="w")

def eliminar_registro_medico():
    #funcion para eliminar historiales medicos
    if not historial_medico:
        messagebox.showwarning("Advertencia", "No hay registros médicos para eliminar")
        return
    
    ventana = tk.Toplevel(root)
    ventana.title("🗑️ Eliminar Registro Médico")
    ventana.geometry("400x200")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    tk.Label(frame, text="Seleccione el registro a eliminar:", bg=COLOR_FONDO).pack()
    
    lista_registros = tk.Listbox(frame, width=50, height=6)
    for i, registro in enumerate(historial_medico):
        lista_registros.insert(tk.END, f"{i+1}. {registro['pokemon']} - {registro['diagnostico']} ({registro['fecha']})")
    lista_registros.pack(pady=10)
    
    def confirmar_eliminacion():
        seleccion = lista_registros.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un registro")
            return
        
        indice = seleccion[0]
        cursor.execute("DELETE FROM historial_medico WHERE id = (SELECT id FROM historial_medico LIMIT 1 OFFSET ?)", (indice,))
        conn.commit()

        messagebox.showinfo("Éxito", "Registro médico eliminado correctamente")
        ventana.destroy()
        mostrar_historial_medico()
    
    tk.Button(frame, text="Eliminar", command=confirmar_eliminacion, bg=COLOR_PELIGRO, fg="white").pack(pady=10)

# Funciones para el menú de Empleados
def mostrar_lista_empleados():
    #muestra la lista de empleados registrados
    ventana = tk.Toplevel(root)
    ventana.title("🏢 Lista de Empleados")
    ventana.geometry("800x400")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.pack(pady=20, padx=10, fill="both", expand=True)
    
    tabla = ttk.Treeview(frame_tabla, columns=("Nombre", "Cargo", "Turno"), show="headings")
    
    tabla.heading("Nombre", text="Nombre", anchor="w")
    tabla.heading("Cargo", text="Cargo", anchor="w")
    tabla.heading("Turno", text="Turno", anchor="w")
    
    tabla.column("Nombre", width=250, anchor="w")
    tabla.column("Cargo", width=250, anchor="w")
    tabla.column("Turno", width=150, anchor="center")
    
    cursor.execute("SELECT nombre, cargo, turno FROM empleados")
    for nombre, cargo, turno in cursor.fetchall():
        tabla.insert("", "end", values=(nombre, cargo, turno))

    
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)
    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white", font=("Arial", 10)).pack(pady=10)

def gestionar_empleados():
    #funcion para dar a elegir entre añadir, eliminar o modificar turnos
    ventana = tk.Toplevel(root)
    ventana.title("👥 Gestión de Empleados")
    ventana.geometry("800x600")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_principal.pack(pady=20, padx=10, fill="both", expand=True)
    
    # Frame para los botones de acción
    frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_botones.pack(fill="x", pady=10)
    
    tk.Button(frame_botones, text="Añadir Empleado", command=agregar_empleado, bg=COLOR_EXITO, fg="white", font=("Arial", 10)).pack(side="left", padx=5)
    
    tk.Button(frame_botones, text="Eliminar Empleado", command=eliminar_empleado, bg=COLOR_PELIGRO, fg="white", font=("Arial", 10)).pack(side="left", padx=5)
    
    tk.Button(frame_botones, text="Modificar Turno", command=modificar_turno_empleado, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 10)).pack(side="left", padx=5)
    
    # Tabla de empleados
    frame_tabla = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_tabla.pack(fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")
    
    tabla = ttk.Treeview(frame_tabla, columns=("Nombre", "Cargo", "Turno"), yscrollcommand=scrollbar.set, height=15)
    scrollbar.config(command=tabla.yview)
    
    tabla.heading("#0", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Cargo", text="Cargo")
    tabla.heading("Turno", text="Turno")
    
    tabla.column("#0", width=50, stretch=tk.NO)
    tabla.column("Nombre", width=200)
    tabla.column("Cargo", width=250)
    tabla.column("Turno", width=100)
    
    cursor.execute("SELECT nombre, cargo, turno FROM empleados")
    for nombre, cargo, turno in cursor.fetchall():
        tabla.insert("", "end", values=(nombre, cargo, turno))

    
    tabla.pack(fill="both", expand=True)
    
    tk.Button(frame_principal, text="Cerrar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white", font=("Arial", 10)).pack(pady=10)

def agregar_empleado():
    #funcion para agregar empleados
    ventana = tk.Toplevel(root)
    ventana.title("➕ Añadir Empleado")
    ventana.geometry("400x300")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    tk.Label(frame, text="Nombre:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre = tk.Entry(frame, width=30)
    entry_nombre.grid(row=0, column=1, pady=5, padx=5)
    
    tk.Label(frame, text="Cargo:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
    entry_cargo = tk.Entry(frame, width=30)
    entry_cargo.grid(row=1, column=1, pady=5, padx=5)
    
    tk.Label(frame, text="Turno:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", pady=5)
    entry_turno = ttk.Combobox(frame, values=["Mañana", "Tarde", "Noche", "Rotativo"], width=27)
    entry_turno.grid(row=2, column=1, pady=5, padx=5)
    entry_turno.current(0)
    
    def guardar_empleado():
        nuevo_empleado = {
            "nombre": entry_nombre.get(),
            "cargo": entry_cargo.get(),
            "turno": entry_turno.get()
        }
        empleados.append(nuevo_empleado)
        messagebox.showinfo("Éxito", "Empleado añadido correctamente")
        ventana.destroy()
        gestionar_empleados()
    
    tk.Button(frame, text="Guardar", command=guardar_empleado, bg=COLOR_EXITO, fg="white").grid(row=3, column=1, pady=10, sticky="e")
    
    tk.Button(frame, text="Cancelar", command=ventana.destroy, bg=COLOR_PELIGRO, fg="white").grid(row=3, column=0, pady=10, sticky="w")

def eliminar_empleado():
    #funcion para despedir empleados
    if not empleados:
        messagebox.showwarning("Advertencia", "No hay empleados para eliminar")
        return
    
    ventana = tk.Toplevel(root)
    ventana.title("🗑️ Eliminar Empleado")
    ventana.geometry("400x300")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    tk.Label(frame, text="Seleccione el empleado a eliminar:", bg=COLOR_FONDO).pack()
    
    lista_empleados = tk.Listbox(frame, width=50, height=10)
    for emp in empleados:
        lista_empleados.insert(tk.END, f"{emp['nombre']} - {emp['cargo']} ({emp['turno']})")
    lista_empleados.pack(pady=10)
    
    def confirmar_eliminacion():
        seleccion = lista_empleados.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un empleado")
            return
        
        indice = seleccion[0]
        empleado_eliminado = empleados.pop(indice)
        messagebox.showinfo("Éxito", f"Empleado {empleado_eliminado['nombre']} eliminado correctamente")
        ventana.destroy()
        gestionar_empleados()
    
    tk.Button(frame, text="Eliminar", command=confirmar_eliminacion, bg=COLOR_PELIGRO, fg="white").pack(pady=10)

def modificar_turno_empleado():
    #funcion para cambiar turnos de los empleados
    if not empleados:
        messagebox.showwarning("Advertencia", "No hay empleados para modificar")
        return
    
    ventana = tk.Toplevel(root)
    ventana.title("🔄 Modificar Turno de Empleado")
    ventana.geometry("400x300")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)
    
    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    tk.Label(frame, text="Seleccione el empleado:", bg=COLOR_FONDO).pack()
    
    lista_empleados = tk.Listbox(frame, width=50, height=8)
    for emp in empleados:
        lista_empleados.insert(tk.END, f"{emp['nombre']} - {emp['cargo']} ({emp['turno']})")
    lista_empleados.pack(pady=10)
    
    tk.Label(frame, text="Nuevo turno:", bg=COLOR_FONDO).pack()
    
    nuevo_turno = ttk.Combobox(frame, values=["Mañana", "Tarde", "Noche", "Rotativo"], width=20)
    nuevo_turno.pack(pady=5)
    nuevo_turno.current(0)
    
    def confirmar_cambio():
        seleccion = lista_empleados.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un empleado")
            return
        
        indice = seleccion[0]
        empleados[indice]["turno"] = nuevo_turno.get()
        messagebox.showinfo("Éxito", f"Turno modificado correctamente para {empleados[indice]['nombre']}")
        ventana.destroy()
        gestionar_empleados()
    
    tk.Button(frame, text="Modificar", command=confirmar_cambio, bg=COLOR_PRIMARIO, fg="white").pack(pady=10)

#variables de la venta de entradas de la zona safari
precios_entradas = {"Adulto": 20, "Niño": 10, "Grupo": 15, "VIP": 50}
estadisticas = {
    "entradas": {"Adulto": 0, "Niño": 0, "Grupo": 0, "VIP": 0},
    "ingresos": {"Adulto": 0, "Niño": 0, "Grupo": 0, "VIP": 0},
    "total_personas": 0,
    "total_ingresos": 0
}
estado_parque = {"abierto": False, "simulacion": None}

#Interfaz principal
root = tk.Tk()

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
icono_path = os.path.join(script_dir, "imagenes", "icono.ico")
if os.path.exists(icono_path):
    try:
        root.iconbitmap(icono_path)
    except Exception as e:
        print("No se pudo establecer el icono:", e)

root.title("Gestión del Parque Pokémon")
root.geometry("400x500")
root.configure(bg=COLOR_FONDO)


# Título
tk.Label(root, text="Zona Safari Pokémon", font=("Helvetica", 25, "bold"), fg=COLOR_SECUNDARIO, bg=COLOR_FONDO).pack(pady=20)
imagen_safari = os.path.join("imagenes", "safari_banner.png")
if os.path.exists(imagen_safari):
    img_banner = PhotoImage(file=imagen_safari)
    tk.Label(root, image=img_banner, bg=COLOR_FONDO).pack()


# Botón para abrir/cerrar el parque
btn_abrir = tk.Button(root, text="Abrir Parque", width=25, height=2, command=abrir_cerrar_parque, bg=COLOR_PELIGRO, fg="white", font=("Helvetica", 12, "bold"))
btn_abrir.pack(pady=10)


# Frame para los menús
frame_menus = tk.Frame(root, bg=COLOR_FONDO)
frame_menus.pack(pady=10)

def abrir_menu_pokemon():
    ventana = tk.Toplevel(root)
    ventana.title("Menú Pokémon")
    ventana.geometry("300x200")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    tk.Button(ventana, text="Mostrar Pokémon", command=mostrar_pokemon_por_habitat, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=10)
    tk.Button(ventana, text="Enfermera Joy", command=mostrar_historial_medico, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=10)

def abrir_menu_empleados():
    ventana = tk.Toplevel(root)
    ventana.title("Menú Empleados")
    ventana.geometry("300x200")
    ventana.configure(bg=COLOR_FONDO)
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    tk.Button(ventana, text="Mostrar Empleados", command=mostrar_lista_empleados, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=10)
    tk.Button(ventana, text="Gestionar Empleados", command=gestionar_empleados, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=10)

# Botones principales con estilo unificado
# Dentro de la configuración de la interfaz principal, en el frame_menus:
tk.Button(frame_menus, text="Menú Pokémon", command=abrir_menu_pokemon, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=8)

tk.Button(frame_menus, text="Menú Empleados", command=abrir_menu_empleados, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=8)

tk.Button(frame_menus, text="Mostrar Informe", command=mostrar_informe, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=8)

tk.Button(frame_menus, text="Ver Informes Anteriores", command=mostrar_informes_anteriores, bg=COLOR_PRIMARIO, fg="white", font=("Arial", 11), width=25).pack(pady=8)

# Botón de salida
tk.Button(root, text="Salir", width=22, height=1, command=root.quit, bg="#616161", fg="white", font=("Arial", 11)).pack(pady=10)

def iniciar_aplicacion():
    #Función para iniciar la aplicación desde main.py
    ejecutar_zona_safari()  # Inicializa la base de datos y carga datos
    root.mainloop()         # Inicia la interfaz gráfica
