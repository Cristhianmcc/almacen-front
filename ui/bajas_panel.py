import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post

class BajasPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_bajas()

    def create_widgets(self):
        self.configure(style='TFrame')
        header = tk.Frame(self, bg="#ff9800")
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Bajas de Inventario", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#ff9800").pack(anchor='center', pady=18)
        filtro_frame = tk.Frame(self, bg="#f7f7f7")
        filtro_frame.pack(fill='x', pady=10)
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#1976d2", "bg": "#f7f7f7"}
        entry_style = {"background": "#f3f6fb", "foreground": "#222", "relief": "flat", "borderwidth": 1, "font": ("Segoe UI", 12)}
        tk.Label(filtro_frame, text="Buscar:", **label_style).pack(side='left')
        self.filtro_var = tk.StringVar()
        tk.Entry(filtro_frame, textvariable=self.filtro_var, **entry_style).pack(side='left', padx=5)
        tk.Button(filtro_frame, text="Buscar", command=self.cargar_bajas, bg="#1976d2", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#1565c0").pack(side='left', padx=8)
        tk.Button(filtro_frame, text="Nueva Baja", command=self.nueva_baja, bg="#ffa000", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#ff8f00").pack(side='left', padx=8)
        tabla_frame = tk.Frame(self, bg="#f7f7f7")
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="#fff", fieldbackground="#fff")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#fff3e0")
        columns = ("id", "producto_id", "motivo_baja", "cantidad_baja", "fecha_baja", "usuario", "valor_perdida")
        self.tabla = ttk.Treeview(tabla_frame, columns=columns, show='headings', style="Treeview")
        for col in columns:
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
            self.tabla.column(col, width=100)
        self.tabla.pack(fill='both', expand=True, padx=10, pady=10)
        self.lbl_status = ttk.Label(self, text="Bajas cargadas: 0")
        self.lbl_status.pack(anchor='w', padx=5, pady=2)

    def cargar_bajas(self):
        try:
            response = get("/withdrawals")
            if not response.success:
                raise Exception(response.message or "Error al obtener bajas")
            bajas = response.data or []
            filtro = self.filtro_var.get().lower()
            self.tabla.delete(*self.tabla.get_children())
            count = 0
            for baja in bajas:
                producto_id = baja.get("producto_id", "")
                motivo_baja = baja.get("motivo_baja", "")
                cantidad_baja = baja.get("cantidad_baja", "")
                fecha_baja = baja.get("fecha_baja", "")
                usuario = baja.get("usuario", "")
                valor_perdida = baja.get("valor_perdida", "")
                if filtro in str(producto_id).lower() or filtro in str(motivo_baja).lower():
                    self.tabla.insert('', 'end', values=(
                        baja.get("id"), producto_id, motivo_baja, cantidad_baja, fecha_baja, usuario, valor_perdida
                    ))
                    count += 1
            self.lbl_status.config(text=f"Bajas cargadas: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nueva_baja(self):
        messagebox.showinfo("Nueva Baja", "Funcionalidad para crear baja")
