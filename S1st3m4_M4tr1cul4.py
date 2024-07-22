import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import ImageTk, Image

class Estudiante:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        self.grado = None
        self.seccion = None
    
    def matricular(self):
        raise NotImplementedError("Subclasses should implement this method")

class MatriculaService:
    @staticmethod
    def matricular_estudiante(estudiante):
        if isinstance(estudiante, EstudianteSecundaria):
            estudiante.matricular()
        else:
            messagebox.showerror("Error", "Tipo de estudiante no soportado")

class EstudianteSecundaria(Estudiante):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
        if 11 <= self.edad <= 12:
            self.grado = 1
            self.seccion = 'A'
            messagebox.showinfo("Matrícula", f"Bienvenido al sistema de matrícula escolar, {self.nombre}!\n"
                                             f"Matriculado automáticamente en 1° año de secundaria.")
        elif 13 <= self.edad <= 14:
            self._preguntar_grado(["1", "2", "3"])
        elif 14 < self.edad <= 15:
            self._preguntar_grado(["3", "4", "5"])
        elif 15 <= self.edad <= 17:
            self._preguntar_grado(["4", "5"])
        else:
            messagebox.showerror("Error", "Edad no permitida para secundaria.")

    def _preguntar_grado(self, opciones):
        eleccion = simpledialog.askstring("Matrícula", f"Bienvenido al sistema de matrícula escolar, {self.nombre}!\n"
                                                       f"Puedes matricularte en: {', '.join(opciones)}.\n"
                                                       "¿En qué grado deseas matricularte?")
        if eleccion in opciones:
            self.grado = int(eleccion)
            self.seccion = 'A'
            messagebox.showinfo("Matrícula", f"Matriculado en {self.grado}° grado, sección {self.seccion}.")
        else:
            messagebox.showerror("Error", "Opción no válida.")

    def matricular(self):
        if self.grado is not None and self.seccion is not None:
            return f"{self.nombre} - {self.edad} años - {self.grado}° grado, sección {self.seccion}"

