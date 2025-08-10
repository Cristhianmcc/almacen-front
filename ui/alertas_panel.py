import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get
from ui.styles import COLORS, FONTS, BUTTON_STYLES, ENTRY_STYLES, LABEL_STYLES, FRAME_STYLES, TABLE_STYLES, SPACING, DIMENSIONS

class AlertasPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_alertas()

    def create_widgets(self):
        self.configure(style='TFrame')
        
        # Header con color de alerta usando la paleta
        header = tk.Frame(self, bg=COLORS['accent'])
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Alertas de Inventario", font=FONTS['title_medium'], fg=COLORS['surface'], bg=COLORS['accent']).pack(anchor='center', pady=SPACING['lg'])
        
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
            command=self.cargar_alertas, 
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
        
        btn_actualizar = tk.Button(
            filtro_frame, 
            text="Actualizar", 
            command=self.cargar_alertas, 
            bg=COLORS['success'], 
            fg=COLORS['surface'], 
            font=FONTS['button'], 
            relief="flat", 
            padx=12, 
            pady=4, 
            activebackground=COLORS['success_dark'],
            cursor="hand2"
        )
        btn_actualizar.pack(side='left', padx=8)
        
        # Frame de tabla
        tabla_frame = tk.Frame(self, bg=COLORS['background'])
        tabla_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Configuración de estilos de tabla
        style = ttk.Style()
        style.configure("Treeview", font=FONTS['body_medium'], rowheight=28, background=COLORS['surface'], fieldbackground=COLORS['surface'])
        style.configure("Treeview.Heading", font=FONTS['heading_small'], background=COLORS['accent_light'])
        
        columns = ("codigo_producto", "nombre_producto", "tipo_alerta", "descripcion", "fecha_alerta", "estado_alerta", "nivel_prioridad")
        
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
        self.lbl_status = ttk.Label(tabla_frame, text="Alertas cargadas: 0")
        self.lbl_status.grid(row=2, column=0, sticky='w', padx=5, pady=2)
        
        # Botón de detalle
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
                productos = alerta.get("productos", {})
                codigo_producto = productos.get("codigo_item", "")
                nombre_producto = productos.get("nombre_item", "")
                tipo_alerta = alerta.get("tipo_alerta", "")
                descripcion = alerta.get("descripcion", "")
                fecha_alerta = alerta.get("fecha_alerta", "")
                estado_alerta = alerta.get("estado_alerta", "")
                nivel_prioridad = alerta.get("nivel_prioridad", "")
                if (filtro in nombre_producto.lower() or
                    filtro in str(codigo_producto).lower() or
                    filtro in str(tipo_alerta).lower()):
                    self.tabla.insert('', 'end', values=(
                        codigo_producto, nombre_producto, tipo_alerta, descripcion, fecha_alerta, estado_alerta, nivel_prioridad
                    ))
                    count += 1
            self.lbl_status.config(text=f"Alertas cargadas: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_detalle(self):
        selected = self.tabla.focus()
        if not selected:
            messagebox.showwarning("Detalle", "Selecciona una alerta para ver el detalle.")
            return
        values = self.tabla.item(selected, 'values')
        if not values:
            messagebox.showwarning("Detalle", "No se pudo obtener la información de la alerta.")
            return
        detalle = (
            f"Código producto: {values[0]}\n"
            f"Nombre producto: {values[1]}\n"
            f"Tipo alerta: {values[2]}\n"
            f"Descripción: {values[3]}\n"
            f"Fecha alerta: {values[4]}\n"
            f"Estado alerta: {values[5]}\n"
            f"Nivel prioridad: {values[6]}"
        )
        messagebox.showinfo("Detalle de alerta", detalle)
