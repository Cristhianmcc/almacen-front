import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post
from ui.styles import COLORS, FONTS, BUTTON_STYLES, ENTRY_STYLES, LABEL_STYLES, FRAME_STYLES, TABLE_STYLES, SPACING, DIMENSIONS

class MovimientosPanel(ttk.Frame):
    def create_widgets(self):
        # Header verde con ícono usando la paleta de colores
        header = tk.Frame(self, bg=COLORS['success'])
        header.pack(fill='x', pady=(0, 0))
        header_inner = tk.Frame(header, bg=COLORS['success'])
        header_inner.pack(anchor='center', pady=SPACING['md'])
        tk.Label(header_inner, text="🔄", font=("Segoe UI Emoji", 32), fg=COLORS['surface'], bg=COLORS['success']).pack(side='left', padx=(0, 12))
        tk.Label(header_inner, text="Movimientos de Inventario", font=FONTS['title_medium'], fg=COLORS['surface'], bg=COLORS['success']).pack(side='left')

        # Barra de búsqueda y actualizar, centrada y moderna
        search_frame = tk.Frame(self, bg=COLORS['background'])
        search_frame.pack(pady=(SPACING['md'], SPACING['lg']))
        label_style = {"font": FONTS['heading_small'], "fg": COLORS['text_primary'], "bg": COLORS['background']}
        entry_style = {"background": COLORS['surface'], "foreground": COLORS['text_primary'], "relief": "solid", "borderwidth": 2, "font": FONTS['body_medium']}
        self.filtro_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        from tkcalendar import DateEntry
        import datetime
        hoy = datetime.date.today().strftime('%Y-%m-%d')
        self.fecha_var.set(hoy)
        tk.Label(search_frame, text="Buscar:", **label_style).pack(side='left', padx=(0, 5))
        tk.Entry(search_frame, textvariable=self.filtro_var, **entry_style, width=24).pack(side='left', padx=(0, 10))
        tk.Button(search_frame, text="Buscar", command=self.cargar_movimientos, bg=COLORS['success'], fg=COLORS['surface'], font=FONTS['button'], relief="flat", padx=16, pady=4, activebackground=COLORS['success_dark']).pack(side='left')
        tk.Label(search_frame, text="Filtrar por fecha:", **label_style).pack(side='left', padx=(10, 5))
        self.fecha_entry = DateEntry(search_frame, textvariable=self.fecha_var, date_pattern='yyyy-mm-dd', font=FONTS['body_medium'], width=12)
        self.fecha_entry.pack(side='left', padx=(0, 10))
        tk.Button(search_frame, text="Filtrar", command=self.cargar_movimientos, bg=COLORS['primary'], fg=COLORS['surface'], font=FONTS['button'], relief="flat", padx=16, pady=4, activebackground=COLORS['primary_dark']).pack(side='left')
      

        # Botones de registrar entrada/salida
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', pady=SPACING['md'])
        ttk.Button(btn_frame, text="Registrar Entrada", command=self.registrar_entrada).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Registrar Salida", command=self.registrar_salida).pack(side='left', padx=10)

        # Tabla de movimientos
        tabla_frame = tk.Frame(self, bg=COLORS['background'])
        tabla_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        style = ttk.Style()
        style.configure("Treeview", font=FONTS['body_medium'], rowheight=28, background=COLORS['surface'], fieldbackground=COLORS['surface'])
        style.configure("Treeview.Heading", font=FONTS['heading_small'], background=COLORS['background'])
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
        # Diseño visual mejorado usando la paleta de colores
        top = tk.Toplevel(self)
        top.title(f"Registrar {'Entrada' if tipo=='entrada' else 'Salida'} de Stock")
        top.configure(bg=COLORS['background'])
        frm = tk.Frame(top, bg=COLORS['background'])
        frm.pack(padx=SPACING['lg'], pady=SPACING['lg'], fill='both', expand=True)
        
        # Título del formulario
        titulo = tk.Label(
            frm, 
            text=f"Registrar {'Entrada' if tipo=='entrada' else 'Salida'} de Stock", 
            font=FONTS['title_small'], 
            fg=COLORS['primary'], 
            bg=COLORS['background']
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, SPACING['lg']))
        
        # Estilos para labels y entradas
        label_style = {"font": FONTS['heading_small'], "fg": COLORS['primary'], "bg": COLORS['background']}
        entry_style = {"background": COLORS['background'], "foreground": COLORS['text_primary'], "relief": "flat", "borderwidth": 1, "font": FONTS['body_medium']}
        
        # Campo de búsqueda
        tk.Label(frm, text="Buscar producto:", **label_style).grid(row=1, column=0, sticky='e', padx=5, pady=7)
        filtro_var = tk.StringVar()
        producto_var = tk.StringVar()
        codigos_full = [f"{p.get('codigo_item','')} - {p.get('nombre_item','')}" for p in productos_full]
        productos_filtrados = productos_full.copy()
        codigos_filtrados = codigos_full.copy()
        producto_combo = ttk.Combobox(frm, textvariable=producto_var, values=codigos_filtrados, state="readonly", font=FONTS['body_medium'], width=38)
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
        
        # Campo de producto
        tk.Label(frm, text="Producto:", **label_style).grid(row=2, column=0, sticky='e', padx=5, pady=7)
        
        # Campo de cantidad
        tk.Label(frm, text="Cantidad:", **label_style).grid(row=3, column=0, sticky='e', padx=5, pady=7)
        cantidad_var = tk.StringVar()
        cantidad_entry = tk.Entry(frm, textvariable=cantidad_var, width=38, **entry_style)
        cantidad_entry.grid(row=3, column=1, padx=5, pady=7)
        
        # Campo de observaciones
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
        
        # Frame de botones con estilos mejorados
        btn_frame = tk.Frame(frm, bg=COLORS['background'])
        btn_frame.grid(row=5, column=0, columnspan=2, pady=SPACING['lg'])
        
        # Botón Guardar
        btn_guardar = tk.Button(
            btn_frame, 
            text="Guardar", 
            command=enviar, 
            bg=COLORS['primary'], 
            fg=COLORS['surface'], 
            font=FONTS['button'], 
            relief="flat", 
            padx=16, 
            pady=6, 
            activebackground=COLORS['primary_dark'],
            cursor="hand2"
        )
        btn_guardar.pack(side='left', padx=10)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            btn_frame, 
            text="Cancelar", 
            command=top.destroy, 
            bg=COLORS['danger'], 
            fg=COLORS['surface'], 
            font=FONTS['button'], 
            relief="flat", 
            padx=16, 
            pady=6, 
            activebackground=COLORS['danger_dark'],
            cursor="hand2"
        )
        btn_cancelar.pack(side='left', padx=10)

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_movimientos()

    def cargar_movimientos(self):
        try:
            response = get("/movements")
            if not response.success:
                raise Exception(response.message or "Error al obtener movimientos")
            movimientos = response.data or []
            filtro = self.filtro_var.get().lower()
            fecha_filtrada = self.fecha_var.get()
            self.tabla.delete(*self.tabla.get_children())
            count = 0
            import datetime
            import tzlocal
            local_tz = tzlocal.get_localzone()
            for mov in movimientos:
                producto = mov.get("productos", {})
                codigo_producto = producto.get("codigo_item", "")
                nombre_producto = producto.get("nombre_item", "")
                tipo_movimiento = mov.get("tipo_movimiento", "")
                cantidad = mov.get("cantidad", "")
                fecha_movimiento = mov.get("fecha_movimiento", "")
                observaciones = mov.get("observaciones", "")
                # Convertir fecha_movimiento a local
                fecha_mov = None
                fecha_sel = None
                fecha_mov_local_str = fecha_movimiento
                try:
                    # Parse ISO y convertir a local
                    dt_utc = datetime.datetime.fromisoformat(str(fecha_movimiento).replace('Z', '+00:00'))
                    dt_local = dt_utc.astimezone(local_tz)
                    fecha_mov = dt_local.date()
                    fecha_mov_local_str = dt_local.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    try:
                        fecha_mov = datetime.datetime.strptime(str(fecha_movimiento)[:10], '%Y-%m-%d').date()
                        fecha_mov_local_str = str(fecha_movimiento)[:10]
                    except Exception:
                        fecha_mov = None
                try:
                    fecha_sel = datetime.datetime.strptime(fecha_filtrada, '%Y-%m-%d').date()
                except Exception:
                    fecha_sel = None
                if (fecha_mov and fecha_sel and fecha_mov == fecha_sel and (
                    filtro in nombre_producto.lower() or
                    filtro in codigo_producto.lower() or
                    filtro in str(tipo_movimiento).lower()
                )):
                    self.tabla.insert('', 'end', values=(
                        codigo_producto, nombre_producto, tipo_movimiento, cantidad, fecha_mov_local_str, observaciones
                    ))
                    count += 1
            self.lbl_status.config(text=f"Movimientos cargados: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nuevo_movimiento(self):
        messagebox.showinfo("Nuevo Movimiento", "Funcionalidad para crear movimiento")
