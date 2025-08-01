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
        columns = ("codigo_producto", "nombre_producto", "motivo_baja", "cantidad_baja", "fecha_baja")
        # Scrollbars
        vsb = tk.Scrollbar(tabla_frame, orient="vertical", command=lambda *args: self.tabla.yview(*args))
        hsb = tk.Scrollbar(tabla_frame, orient="horizontal", command=lambda *args: self.tabla.xview(*args))
        self.tabla = ttk.Treeview(tabla_frame, columns=columns, show='headings', style="Treeview", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        for col in columns:
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
            self.tabla.column(col, width=120, anchor='center')
        self.tabla.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)
        self.lbl_status = ttk.Label(tabla_frame, text="Bajas cargadas: 0")
        self.lbl_status.grid(row=2, column=0, sticky='w', padx=5, pady=2)

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
                productos = baja.get("productos", {})
                codigo_producto = productos.get("codigo_item", "")
                nombre_producto = productos.get("nombre_item", "")
                motivo_baja = baja.get("motivo_baja", "")
                cantidad_baja = baja.get("cantidad_baja", "")
                fecha_baja = baja.get("fecha_baja", "")
                if (filtro in nombre_producto.lower() or
                    filtro in str(codigo_producto).lower() or
                    filtro in str(motivo_baja).lower()):
                    self.tabla.insert('', 'end', values=(
                        codigo_producto, nombre_producto, motivo_baja, cantidad_baja, fecha_baja
                    ))
                    count += 1
            self.lbl_status.config(text=f"Bajas cargadas: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nueva_baja(self):
        try:
            resp = get("/products")
            if not resp.success:
                raise Exception(resp.message or "Error al obtener productos")
            productos_full = [p for p in (resp.data or []) if p.get("estado") != "baja"]
            if not productos_full:
                messagebox.showwarning("Sin productos", "No hay productos activos para registrar baja.")
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        top = tk.Toplevel(self)
        top.title("Registrar Baja de Inventario")
        top.configure(bg="#f7f7f7")
        frm = tk.Frame(top, bg="#f7f7f7")
        frm.pack(padx=20, pady=20, fill='both', expand=True)
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#ff9800", "bg": "#f7f7f7"}
        entry_style = {"background": "#f3f6fb", "foreground": "#222", "relief": "flat", "borderwidth": 1, "font": ("Segoe UI", 12)}
        tk.Label(frm, text="Registrar Baja de Inventario", font=("Segoe UI", 18, "bold"), fg="#ff9800", bg="#f7f7f7").grid(row=0, column=0, columnspan=2, pady=(0,18))
        tk.Label(frm, text="Buscar producto:", **label_style).grid(row=1, column=0, sticky='e', padx=5, pady=7)
        filtro_var = tk.StringVar()
        producto_var = tk.StringVar()
        codigos_full = [f"{p.get('codigo_item','')} - {p.get('nombre_item','')}" for p in productos_full]
        productos_filtrados = productos_full.copy()
        codigos_filtrados = codigos_full.copy()
        producto_combo = ttk.Combobox(frm, textvariable=producto_var, values=codigos_filtrados, state="readonly", font=("Segoe UI", 11), width=38)
        producto_combo.grid(row=2, column=1, padx=5, pady=7)
        producto_combo.current(0)
        def filtrar_productos(*args):
            texto = filtro_var.get().lower()
            nonlocal productos_filtrados, codigos_filtrados
            productos_filtrados = [p for p in productos_full if texto in p.get('codigo_item','').lower() or texto in p.get('nombre_item','').lower()]
            codigos_filtrados = [f"{p.get('codigo_item','')} - {p.get('nombre_item','')}" for p in productos_filtrados]
            producto_combo['values'] = codigos_filtrados
            if codigos_filtrados:
                producto_combo.current(0)
            else:
                producto_combo.set("")
        filtro_entry = tk.Entry(frm, textvariable=filtro_var, width=38, **entry_style)
        filtro_entry.grid(row=1, column=1, padx=5, pady=7)
        filtro_var.trace_add('write', filtrar_productos)
        tk.Label(frm, text="Producto:", **label_style).grid(row=2, column=0, sticky='e', padx=5, pady=7)
        tk.Label(frm, text="Cantidad baja:", **label_style).grid(row=3, column=0, sticky='e', padx=5, pady=7)
        cantidad_var = tk.StringVar()
        cantidad_entry = tk.Entry(frm, textvariable=cantidad_var, width=38, **entry_style)
        cantidad_entry.grid(row=3, column=1, padx=5, pady=7)
        tk.Label(frm, text="Motivo baja:", **label_style).grid(row=4, column=0, sticky='e', padx=5, pady=7)
        motivo_var = tk.StringVar()
        motivo_entry = tk.Entry(frm, textvariable=motivo_var, width=38, **entry_style)
        motivo_entry.grid(row=4, column=1, padx=5, pady=7)
        tk.Label(frm, text="Observaciones:", **label_style).grid(row=5, column=0, sticky='e', padx=5, pady=7)
        obs_var = tk.StringVar()
        obs_entry = tk.Entry(frm, textvariable=obs_var, width=38, **entry_style)
        obs_entry.grid(row=5, column=1, padx=5, pady=7)
        def enviar():
            try:
                idx = producto_combo.current()
                if idx < 0 or not productos_filtrados:
                    raise ValueError("Selecciona un producto.")
                producto = productos_filtrados[idx]
                producto_id = producto.get("id")
                cantidad_baja = int(cantidad_var.get())
                if cantidad_baja <= 0:
                    raise ValueError("La cantidad debe ser mayor a cero.")
                motivo_baja = motivo_var.get()
                observaciones = obs_var.get()
                usuario = "admin"  # Cambia por el usuario real si aplica
                body = {
                    "producto_id": int(producto_id),
                    "cantidad_baja": cantidad_baja,
                    "motivo_baja": motivo_baja,
                    "usuario": usuario,
                    "observaciones": observaciones
                }
                resp = post("/withdrawals", body)
                if resp.success:
                    messagebox.showinfo("Éxito", "Baja registrada correctamente")
                    top.destroy()
                    self.cargar_bajas()
                else:
                    messagebox.showerror("Error", resp.message, parent=top)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=top)
        btn_frame = tk.Frame(frm, bg="#f7f7f7")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=18)
        tk.Button(btn_frame, text="Guardar", command=enviar, bg="#ff9800", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=6, activebackground="#fb8c00").pack(side='left', padx=10)
        tk.Button(btn_frame, text="Cancelar", command=top.destroy, bg="#d32f2f", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=6, activebackground="#b71c1c").pack(side='left', padx=10)
