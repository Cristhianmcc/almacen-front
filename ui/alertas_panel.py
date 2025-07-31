import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get

class AlertasPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_alertas()

    def create_widgets(self):
        self.configure(style='TFrame')
        header = tk.Frame(self, bg="#d81b60")
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Alertas de Inventario", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#d81b60").pack(anchor='center', pady=18)
        filtro_frame = tk.Frame(self, bg="#f7f7f7")
        filtro_frame.pack(fill='x', pady=10)
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#1976d2", "bg": "#f7f7f7"}
        entry_style = {"background": "#f3f6fb", "foreground": "#222", "relief": "flat", "borderwidth": 1, "font": ("Segoe UI", 12)}
        tk.Label(filtro_frame, text="Buscar:", **label_style).pack(side='left')
        self.filtro_var = tk.StringVar()
        tk.Entry(filtro_frame, textvariable=self.filtro_var, **entry_style).pack(side='left', padx=5)
        tk.Button(filtro_frame, text="Buscar", command=self.cargar_alertas, bg="#1976d2", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#1565c0").pack(side='left', padx=8)
        tk.Button(filtro_frame, text="Actualizar", command=self.cargar_alertas, bg="#43a047", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#388e3c").pack(side='left', padx=8)
        tabla_frame = tk.Frame(self, bg="#f7f7f7")
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="#fff", fieldbackground="#fff")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#fce4ec")
        columns = ("id", "producto_id", "tipo_alerta", "descripcion", "fecha_alerta", "estado_alerta", "nivel_prioridad")
        self.tabla = ttk.Treeview(tabla_frame, columns=columns, show='headings', style="Treeview")
        for col in columns:
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
            self.tabla.column(col, width=100)
        self.tabla.pack(fill='both', expand=True, padx=10, pady=10)
        self.lbl_status = ttk.Label(self, text="Alertas cargadas: 0")
        self.lbl_status.pack(anchor='w', padx=5, pady=2)
        ttk.Button(self, text="Ver Detalle", command=self.ver_detalle).pack(anchor='e', padx=10, pady=5)

    def cargar_alertas(self):
        try:
            response = get("/alerts")
            if not response.success:
                raise Exception(response.message or "Error al obtener alertas")
            alertas = response.data or []
            filtro = self.filtro_var.get().lower()
            self.tabla.delete(*self.tabla.get_children())
            count = 0
            for alerta in alertas:
                producto_id = alerta.get("producto_id", "")
                tipo_alerta = alerta.get("tipo_alerta", "")
                descripcion = alerta.get("descripcion", "")
                fecha_alerta = alerta.get("fecha_alerta", "")
                estado_alerta = alerta.get("estado_alerta", "")
                nivel_prioridad = alerta.get("nivel_prioridad", "")
                if filtro in str(producto_id).lower() or filtro in str(tipo_alerta).lower():
                    self.tabla.insert('', 'end', values=(
                        alerta.get("id"), producto_id, tipo_alerta, descripcion, fecha_alerta, estado_alerta, nivel_prioridad
                    ))
                    count += 1
            self.lbl_status.config(text=f"Alertas cargadas: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_detalle(self):
        messagebox.showinfo("Detalle", "Funcionalidad para ver detalle de alerta")