class VistaGrado(tk.Toplevel):
    def __init__(self, parent, grado, matriculados):
        super().__init__(parent)
        self.title(f"Estudiantes en {grado}° grado")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")
        self.centrar_ventana()

        self.matriculados = matriculados
        self.grado = grado

        self.crear_interfaz()

    def centrar_ventana(self):
        ventana_width = 600
        ventana_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (ventana_width // 2)
        y = (screen_height // 2) - (ventana_height // 2)
        self.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

    def crear_interfaz(self):
        style = ttk.Style()
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#000000")

        btn_horarios = tk.Button(self, text="Horarios", command=self.mostrar_horarios, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        btn_horarios.pack(pady=10)

        estudiantes_grado = [estudiante for estudiante in self.matriculados if estudiante.grado == self.grado]

        if estudiantes_grado:
            tree = ttk.Treeview(self, columns=("Nombre", "Edad", "Grado", "Sección"), show="headings")
            tree.heading("Nombre", text="Nombre")
            tree.heading("Edad", text="Edad")
            tree.heading("Grado", text="Grado")
            tree.heading("Sección", text="Sección")

            for estudiante in estudiantes_grado:
                tree.insert("", tk.END, values=(estudiante.nombre, estudiante.edad, estudiante.grado, estudiante.seccion))

            tree.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
        else:
            label_vacio = tk.Label(self, text=f"No hay estudiantes en {self.grado}° grado.", bg="#f0f0f0", fg="#FF5733", font=("Arial", 14))
            label_vacio.pack(padx=20, pady=20)

    def mostrar_horarios(self):
        # Define la ruta de la imagen según el grado seleccionado
        imagen_path = f"HORARIO{self.grado}.jpg"

        ventana_horarios = tk.Toplevel(self)
        ventana_horarios.title(f"Horarios de {self.grado}° grado")
        ventana_horarios.configure(bg="#f0f0f0")  # Fondo gris claro

        # Centrar la ventana de horarios en la pantalla
        ventana_horarios_width = 600
        ventana_horarios_height = 400
        screen_width = ventana_horarios.winfo_screenwidth()
        screen_height = ventana_horarios.winfo_screenheight()
        x = (screen_width // 2) - (ventana_horarios_width // 2)
        y = (screen_height // 2) - (ventana_horarios_height // 2)
        ventana_horarios.geometry(f"{ventana_horarios_width}x{ventana_horarios_height}+{x}+{y}")

        # Cargar la imagen de los horarios
        try:
            imagen = Image.open(imagen_path)
            imagen = imagen.resize((500, 300))
            imagen = ImageTk.PhotoImage(imagen)

            label_imagen = tk.Label(ventana_horarios, image=imagen)
            label_imagen.image = imagen  # Guardar referencia para evitar que se elimine por el recolector de basura
            label_imagen.pack(padx=20, pady=20)

        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró la imagen {imagen_path}")

class SistemaMatricula(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Matrícula Escolar")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        self.centrar_ventana()

        self.matriculados = []

        self.crear_interfaz()

    def centrar_ventana(self):
        ventana_width = 800
        ventana_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (ventana_width // 2)
        y = (screen_height // 2) - (ventana_height // 2)
        self.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

    def crear_interfaz(self):
        frame_datos = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        frame_datos.pack()

        label_nombre = tk.Label(frame_datos, text="Nombre:", bg="#ffffff", font=("Arial", 12))
        label_nombre.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_datos, font=("Arial", 12))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        label_edad = tk.Label(frame_datos, text="Edad:", bg="#ffffff", font=("Arial", 12))
        label_edad.grid(row=1, column=0, padx=5, pady=5)
        self.entry_edad = tk.Entry(frame_datos, font=("Arial", 12))
        self.entry_edad.grid(row=1, column=1, padx=5, pady=5)

        btn_matricular = tk.Button(frame_datos, text="Matricular", command=self.matricular_estudiante, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        btn_matricular.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        frame_botones_grados = tk.Frame(self, bg="#f0f0f0")
        frame_botones_grados.pack(pady=20)

        btn_ver_1ro = tk.Button(frame_botones_grados, text="Ver 1° Grado", command=lambda: self.ver_estudiantes_por_grado(1), bg="#008CBA", fg="white", font=("Arial", 12))
        btn_ver_1ro.pack(side=tk.LEFT, padx=10)

        btn_ver_2do = tk.Button(frame_botones_grados, text="Ver 2° Grado", command=lambda: self.ver_estudiantes_por_grado(2), bg="#008CBA", fg="white", font=("Arial", 12))
        btn_ver_2do.pack(side=tk.LEFT, padx=10)

        btn_ver_3ro = tk.Button(frame_botones_grados, text="Ver 3° Grado", command=lambda: self.ver_estudiantes_por_grado(3), bg="#008CBA", fg="white", font=("Arial", 12))
        btn_ver_3ro.pack(side=tk.LEFT, padx=10)

        btn_ver_4to = tk.Button(frame_botones_grados, text="Ver 4° Grado", command=lambda: self.ver_estudiantes_por_grado(4), bg="#008CBA", fg="white", font=("Arial", 12))
        btn_ver_4to.pack(side=tk.LEFT, padx=10)

        btn_ver_5to = tk.Button(frame_botones_grados, text="Ver 5° Grado", command=lambda: self.ver_estudiantes_por_grado(5), bg="#008CBA", fg="white", font=("Arial", 12))
        btn_ver_5to.pack(side=tk.LEFT, padx=10)

        btn_salir = tk.Button(self, text="Salir", command=self.salir, bg="#FF5733", fg="white", font=("Arial", 12, "bold"))
        btn_salir.pack(pady=10)

    def matricular_estudiante(self):
        nombre = self.entry_nombre.get()
        edad = int(self.entry_edad.get())

        estudiante = EstudianteSecundaria(nombre, edad)
        MatriculaService.matricular_estudiante(estudiante)
        self.matriculados.append(estudiante)

    def ver_estudiantes_por_grado(self, grado):
        VistaGrado(self, grado, self.matriculados)

    def salir(self):
        self.destroy()

if __name__ == "__main__":
    app = SistemaMatricula()
    app.mainloop()
