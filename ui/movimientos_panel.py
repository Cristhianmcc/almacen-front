import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post

class MovimientosPanel(ttk.Frame):
    def create_widgets(self):
        # Header verde con ícono
        header = tk.Frame(self, bg="#43a047")
        header.pack(fill='x', pady=(0, 0))
        header_inner = tk.Frame(header, bg="#43a047")
        header_inner.pack(anchor='center', pady=10)
        tk.Label(header_inner, text="🔄", font=("Segoe UI Emoji", 32), fg="#fff", bg="#43a047").pack(side='left', padx=(0, 12))
        tk.Label(header_inner, text="Movimientos de Inventario", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#43a047").pack(side='left')
        # Barra de búsqueda y actualizar, centrada y moderna
        search_frame = tk.Frame(self, bg="#f7f7f7")
        search_frame.pack(pady=(10, 18))
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#333", "bg": "#f7f7f7"}
        entry_style = {"background": "#fff", "foreground": "#222", "relief": "solid", "borderwidth": 2, "font": ("Segoe UI", 12)}
        self.filtro_var = tk.StringVar()
        tk.Label(search_frame, text="Buscar:", **label_style).pack(side='left', padx=(0, 5))
        tk.Entry(search_frame, textvariable=self.filtro_var, **entry_style, width=24).pack(side='left', padx=(0, 10))
        tk.Button(search_frame, text="Buscar", command=self.cargar_movimientos, bg="#43a047", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=4, activebackground="#388e3c").pack(side='left')
        # Botones de registrar entrada/salida
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Registrar Entrada", command=self.registrar_entrada).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Registrar Salida", command=self.registrar_salida).pack(side='left', padx=10)
        # Tabla de movimientos
        tabla_frame = tk.Frame(self, bg="#f7f7f7")
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="#fff", fieldbackground="#fff")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#e3f2fd")
        # Columnas ocultas: id, usuario, motivo, destino
        # self.tabla = ttk.Treeview(tabla_frame, columns=("id", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "usuario", "observaciones", "motivo", "destino"), show='headings', style="Treeview")
        # for col in ("id", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "usuario", "observaciones", "motivo", "destino"):
        #     self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
        self.tabla = ttk.Treeview(tabla_frame, columns=("codigo_producto", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "observaciones"), show='headings', style="Treeview")
        for col in ("codigo_producto", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "observaciones"):
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
            self.tabla.column(col, anchor='center')
        self.tabla.pack(fill='both', expand=True, padx=10, pady=10)
        self.lbl_status = ttk.Label(self, text="Movimientos cargados: 0")
        self.lbl_status.pack(anchor='w', padx=5, pady=2)

    def registrar_entrada(self):
        self._abrir_formulario_movimiento('entrada')

    def registrar_salida(self):
        self._abrir_formulario_movimiento('salida')

    def _abrir_formulario_movimiento(self, tipo):
        # Obtener productos activos
        try:
            resp = get("/products")
            if not resp.success:
                raise Exception(resp.message or "Error al obtener productos")
            productos_full = [p for p in (resp.data or []) if p.get("estado") != "baja"]
            if not productos_full:
                messagebox.showwarning("Sin productos", "No hay productos activos para registrar movimiento.")
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        # Diseño visual mejorado
        top = tk.Toplevel(self)
        top.title(f"Registrar {'Entrada' if tipo=='entrada' else 'Salida'} de Stock")
        top.configure(bg="#f7f7f7")
        frm = tk.Frame(top, bg="#f7f7f7")
        frm.pack(padx=20, pady=20, fill='both', expand=True)
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#1976d2", "bg": "#f7f7f7"}
        entry_style = {"background": "#f3f6fb", "foreground": "#222", "relief": "flat", "borderwidth": 1, "font": ("Segoe UI", 12)}
        tk.Label(frm, text=f"Registrar {'Entrada' if tipo=='entrada' else 'Salida'} de Stock", font=("Segoe UI", 18, "bold"), fg="#1976d2", bg="#f7f7f7").grid(row=0, column=0, columnspan=2, pady=(0,18))
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
        tk.Label(frm, text="Cantidad:", **label_style).grid(row=3, column=0, sticky='e', padx=5, pady=7)
        cantidad_var = tk.StringVar()
        cantidad_entry = tk.Entry(frm, textvariable=cantidad_var, width=38, **entry_style)
        cantidad_entry.grid(row=3, column=1, padx=5, pady=7)
        tk.Label(frm, text="Observaciones:", **label_style).grid(row=4, column=0, sticky='e', padx=5, pady=7)
        obs_var = tk.StringVar()
        obs_entry = tk.Entry(frm, textvariable=obs_var, width=38, **entry_style)
        obs_entry.grid(row=4, column=1, padx=5, pady=7)
        def enviar():
            try:
                idx = producto_combo.current()
                if idx < 0 or not productos_filtrados:
                    raise ValueError("Selecciona un producto.")
                producto = productos_filtrados[idx]
                producto_id = producto.get("id")
                cantidad = int(cantidad_var.get())
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a cero.")
                # Validación de stock para salida
                if tipo == 'salida':
                    stock_actual = producto.get("stock_actual", 0)
                    if cantidad > stock_actual:
                        top.lift()  # Traer el formulario al frente
                        top.attributes('-topmost', True)
                        top.after(100, lambda: top.attributes('-topmost', False))
                        messagebox.showwarning(
                            "Stock insuficiente",
                            f"No se puede registrar la salida.\n\nCantidad solicitada: {cantidad}\nStock disponible: {stock_actual}\n\nPor favor, ingresa una cantidad válida.",
                            parent=top
                        )
                        cantidad_entry.focus_set()
                        cantidad_var.set("")
                        return
                usuario = "admin"  # Cambia por el usuario real si aplica
                body = {
                    "producto_id": int(producto_id),
                    "cantidad": cantidad,
                    "usuario": usuario,
                    "observaciones": obs_var.get()
                }
                if tipo == 'entrada':
                    resp = post("/movements/entry", body)
                else:
                    resp = post("/movements/exit", body)
                if resp.success:
                    messagebox.showinfo("Éxito", f"{('Entrada' if tipo=='entrada' else 'Salida')} registrada correctamente")
                    top.destroy()
                    self.cargar_movimientos()
                else:
                    messagebox.showerror("Error", resp.message, parent=top)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=top)
        btn_frame = tk.Frame(frm, bg="#f7f7f7")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=18)
        tk.Button(btn_frame, text="Guardar", command=enviar, bg="#1976d2", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=6, activebackground="#1565c0").pack(side='left', padx=10)
        tk.Button(btn_frame, text="Cancelar", command=top.destroy, bg="#d32f2f", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=6, activebackground="#b71c1c").pack(side='left', padx=10)
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_movimientos()

    def create_widgets(self):
        # Header azul
        header = tk.Frame(self, bg="#1976d2")
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Movimientos de Inventario", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#1976d2").pack(anchor='center', pady=18)

        # Barra de búsqueda y actualizar, centrada y moderna
        search_frame = tk.Frame(self, bg="#f7f7f7")
        search_frame.pack(pady=(10, 18))
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#333", "bg": "#f7f7f7"}
        entry_style = {"background": "#fff", "foreground": "#222", "relief": "solid", "borderwidth": 2, "font": ("Segoe UI", 12)}
        self.filtro_var = tk.StringVar()
        tk.Label(search_frame, text="Buscar:", **label_style).pack(side='left', padx=(0, 5))
        tk.Entry(search_frame, textvariable=self.filtro_var, **entry_style, width=24).pack(side='left', padx=(0, 10))
        tk.Button(search_frame, text="Buscar", command=self.cargar_movimientos, bg="#43a047", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=4, activebackground="#388e3c").pack(side='left')

        # Botones de registrar entrada/salida
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Registrar Entrada", command=self.registrar_entrada).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Registrar Salida", command=self.registrar_salida).pack(side='left', padx=10)

        # Tabla de movimientos
        tabla_frame = tk.Frame(self, bg="#f7f7f7")
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="#fff", fieldbackground="#fff")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#e3f2fd")
        # Columnas ocultas: id, usuario, motivo, destino
        # self.tabla = ttk.Treeview(tabla_frame, columns=("id", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "usuario", "observaciones", "motivo", "destino"), show='headings', style="Treeview")
        # for col in ("id", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "usuario", "observaciones", "motivo", "destino"):
        #     self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
        # Scrollbars
        vsb = tk.Scrollbar(tabla_frame, orient="vertical", command=lambda *args: self.tabla.yview(*args))
        hsb = tk.Scrollbar(tabla_frame, orient="horizontal", command=lambda *args: self.tabla.xview(*args))
        self.tabla = ttk.Treeview(tabla_frame, columns=("codigo_producto", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "observaciones"), show='headings', style="Treeview", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        for col in ("codigo_producto", "nombre_producto", "tipo_movimiento", "cantidad", "fecha_movimiento", "observaciones"):
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
            self.tabla.column(col, anchor='center')
        self.tabla.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)
        self.lbl_status = ttk.Label(tabla_frame, text="Movimientos cargados: 0")
        self.lbl_status.grid(row=2, column=0, sticky='w', padx=5, pady=2)


    def cargar_movimientos(self):
        try:
            response = get("/movements")
            if not response.success:
                raise Exception(response.message or "Error al obtener movimientos")
            movimientos = response.data or []
            filtro = self.filtro_var.get().lower()
            self.tabla.delete(*self.tabla.get_children())
            count = 0
            for mov in movimientos:
                producto = mov.get("productos", {})
                codigo_producto = producto.get("codigo_item", "")
                nombre_producto = producto.get("nombre_item", "")
                tipo_movimiento = mov.get("tipo_movimiento", "")
                cantidad = mov.get("cantidad", "")
                fecha_movimiento = mov.get("fecha_movimiento", "")
                # usuario = mov.get("usuario", "")  # Oculto
                observaciones = mov.get("observaciones", "")
                # motivo = mov.get("motivo", "")    # Oculto
                # destino = mov.get("destino", "")   # Oculto
                # Búsqueda por nombre de producto, código o tipo de movimiento
                if (filtro in nombre_producto.lower() or
                    filtro in codigo_producto.lower() or
                    filtro in str(tipo_movimiento).lower()):
                    self.tabla.insert('', 'end', values=(
                        codigo_producto, nombre_producto, tipo_movimiento, cantidad, fecha_movimiento, observaciones
                    ))
                    count += 1
            self.lbl_status.config(text=f"Movimientos cargados: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nuevo_movimiento(self):
        messagebox.showinfo("Nuevo Movimiento", "Funcionalidad para crear movimiento")
