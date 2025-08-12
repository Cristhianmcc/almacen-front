import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post, put, delete

class ProductosPanel(ttk.Frame):
    # Paleta de colores profesional y moderna
    COLORS = {
        'primary': '#2563eb',      # Azul profesional principal
        'primary_dark': '#1d4ed8', # Azul oscuro para hover
        'secondary': '#64748b',    # Gris elegante secundario
        'secondary_dark': '#475569', # Gris oscuro para hover
        'success': '#059669',      # Verde suave para éxito
        'success_dark': '#047857', # Verde oscuro para hover
        'warning': '#d97706',      # Naranja cálido para advertencias
        'warning_dark': '#b45309', # Naranja oscuro para hover
        'danger': '#dc2626',       # Rojo profesional para peligro
        'danger_dark': '#b91c1c',  # Rojo oscuro para hover
        'background': '#f8fafc',   # Fondo muy claro y elegante
        'surface': '#ffffff',      # Superficies blancas
        'text_primary': '#1e293b', # Texto principal oscuro
        'text_secondary': '#64748b', # Texto secundario
        'border': '#e2e8f0',      # Bordes sutiles
        'accent': '#8b5cf6'       # Acento púrpura para elementos especiales
    }
    
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_productos()

    def create_widgets(self):
        # Encabezado profesional y responsivo con mejor diseño
        header = tk.Frame(self, bg=self.COLORS['primary'])
        header.pack(fill='x', pady=(0, 0))
        
        header_label = tk.Label(
            header, 
            text="Gestión de Productos", 
            font=("Segoe UI", 32, "bold"), 
            fg=self.COLORS['surface'], 
            bg=self.COLORS['primary']
        )
        header_label.pack(anchor='center', pady=24)
        
        # Leyenda visual elegante con mejor diseño
        legend_frame = tk.Frame(self, bg=self.COLORS['background'])
        legend_frame.pack(fill='x', pady=(0, 15))
        
        leyendas = [
            (self.COLORS['danger'], "● Stock bajo"),
            (self.COLORS['success'], "● Stock normal"),
            (self.COLORS['warning'], "● Próxima expiración"),
            (self.COLORS['accent'], "🎯 Fecha vencimiento dinámica (FEFO)")
        ]
        
        for color, texto in leyendas:
            lbl = tk.Label(
                legend_frame, 
                text=texto, 
                fg=color, 
                bg=self.COLORS['background'], 
                font=("Segoe UI", 13, "bold")
            )
            lbl.pack(side='left', padx=20, pady=8)
        
        # Barra de búsqueda y botones mejorada
        filtro_frame = tk.Frame(self, bg=self.COLORS['background'])
        filtro_frame.pack(fill='x', padx=0, pady=(0, 15))
        
        search_card = tk.Frame(
            filtro_frame, 
            bg=self.COLORS['surface'], 
            highlightbackground=self.COLORS['border'], 
            highlightthickness=1,
            relief="flat"
        )
        search_card.pack(padx=25, pady=12, fill='x')
        
        label_style = {
            "font": ("Segoe UI", 13, "bold"), 
            "fg": self.COLORS['primary'], 
            "bg": self.COLORS['surface']
        }
        
        entry_style = {
            "background": self.COLORS['background'], 
            "foreground": self.COLORS['text_primary'], 
            "relief": "flat", 
            "borderwidth": 1, 
            "font": ("Segoe UI", 12)
        }
        
        tk.Label(
            search_card, 
            text="Buscar:", 
            **label_style
        ).pack(side='left', padx=(18, 8), pady=12)
        
        self.filtro_var = tk.StringVar()
        entry = tk.Entry(
            search_card, 
            textvariable=self.filtro_var, 
            **entry_style
        )
        entry.pack(side='left', padx=(0, 15), ipady=4, ipadx=4, pady=12, fill='x', expand=True)
        
        # Agrupar botones en un frame para mejor alineación
        btn_group = tk.Frame(search_card, bg=self.COLORS['surface'])
        btn_group.pack(side='left', padx=(0, 0), pady=8)
        
        btn_style = {
            "font": ("Segoe UI", 12, "bold"), 
            "fg": self.COLORS['surface'], 
            "relief": "flat", 
            "padx": 16, 
            "pady": 6, 
            "bd": 0, 
            "activeforeground": self.COLORS['surface'],
            "cursor": "hand2"
        }
        
        botones = [
            ("Buscar", self.cargar_productos, self.COLORS['primary'], self.COLORS['primary_dark']),
            ("Cargar Datos", self.cargar_productos, self.COLORS['success'], self.COLORS['success_dark']),
            ("Nuevo", self.nuevo_producto, self.COLORS['primary_dark'], self.COLORS['primary']),
            ("Editar", self.editar_producto, self.COLORS['warning'], self.COLORS['warning_dark']),
            ("Eliminar", self.eliminar_producto, self.COLORS['danger'], self.COLORS['danger_dark'])
        ]
        
        for txt, cmd, color, active in botones:
            btn = tk.Button(
                btn_group, 
                text=txt, 
                command=cmd, 
                bg=color, 
                activebackground=active, 
                **btn_style
            )
            btn.pack(side='left', padx=8, pady=3)
        
        # Tabla profesional y responsiva con mejor diseño
        tabla_frame = tk.Frame(self, bg=self.COLORS['surface'])
        tabla_frame.pack(fill='both', expand=True, padx=25, pady=(0, 20))
        
        # Se comenta la columna 'estado' para futura visualización
        # columns = ("id", "codigo", "nombre", "marca", "orden", "medida", "precio", "subcuenta", "stock", "fecha_ingreso", "fecha_vencimiento", "estado")
        columns = ("id", "codigo", "nombre", "marca", "orden", "medida", "mayor", "subcuenta", "stock", "fecha_ingreso", "fecha_vencimiento")
        
        # Scrollbars con mejor diseño
        vsb = tk.Scrollbar(tabla_frame, orient="vertical", command=lambda *args: self.tabla.yview(*args))
        hsb = tk.Scrollbar(tabla_frame, orient="horizontal", command=lambda *args: self.tabla.xview(*args))
        
        self.tabla = ttk.Treeview(
            tabla_frame, 
            columns=columns, 
            show='headings', 
            style="Treeview", 
            yscrollcommand=vsb.set, 
            xscrollcommand=hsb.set,
            height=15
        )
        self.tabla.grid(row=0, column=0, sticky='nsew', padx=8, pady=8)
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)
        
        # Label de estado con mejor diseño
        self.lbl_status = tk.Label(
            tabla_frame, 
            text="Productos cargados: 0", 
            font=("Segoe UI", 13, "bold"), 
            fg=self.COLORS['primary'], 
            bg=self.COLORS['surface']
        )
        self.lbl_status.grid(row=2, column=0, sticky='w', padx=10, pady=(0, 10))
        
        style = ttk.Style()
        self.tabla_style_patch(style)
        
        # Configurar encabezados y columnas
        self.tabla.heading("id", text="ID")
        self.tabla.column("id", width=0, stretch=False)
        
        # Se comenta el header 'estado' y se cambia 'precio' por 'mayor'
        headers = [
            ("codigo", "Código"),
            ("nombre", "Nombre"),
            ("marca", "Marca"),
            ("orden", "Orden Compra"),
            ("medida", "Medida"),
            ("mayor", "Mayor"),
            ("subcuenta", "Subcuenta"),
            ("stock", "Stock"),
            ("fecha_ingreso", "F. Ingreso"),
            ("fecha_vencimiento", "F. Vencimiento")
            # ("estado", "Estado")  # Comentado para futura visualización
        ]
        
        for col, header in headers:
            self.tabla.heading(col, text=header)
            # Ancho adaptativo según el contenido
            width = max(120, len(header) * 10)
            self.tabla.column(col, width=width, anchor='center', minwidth=100)
        
        # Configurar estilos de filas alternadas con la nueva paleta
        self.tabla.tag_configure('oddrow', background=self.COLORS['background'])
        self.tabla.tag_configure('evenrow', background=self.COLORS['surface'])
        
        # Forzar color de encabezados en Windows (después de crear self.tabla)
        self.tabla_style_patch(style)

    def tabla_style_patch(self, style):
        # Refuerza el color de encabezado en Windows (Tkinter bug workaround)
        import platform
        if platform.system() == "Windows":
            style.layout("Treeview.Heading", [
                ('Treeheading.cell', {'sticky': 'nswe'}),
                ('Treeheading.border', {'sticky': 'nswe', 'children': [
                    ('Treeheading.padding', {'sticky': 'nswe', 'children': [
                        ('Treeheading.image', {'side': 'right', 'sticky': ''}),
                        ('Treeheading.text', {'sticky': 'we'})
                    ]})
                ]})
            ])
            style.configure("Treeview.Heading", background="#1976d2", foreground="#fff", font=("Segoe UI", 14, "bold"))

    def cargar_productos(self):
        try:
            response = get("/products")
            if not response.success:
                raise Exception(response.message or "Error al obtener productos")
            productos = response.data or []
            filtro = self.filtro_var.get().lower()
            self.tabla.delete(*self.tabla.get_children())
            count = 0
            low_stock_threshold = 10  # Puedes ajustar este valor si lo deseas
            
            # Importar el servicio FEFO
            from services.fefo_service import FEFOService
            
            # Configurar el tag para bajo stock
            self.tabla.tag_configure("bajo_stock", background="#ffcccc")
            
            for prod in productos:
                id_ = prod.get("id", "")
                codigo = prod.get("codigo_item", "")
                nombre = prod.get("nombre_item", "")
                marca = prod.get("nombre_marca", "")
                orden = prod.get("orden_compra", "")
                medida = prod.get("nombre_medida", "")
                mayor = prod.get("mayor", "")
                subcuenta = prod.get("sub_cta", "")
                stock = prod.get("stock_actual", "")
                fecha_ingreso = prod.get("fecha_ingreso", "")
                
                # Obtener fecha de vencimiento más próxima usando FEFO
                fecha_vencimiento = prod.get("fecha_vencimiento", "")
                try:
                    fecha_proxima = FEFOService.obtener_fecha_vencimiento_proxima(int(id_))
                    if fecha_proxima:
                        fecha_vencimiento = fecha_proxima
                        print(f"✅ Producto {nombre}: Fecha vencimiento actualizada a {fecha_proxima}")
                except Exception as e:
                    print(f"⚠️ No se pudo obtener fecha próxima para producto {id_}: {e}")
                
                # Filtro por nombre o código
                if prod.get("estado", "") != "baja" and (filtro in str(nombre).lower() or filtro in str(codigo).lower()):
                    tags = []
                    try:
                        if int(stock) <= low_stock_threshold:
                            tags.append("bajo_stock")
                    except Exception:
                        pass
                    self.tabla.insert('', 'end', values=(
                        id_, codigo, nombre, marca, orden, medida, mayor, subcuenta, stock, fecha_ingreso, fecha_vencimiento
                        # estado  # Comentado para futura visualización
                    ), tags=tags)
                    count += 1
            self.lbl_status.config(text=f"Productos cargados: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nuevo_producto(self):
        # Ejemplo simple: formulario emergente para crear producto
        self._abrir_formulario_producto("Nuevo Producto")

    def editar_producto(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Editar", "Selecciona un producto para editar.")
            return
        valores = self.tabla.item(item[0], "values")
        self._abrir_formulario_producto("Editar Producto", valores)

    def eliminar_producto(self):
        item = self.tabla.selection()
        if not item:
            messagebox.showwarning("Eliminar", "Selecciona un producto para eliminar.")
            return
        id_ = self.tabla.item(item[0], "values")[0]
        codigo = self.tabla.item(item[0], "values")[1]
        if messagebox.askyesno("Eliminar", f"¿Eliminar producto {codigo}?"):
            try:
                # Corregir ruta duplicada
                resp = delete(f"/products/{id_}")
                if resp.success:
                    messagebox.showinfo("Éxito", "Producto eliminado")
                    self.cargar_productos()
                else:
                    messagebox.showerror("Error", resp.message)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        # self.tabla = ttk.Treeview(tabla_frame, columns=columns, show='headings', style="Treeview")
    def _abrir_formulario_producto(self, titulo, valores=None):
        import re
        try:
            from tkcalendar import DateEntry
        except ImportError:
            DateEntry = None
        top = tk.Toplevel(self)
        top.title(titulo)
        top.configure(bg="#fff")
        top.resizable(False, False)
        # Centrar ventana siempre que se abra
        w, h = 540, 480
        top.geometry(f"{w}x{h}+0+0")
        top.update_idletasks()
        x = top.winfo_screenwidth() // 2 - w // 2
        y = top.winfo_screenheight() // 2 - h // 2
        top.geometry(f"{w}x{h}+{x}+{y}")
        # Solo mostrar campos editables y válidos para el backend
        if valores:
            # Editar: mostrar código solo como label (no editable), no mostrar stock ni fecha_ingreso
            # Se comenta el campo 'estado' para futura visualización
            campos = [
                ("codigo_item", "Código"),
                ("nombre_item", "Nombre"),
                ("nombre_marca", "Marca"),
                ("orden_compra", "Orden Compra"),
                ("nombre_medida", "Medida"),
                ("mayor", "Mayor"),
                ("sub_cta", "Subcuenta"),
                ("fecha_vencimiento", "Fecha vencimiento")
                # ("estado", "Estado")  # Comentado para futura visualización
            ]
        else:
            # Nuevo: pedir código y stock (ambos editables), no mostrar fecha_ingreso
            # Se comenta el campo 'estado' para futura visualización
            campos = [
                ("codigo_item", "Código"),
                ("nombre_item", "Nombre"),
                ("nombre_marca", "Marca"),
                ("orden_compra", "Orden Compra"),
                ("nombre_medida", "Medida"),
                ("mayor", "Mayor"),
                ("sub_cta", "Subcuenta"),
                ("stock_actual", "Stock inicial"),
                ("fecha_vencimiento", "Fecha vencimiento")
                # ("estado", "Estado")  # Comentado para futura visualización
            ]
        # El id nunca se muestra ni edita en el formulario
        entradas = {}
        # Si valores es una tupla, convertir a dict usando los nombres de columnas de la tabla
        valores_dict = None
        if valores:
            # Mapeo: columnas de la tabla -> campos del formulario
            columnas_tabla = [
                "id", "codigo", "nombre", "marca", "orden", "medida", "precio", "subcuenta", "stock", "fecha_ingreso", "fecha_vencimiento", "estado"
            ]
            # Mapeo a los nombres reales de la base de datos
            map_to_db = {
                "codigo": "codigo_item",
                "nombre": "nombre_item",
                "marca": "nombre_marca",
                "orden": "orden_compra",
                "medida": "nombre_medida",
                "precio": "mayor",
                "subcuenta": "sub_cta",
                "stock": "stock_actual",
                "fecha_ingreso": "fecha_ingreso",
                "fecha_vencimiento": "fecha_vencimiento",
                "estado": "estado"
            }
            valores_dict = {}
            for i, col in enumerate(columnas_tabla):
                if i < len(valores):
                    db_col = map_to_db.get(col, col)
                    valores_dict[db_col] = valores[i]
            id_interno = valores[0] if len(valores) > 0 else None
        else:
            id_interno = None
    # opciones_estado = ["activo", "inactivo", "baja", "pendiente", "agotado"]  # Comentado para futura visualización
        entry_style = {"background": "#ffffff", "foreground": "#111", "relief": "groove", "borderwidth": 2, "font": ("Segoe UI", 13), "insertbackground": "#111", "highlightthickness": 1, "highlightbackground": "#888", "highlightcolor": "#1976d2"}
        label_style = {"font": ("Segoe UI", 13, "bold"), "foreground": "#222", "bg": "#fff"}
        entry_padx = 10
        entry_pady = 10
        for i, (campo, label) in enumerate(campos):
            tk.Label(top, text=label+":", **label_style).place(x=30, y=30 + i*38, width=160, height=30)
            entry_x = 200
            entry_w = 320
            if campo == "codigo_item":
                if valores:
                    # Editar: solo mostrar como label
                    ent = tk.Label(top, text=valores_dict[campo] if valores_dict and campo in valores_dict else "", font=("Segoe UI", 13), bg="#fff", fg="#222", anchor="w")
                    ent.place(x=entry_x, y=30 + i*38, width=entry_w, height=30)
                    entradas[campo] = ent
                    continue
                else:
                    ent = tk.Entry(top, **entry_style)
                    ent.place(x=entry_x, y=30 + i*38, width=entry_w, height=30)
                    ent.insert(0, "")
            elif campo == "fecha_vencimiento" and DateEntry:
                ent = DateEntry(top, date_pattern='yyyy-mm-dd')
                ent.configure(background="#ffffff", foreground="#111", borderwidth=2)
                ent.place(x=entry_x, y=30 + i*38, width=entry_w, height=30)
            else:
                ent = tk.Entry(top, **entry_style)
                ent.place(x=entry_x, y=30 + i*38, width=entry_w, height=30)
            if valores_dict and campo in valores_dict:
                if isinstance(ent, (tk.Entry, ttk.Combobox)):
                    ent.delete(0, 'end')
                if isinstance(ent, (tk.Entry, ttk.Combobox)):
                    ent.insert(0, valores_dict[campo])
            entradas[campo] = ent
        def guardar():
            # Solo tomar los campos válidos y editables para la base de datos
            if valores:
                # Editar: no enviar codigo_item, stock_actual ni fecha_ingreso
                # Se comenta 'estado' para futura visualización
                campos_db = ["nombre_item", "nombre_marca", "orden_compra", "nombre_medida", "mayor", "sub_cta", "fecha_vencimiento"]
                # "estado"  # Comentado para futura visualización
            else:
                # Nuevo: enviar codigo_item, stock_actual y demás campos válidos
                # Se comenta 'estado' para futura visualización
                campos_db = ["codigo_item", "nombre_item", "nombre_marca", "orden_compra", "nombre_medida", "mayor", "sub_cta", "stock_actual", "fecha_vencimiento"]
                # "estado"  # Comentado para futura visualización
            datos = {}
            for k in campos_db:
                widget = entradas.get(k)
                if widget:
                    if isinstance(widget, (tk.Entry, ttk.Entry)):
                        datos[k] = widget.get()
                    elif isinstance(widget, ttk.Combobox):
                        datos[k] = widget.get()
            # Validación y conversión de tipos
            try:
                if valores:
                    obligatorios = ["nombre_item", "mayor"]
                    # "estado"  # Comentado para futura visualización
                else:
                    obligatorios = ["codigo_item", "nombre_item", "mayor", "stock_actual"]
                    # "estado"  # Comentado para futura visualización
                for campo in obligatorios:
                    if not datos.get(campo) or not str(datos.get(campo)).strip():
                        raise ValueError(f"El campo '{campo}' es obligatorio.")
                # Validar que el código y stock no sean solo espacios ni vacíos
                if not valores:
                    codigo = datos.get("codigo_item", "").strip()
                    if not codigo:
                        raise ValueError("El campo 'Código' es obligatorio.")
                    datos["codigo_item"] = codigo
                    try:
                        datos["stock_actual"] = int(datos["stock_actual"])
                        if datos["stock_actual"] < 0:
                            raise ValueError("El stock inicial debe ser 0 o mayor.")
                    except Exception:
                        raise ValueError("El campo 'Stock inicial' debe ser un número entero válido.")
                datos["mayor"] = float(datos["mayor"])
                if datos.get("fecha_vencimiento"):
                    f = datos["fecha_vencimiento"]
                    if re.match(r"\d{2}/\d{2}/\d{4}", f):
                        d, m, y = f.split("/")
                        datos["fecha_vencimiento"] = f"{y}-{m}-{d}"
                    elif re.match(r"\d{4}-\d{2}-\d{2}", f):
                        pass
                    else:
                        raise ValueError("Fecha vencimiento debe ser YYYY-MM-DD o DD/MM/YYYY")
                else:
                    datos.pop("fecha_vencimiento", None)
                datos = {k: v for k, v in datos.items() if v != ""}
                if "Nuevo" in titulo:
                    resp = post("/products", datos)
                else:
                    if id_interno:
                        resp = put(f"/products/{id_interno}", datos)
                    else:
                        raise Exception("No se encontró el ID interno del producto para editar.")
                if resp.success:
                    messagebox.showinfo("Éxito", "Producto guardado")
                    top.destroy()
                    self.cargar_productos()
                else:
                    messagebox.showerror("Error", resp.message)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        btn_guardar = tk.Button(top, text="Guardar", command=guardar, bg="#1976d2", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=6, activebackground="#1565c0")
        btn_guardar.place(x=130, y=30 + len(campos)*38 + 10, width=130, height=38)
        btn_cancelar = tk.Button(top, text="Cancelar", command=top.destroy, bg="#d32f2f", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=6, activebackground="#b71c1c")
        btn_cancelar.place(x=290, y=30 + len(campos)*38 + 10, width=130, height=38)
