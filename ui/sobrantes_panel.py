import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get, post
from ui.styles import COLORS, FONTS, SPACING, DIMENSIONS, BUTTON_STYLES, ENTRY_STYLES, LABEL_STYLES, FRAME_STYLES, TABLE_STYLES

class SobrantesPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_sobrantes()

    def create_widgets(self):
        self.configure(style='TFrame')
        
        # Header con color de éxito
        header = tk.Frame(self, bg=COLORS['success'])
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Sobrantes de Inventario", 
                font=FONTS['title_large'], 
                fg=COLORS['surface'], 
                bg=COLORS['success']).pack(anchor='center', pady=SPACING['lg'])
        
        # Frame de filtros
        filtro_frame = tk.Frame(self, bg=COLORS['background'])
        filtro_frame.pack(fill='x', pady=SPACING['md'])
        
        # Estilos para labels y entries
        label_style = {"font": FONTS['heading_small'], "fg": COLORS['primary'], "bg": COLORS['background']}
        entry_style = {"background": COLORS['surface'], "foreground": COLORS['text_primary'], 
                      "relief": "flat", "borderwidth": 1, "font": FONTS['body_medium']}
        
        tk.Label(filtro_frame, text="Buscar:", **label_style).pack(side='left')
        self.filtro_var = tk.StringVar()
        tk.Entry(filtro_frame, textvariable=self.filtro_var, **entry_style).pack(side='left', padx=SPACING['sm'])
        
        # Botones con estilos centralizados
        tk.Button(filtro_frame, text="Buscar", command=self.cargar_sobrantes, 
                 bg=COLORS['primary'], fg=COLORS['surface'], 
                 font=FONTS['button'], relief="flat", 
                 padx=SPACING['md'], pady=SPACING['sm'], 
                 activebackground=COLORS['primary_dark'],
                 cursor="hand2").pack(side='left', padx=SPACING['sm'])
        
        tk.Button(filtro_frame, text="Nuevo Sobrante", command=self.nuevo_sobrante, 
                 bg=COLORS['accent'], fg=COLORS['surface'], 
                 font=FONTS['button'], relief="flat", 
                 padx=SPACING['md'], pady=SPACING['sm'], 
                 activebackground=COLORS['accent_dark'],
                 cursor="hand2").pack(side='left', padx=SPACING['sm'])
        
        # Frame de tabla
        tabla_frame = tk.Frame(self, bg=COLORS['background'])
        tabla_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Configuración de estilos para Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                       font=FONTS['body_medium'], 
                       rowheight=DIMENSIONS['table_row_height'], 
                       background=COLORS['surface'], 
                       fieldbackground=COLORS['surface'])
        style.configure("Treeview.Heading", 
                       font=FONTS['heading_small'], 
                       background=COLORS['surface'], 
                       foreground=COLORS['primary'])
        
        columns = ("codigo_producto", "nombre_producto", "cantidad", "fecha_sobrante", "estado_envio")
        
        # Scrollbars
        vsb = tk.Scrollbar(tabla_frame, orient="vertical", command=lambda *args: self.tabla.yview(*args))
        hsb = tk.Scrollbar(tabla_frame, orient="horizontal", command=lambda *args: self.tabla.xview(*args))
        
        self.tabla = ttk.Treeview(tabla_frame, columns=columns, show='headings', 
                                 style="Treeview", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        for col in columns:
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize())
            self.tabla.column(col, width=120, anchor='center')
        
        self.tabla.grid(row=0, column=0, sticky='nsew', padx=SPACING['md'], pady=SPACING['md'])
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)
        
        self.lbl_status = ttk.Label(tabla_frame, text="Sobrantes cargados: 0")
        self.lbl_status.grid(row=2, column=0, sticky='w', padx=SPACING['sm'], pady=SPACING['xs'])

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
                productos = sobrante.get("productos", {})
                codigo_producto = productos.get("codigo_item", "")
                nombre_producto = productos.get("nombre_item", "")
                cantidad = sobrante.get("cantidad", "")
                fecha_sobrante = sobrante.get("fecha_sobrante", "")
                estado_envio = sobrante.get("estado_envio", "")
                if (filtro in nombre_producto.lower() or
                    filtro in str(codigo_producto).lower()):
                    self.tabla.insert('', 'end', values=(
                        codigo_producto, nombre_producto, cantidad, fecha_sobrante, estado_envio
                    ))
                    count += 1
            self.lbl_status.config(text=f"Sobrantes cargados: {count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nuevo_sobrante(self):
        try:
            resp = get("/products")
            if not resp.success:
                raise Exception(resp.message or "Error al obtener productos")
            productos_full = [p for p in (resp.data or []) if p.get("estado") != "baja"]
            if not productos_full:
                messagebox.showwarning("Sin productos", "No hay productos activos para registrar sobrante.")
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        
        top = tk.Toplevel(self)
        top.title("Registrar Sobrante de Inventario")
        top.configure(bg=COLORS['background'])
        
        frm = tk.Frame(top, bg=COLORS['background'])
        frm.pack(padx=SPACING['lg'], pady=SPACING['lg'], fill='both', expand=True)
        
        # Estilos para el formulario
        label_style = {"font": FONTS['heading_small'], "fg": COLORS['success'], "bg": COLORS['background']}
        entry_style = {"background": COLORS['surface'], "foreground": COLORS['text_primary'], 
                      "relief": "flat", "borderwidth": 1, "font": FONTS['body_medium']}
        
        tk.Label(frm, text="Registrar Sobrante de Inventario", 
                font=FONTS['title_medium'], 
                fg=COLORS['success'], 
                bg=COLORS['background']).grid(row=0, column=0, columnspan=2, pady=(0, SPACING['lg']))
        
        tk.Label(frm, text="Buscar producto:", **label_style).grid(row=1, column=0, sticky='e', padx=SPACING['sm'], pady=SPACING['sm'])
        
        filtro_var = tk.StringVar()
        producto_var = tk.StringVar()
        codigos_full = [f"{p.get('codigo_item','')} - {p.get('nombre_item','')}" for p in productos_full]
        productos_filtrados = productos_full.copy()
        codigos_filtrados = codigos_full.copy()
        
        producto_combo = ttk.Combobox(frm, textvariable=producto_var, values=codigos_filtrados, 
                                     state="readonly", font=FONTS['body_medium'], width=38)
        producto_combo.grid(row=2, column=1, padx=SPACING['sm'], pady=SPACING['sm'])
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
        filtro_entry.grid(row=1, column=1, padx=SPACING['sm'], pady=SPACING['sm'])
        filtro_var.trace_add('write', filtrar_productos)
        
        tk.Label(frm, text="Producto:", **label_style).grid(row=2, column=0, sticky='e', padx=SPACING['sm'], pady=SPACING['sm'])
        tk.Label(frm, text="Cantidad sobrante:", **label_style).grid(row=3, column=0, sticky='e', padx=SPACING['sm'], pady=SPACING['sm'])
        
        cantidad_var = tk.StringVar()
        cantidad_entry = tk.Entry(frm, textvariable=cantidad_var, width=38, **entry_style)
        cantidad_entry.grid(row=3, column=1, padx=SPACING['sm'], pady=SPACING['sm'])
        
        tk.Label(frm, text="Observaciones:", **label_style).grid(row=4, column=0, sticky='e', padx=SPACING['sm'], pady=SPACING['sm'])
        obs_var = tk.StringVar()
        obs_entry = tk.Entry(frm, textvariable=obs_var, width=38, **entry_style)
        obs_entry.grid(row=4, column=1, padx=SPACING['sm'], pady=SPACING['sm'])
        
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
                observaciones = obs_var.get()
                body = {
                    "producto_id": int(producto_id),
                    "cantidad": cantidad,
                    "observaciones": observaciones
                }
                resp = post("/surplus", body)
                if resp.success:
                    messagebox.showinfo("Éxito", "Sobrante registrado correctamente")
                    top.destroy()
                    self.cargar_sobrantes()
                else:
                    messagebox.showerror("Error", resp.message, parent=top)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=top)
        
        btn_frame = tk.Frame(frm, bg=COLORS['background'])
        btn_frame.grid(row=6, column=0, columnspan=2, pady=SPACING['lg'])
        
        # Botones con estilos centralizados
        tk.Button(btn_frame, text="Guardar", command=enviar, 
                 bg=COLORS['success'], fg=COLORS['surface'], 
                 font=FONTS['button'], relief="flat", 
                 padx=SPACING['md'], pady=SPACING['sm'], 
                 activebackground=COLORS['success_dark'],
                 cursor="hand2").pack(side='left', padx=SPACING['md'])
        
        tk.Button(btn_frame, text="Cancelar", command=top.destroy, 
                 bg=COLORS['danger'], fg=COLORS['surface'], 
                 font=FONTS['button'], relief="flat", 
                 padx=SPACING['md'], pady=SPACING['sm'], 
                 activebackground=COLORS['danger_dark'],
                 cursor="hand2").pack(side='left', padx=SPACING['md'])
