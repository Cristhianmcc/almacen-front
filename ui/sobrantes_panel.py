import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post

class SobrantesPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_sobrantes()

    def create_widgets(self):
        self.configure(style='TFrame')
        self.lbl_title = ttk.Label(self, text="Sobrantes de Inventario", font=("Segoe UI", 20, "bold"), background="#f7f7f7", foreground="#43a047")
        self.lbl_title.pack(pady=30)
        filtro_frame = tk.Frame(self, bg="#f7f7f7")
        filtro_frame.pack(fill='x', pady=10)
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#333", "bg": "#f7f7f7"}
        entry_style = {"background": "#fff", "foreground": "#222", "relief": "solid", "borderwidth": 2, "font": ("Segoe UI", 12)}
        tk.Label(filtro_frame, text="Buscar:", **label_style).pack(side='left')
        self.filtro_var = tk.StringVar()
        tk.Entry(filtro_frame, textvariable=self.filtro_var, **entry_style).pack(side='left', padx=5)
        tk.Button(filtro_frame, text="Buscar", command=self.cargar_sobrantes, bg="#1976d2", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#1565c0").pack(side='left', padx=8)
        tk.Button(filtro_frame, text="Nuevo Sobrante", command=self.nuevo_sobrante, bg="#ab47bc", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#8e24aa").pack(side='left', padx=8)
        tabla_frame = tk.Frame(self, bg="#f7f7f7")
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="#fff", fieldbackground="#fff")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#e8f5e9")
        columns = ("id", "producto_id", "cantidad", "fecha_sobrante", "fecha_envio", "destino", "estado_envio", "usuario")
        self.tabla = ttk.Treeview(tabla_frame, columns=columns, show='headings', style="Treeview")
        for col in columns:
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
            self.tabla.column(col, width=100)
        self.tabla.pack(fill='both', expand=True, padx=10, pady=10)
        self.lbl_status = ttk.Label(self, text="Sobrantes cargados: 0")
        self.lbl_status.pack(anchor='w', padx=5, pady=2)

    def cargar_sobrantes(self):
        try:
            response = get("/surplus")
            if not response.success:
                raise Exception(response.message or "Error al obtener sobrantes")
            sobrantes = response.data or []
            filtro = self.filtro_var.get().lower()
            self.tabla.delete(*self.tabla.get_children())
            count = 0
            for sobrante in sobrantes:
                producto_id = sobrante.get("producto_id", "")
                cantidad = sobrante.get("cantidad", "")
                fecha_sobrante = sobrante.get("fecha_sobrante", "")
                fecha_envio = sobrante.get("fecha_envio", "")
                destino = sobrante.get("destino", "")
                estado_envio = sobrante.get("estado_envio", "")
                usuario = sobrante.get("usuario", "")
                if filtro in str(producto_id).lower() or filtro in str(destino).lower():
                    self.tabla.insert('', 'end', values=(
                        sobrante.get("id"), producto_id, cantidad, fecha_sobrante, fecha_envio, destino, estado_envio, usuario
                    ))
                    count += 1
            self.lbl_status.config(text=f"Sobrantes cargados: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nuevo_sobrante(self):
        messagebox.showinfo("Nuevo Sobrante", "Funcionalidad para crear sobrante")
