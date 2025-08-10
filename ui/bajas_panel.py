import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post
from ui.styles import COLORS, FONTS, BUTTON_STYLES, ENTRY_STYLES, LABEL_STYLES, FRAME_STYLES, TABLE_STYLES, SPACING, DIMENSIONS

class BajasPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_bajas()

    def create_widgets(self):
        self.configure(style='TFrame')
        
        # Header con color de advertencia usando la paleta
        header = tk.Frame(self, bg=COLORS['warning'])
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Bajas de Inventario", font=FONTS['title_medium'], fg=COLORS['surface'], bg=COLORS['warning']).pack(anchor='center', pady=SPACING['lg'])
        
        # Frame de filtros
        filtro_frame = tk.Frame(self, bg=COLORS['background'])
        filtro_frame.pack(fill='x', pady=SPACING['md'])
        label_style = {"font": FONTS['heading_small'], "fg": COLORS['primary'], "bg": COLORS['background']}
        entry_style = {"background": COLORS['background'], "foreground": COLORS['text_primary'], "relief": "flat", "borderwidth": 1, "font": FONTS['body_medium']}
        
        tk.Label(filtro_frame, text="Buscar:", **label_style).pack(side='left')
        self.filtro_var = tk.StringVar()
        tk.Entry(filtro_frame, textvariable=self.filtro_var, **entry_style).pack(side='left', padx=5)
        
        # Botones con estilos mejorados
        btn_buscar = tk.Button(
            filtro_frame, 
            text="Buscar", 
            command=self.cargar_bajas, 
            bg=COLORS['primary'], 
            fg=COLORS['surface'], 
            font=FONTS['button'], 
            relief="flat", 
            padx=12, 
            pady=4, 
            activebackground=COLORS['primary_dark'],
            cursor="hand2"
        )
        btn_buscar.pack(side='left', padx=8)
        
        btn_nueva_baja = tk.Button(
            filtro_frame, 
            text="Nueva Baja", 
            command=self.nueva_baja, 
            bg=COLORS['warning'], 
            fg=COLORS['surface'], 
            font=FONTS['button'], 
            relief="flat", 
            padx=12, 
            pady=4, 
            activebackground=COLORS['warning_dark'],
            cursor="hand2"
        )
        btn_nueva_baja.pack(side='left', padx=8)
        
        # Frame de tabla
        tabla_frame = tk.Frame(self, bg=COLORS['background'])
        tabla_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Configuración de estilos de tabla
        style = ttk.Style()
        style.configure("Treeview", font=FONTS['body_medium'], rowheight=28, background=COLORS['surface'], fieldbackground=COLORS['surface'])
        style.configure("Treeview.Heading", font=FONTS['heading_small'], background=COLORS['warning_light'])
        
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
        
        # Label de estado
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
        
        # Ventana de formulario con estilos mejorados
        top = tk.Toplevel(self)
        top.title("Registrar Baja de Inventario")
        top.configure(bg=COLORS['background'])
        frm = tk.Frame(top, bg=COLORS['background'])
        frm.pack(padx=SPACING['lg'], pady=SPACING['lg'], fill='both', expand=True)
        
        # Título del formulario
        titulo = tk.Label(
            frm, 
            text="Registrar Baja de Inventario", 
            font=FONTS['title_small'], 
            fg=COLORS['warning'], 
            bg=COLORS['background']
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, SPACING['lg']))
        
        # Estilos para labels y entradas
        label_style = {"font": FONTS['heading_small'], "fg": COLORS['warning'], "bg": COLORS['background']}
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
        tk.Label(frm, text="Cantidad baja:", **label_style).grid(row=3, column=0, sticky='e', padx=5, pady=7)
        cantidad_var = tk.StringVar()
        cantidad_entry = tk.Entry(frm, textvariable=cantidad_var, width=38, **entry_style)
        cantidad_entry.grid(row=3, column=1, padx=5, pady=7)
        
        # Campo de motivo
        tk.Label(frm, text="Motivo baja:", **label_style).grid(row=4, column=0, sticky='e', padx=5, pady=7)
        motivo_var = tk.StringVar()
        motivo_entry = tk.Entry(frm, textvariable=motivo_var, width=38, **entry_style)
        motivo_entry.grid(row=4, column=1, padx=5, pady=7)
        
        # Campo de observaciones
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
        
        # Frame de botones con estilos mejorados
        btn_frame = tk.Frame(frm, bg=COLORS['background'])
        btn_frame.grid(row=6, column=0, columnspan=2, pady=SPACING['lg'])
        
        # Botón Guardar
        btn_guardar = tk.Button(
            btn_frame, 
            text="Guardar", 
            command=enviar, 
            bg=COLORS['warning'], 
            fg=COLORS['surface'], 
            font=FONTS['button'], 
            relief="flat", 
            padx=16, 
            pady=6, 
            activebackground=COLORS['warning_dark'],
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
