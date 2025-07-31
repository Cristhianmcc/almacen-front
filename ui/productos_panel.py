import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post, put, delete

class ProductosPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_productos()

    def create_widgets(self):
        # Encabezado profesional y responsivo
        header = tk.Frame(self, bg="#1976d2")
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Gestión de Productos", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#1976d2").pack(anchor='center', pady=18)
        # Leyenda visual elegante
        legend_frame = tk.Frame(self, bg="#f7f7f7")
        legend_frame.pack(fill='x', pady=(0, 10))
        leyendas = [
            ("#ff4d4d", "● Stock bajo"),
            ("#4caf50", "● Stock normal"),
            ("#ff9800", "● Próxima expiración")
        ]
        for color, texto in leyendas:
            lbl = tk.Label(legend_frame, text=texto, fg=color, bg="#f7f7f7", font=("Segoe UI", 12, "bold"))
            lbl.pack(side='left', padx=18, pady=6)
        # Barra de búsqueda y botones mejorada
        filtro_frame = tk.Frame(self, bg="#f7f7f7")
        filtro_frame.pack(fill='x', padx=0, pady=(0, 0))
        search_card = tk.Frame(filtro_frame, bg="#fff", highlightbackground="#e0e0e0", highlightthickness=1)
        search_card.pack(padx=24, pady=10, fill='x')
        search_card.configure(bd=0)
        label_style = {"font": ("Segoe UI", 12, "bold"), "fg": "#1976d2", "bg": "#fff"}
        entry_style = {"background": "#f3f6fb", "foreground": "#222", "relief": "flat", "borderwidth": 1, "font": ("Segoe UI", 12)}
        tk.Label(search_card, text="Buscar:", **label_style).pack(side='left', padx=(16, 6), pady=10)
        self.filtro_var = tk.StringVar()
        entry = tk.Entry(search_card, textvariable=self.filtro_var, **entry_style)
        entry.pack(side='left', padx=(0, 12), ipady=2, ipadx=2, pady=10, fill='x', expand=True)
        # Agrupar botones en un frame para mejor alineación
        btn_group = tk.Frame(search_card, bg="#fff")
        btn_group.pack(side='left', padx=(0, 0), pady=6)
        btn_style = {"font": ("Segoe UI", 11, "bold"), "fg": "#fff", "relief": "flat", "padx": 12, "pady": 4, "bd": 0, "activeforeground": "#fff"}
        botones = [
            ("Buscar", self.cargar_productos, "#1976d2", "#1565c0"),
            ("Cargar Datos", self.cargar_productos, "#43a047", "#388e3c"),
            ("Nuevo", self.nuevo_producto, "#1565c0", "#1976d2"),
            ("Editar", self.editar_producto, "#ffa000", "#ffb300"),
            ("Eliminar", self.eliminar_producto, "#d32f2f", "#b71c1c")
        ]
        for txt, cmd, color, active in botones:
            btn = tk.Button(btn_group, text=txt, command=cmd, bg=color, activebackground=active, **btn_style)
            btn.pack(side='left', padx=6, pady=2)
        # Tabla profesional y responsiva
        tabla_frame = tk.Frame(self, bg="#fff")
        tabla_frame.pack(fill='both', expand=True, padx=24, pady=(0, 18))
        columns = ("id", "codigo", "nombre", "marca", "orden", "medida", "precio", "subcuenta", "stock", "fecha_ingreso", "fecha_vencimiento", "estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columns, show='headings', style="Treeview")
        self.tabla.pack(fill='both', expand=True, padx=6, pady=6)
        self.lbl_status = tk.Label(tabla_frame, text="Productos cargados: 0", font=("Segoe UI", 12, "bold"), fg="#1976d2", bg="#fff")
        self.lbl_status.pack(anchor='w', padx=8, pady=(0, 8))
        style = ttk.Style()
        self.tabla_style_patch(style)
        # Configurar encabezados y columnas
        self.tabla.heading("id", text="ID")
        self.tabla.column("id", width=0, stretch=False)
        headers = [
            ("codigo", "Código"),
            ("nombre", "Nombre"),
            ("marca", "Marca"),
            ("orden", "Orden Compra"),
            ("medida", "Medida"),
            ("precio", "Precio"),
            ("subcuenta", "Subcuenta"),
            ("stock", "Stock"),
            ("fecha_ingreso", "F. Ingreso"),
            ("fecha_vencimiento", "F. Vencimiento"),
            ("estado", "Estado")
        ]
        for col, header in headers:
            self.tabla.heading(col, text=header)
            self.tabla.column(col, width=120, anchor='center')
        self.tabla.tag_configure('oddrow', background='#f3f6fb')
        self.tabla.tag_configure('evenrow', background='#e3f2fd')
        self.tabla.pack(fill='both', expand=True, padx=6, pady=6)
        self.lbl_status = tk.Label(tabla_frame, text="Productos cargados: 0", font=("Segoe UI", 12, "bold"), fg="#1976d2", bg="#fff")
        self.lbl_status.pack(anchor='w', padx=8, pady=(0, 8))
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
            # Configurar el tag para bajo stock
            self.tabla.tag_configure("bajo_stock", background="#ffcccc")
            for prod in productos:
                id_ = prod.get("id", "")
                codigo = prod.get("codigo_item", "")
                nombre = prod.get("nombre_item", "")
                marca = prod.get("nombre_marca", "")
                orden = prod.get("orden_compra", "")
                medida = prod.get("nombre_medida", "")
                precio = prod.get("mayor", "")
                subcuenta = prod.get("sub_cta", "")
                stock = prod.get("stock_actual", "")
                fecha_ingreso = prod.get("fecha_ingreso", "")
                fecha_vencimiento = prod.get("fecha_vencimiento", "")
                estado = prod.get("estado", "")
                # Filtro por nombre o código
                if estado != "baja" and (filtro in str(nombre).lower() or filtro in str(codigo).lower()):
                    tags = []
                    try:
                        if int(stock) <= low_stock_threshold:
                            tags.append("bajo_stock")
                    except Exception:
                        pass
                    self.tabla.insert('', 'end', values=(
                        id_, codigo, nombre, marca, orden, medida, precio, subcuenta, stock, fecha_ingreso, fecha_vencimiento, estado
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
            campos = [
                ("codigo_item", "Código"),
                ("nombre_item", "Nombre"),
                ("nombre_marca", "Marca"),
                ("orden_compra", "Orden Compra"),
                ("nombre_medida", "Medida"),
                ("mayor", "Precio"),
                ("sub_cta", "Subcuenta"),
                ("fecha_vencimiento", "Fecha vencimiento"),
                ("estado", "Estado")
            ]
        else:
            # Nuevo: pedir código y stock (ambos editables), no mostrar fecha_ingreso
            campos = [
                ("codigo_item", "Código"),
                ("nombre_item", "Nombre"),
                ("nombre_marca", "Marca"),
                ("orden_compra", "Orden Compra"),
                ("nombre_medida", "Medida"),
                ("mayor", "Precio"),
                ("sub_cta", "Subcuenta"),
                ("stock_actual", "Stock inicial"),
                ("fecha_vencimiento", "Fecha vencimiento"),
                ("estado", "Estado")
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
        # Opciones posibles para estado
        opciones_estado = ["activo", "inactivo", "baja", "pendiente", "agotado"]
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
            elif campo == "estado":
                ent = ttk.Combobox(top, values=opciones_estado, font=("Segoe UI", 13))
                try:
                    ent.configure(background="#ffffff", foreground="#111")
                except Exception:
                    pass
                ent.place(x=entry_x, y=30 + i*38, width=entry_w, height=30)
            else:
                ent = tk.Entry(top, **entry_style)
                ent.place(x=entry_x, y=30 + i*38, width=entry_w, height=30)
            if valores_dict and campo in valores_dict:
                if isinstance(ent, (tk.Entry, ttk.Combobox)):
                    ent.delete(0, 'end')
                if campo == "estado":
                    valor_estado = valores_dict[campo]
                    if valor_estado not in opciones_estado:
                        opciones_estado.append(valor_estado)
                        ent['values'] = opciones_estado
                    ent.set(valor_estado)
                else:
                    if isinstance(ent, (tk.Entry, ttk.Combobox)):
                        ent.insert(0, valores_dict[campo])
            entradas[campo] = ent
        def guardar():
            # Solo tomar los campos válidos y editables para la base de datos
            if valores:
                # Editar: no enviar codigo_item, stock_actual ni fecha_ingreso
                campos_db = ["nombre_item", "nombre_marca", "orden_compra", "nombre_medida", "mayor", "sub_cta", "fecha_vencimiento", "estado"]
            else:
                # Nuevo: enviar codigo_item, stock_actual y demás campos válidos
                campos_db = ["codigo_item", "nombre_item", "nombre_marca", "orden_compra", "nombre_medida", "mayor", "sub_cta", "stock_actual", "fecha_vencimiento", "estado"]
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
                    obligatorios = ["nombre_item", "mayor", "estado"]
                else:
                    obligatorios = ["codigo_item", "nombre_item", "mayor", "stock_actual", "estado"]
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
