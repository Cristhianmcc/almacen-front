"""
Panel para visualizar y gestionar lotes FEFO
Muestra información detallada de fechas de vencimiento y stock por lote
"""

import tkinter as tk
from tkinter import ttk, messagebox
from services.fefo_service import FEFOService
from ui.styles import COLORS, FONTS, BUTTON_STYLES, ENTRY_STYLES, LABEL_STYLES, FRAME_STYLES, TABLE_STYLES, SPACING, DIMENSIONS
import datetime

class LotesPanel(ttk.Frame):
    """Panel para gestión de lotes FEFO"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_lotes()
    
    def create_widgets(self):
        """Crea todos los widgets del panel"""
        # Header principal con ícono y título
        header = tk.Frame(self, bg=COLORS['accent'])
        header.pack(fill='x', pady=(0, 0))
        header_inner = tk.Frame(header, bg=COLORS['accent'])
        header_inner.pack(anchor='center', pady=SPACING['md'])
        tk.Label(header_inner, text="📦", font=("Segoe UI Emoji", 32), fg=COLORS['surface'], bg=COLORS['accent']).pack(side='left', padx=(0, 12))
        tk.Label(header_inner, text="Gestión de Lotes FEFO", font=FONTS['title_medium'], fg=COLORS['surface'], bg=COLORS['accent']).pack(side='left')
        
        # Barra de herramientas
        toolbar = tk.Frame(self, bg=COLORS['background'])
        toolbar.pack(fill='x', pady=SPACING['md'], padx=SPACING['lg'])
        
        # Botón para refrescar lotes
        btn_refrescar = tk.Button(
            toolbar,
            text="🔄 Refrescar Lotes",
            command=self.cargar_lotes,
            bg=COLORS['primary'],
            fg=COLORS['surface'],
            font=FONTS['button'],
            relief='flat',
            padx=16,
            pady=8,
            activebackground=COLORS['primary_dark'],
            cursor='hand2'
        )
        btn_refrescar.pack(side='left', padx=(0, 10))
        
        # Botón para simular salida FEFO
        btn_simular = tk.Button(
            toolbar,
            text="🧮 Simular Salida FEFO",
            command=self.simular_salida_fefo,
            bg=COLORS['warning'],
            fg=COLORS['surface'],
            font=FONTS['button'],
            relief='flat',
            padx=16,
            pady=8,
            activebackground=COLORS['warning_dark'],
            cursor='hand2'
        )
        btn_simular.pack(side='left', padx=(0, 10))
        
        # Botón para ver historial
        btn_historial = tk.Button(
            toolbar,
            text="📊 Historial de Lotes",
            command=self.mostrar_historial,
            bg=COLORS['secondary'],
            fg=COLORS['surface'],
            font=FONTS['button'],
            relief='flat',
            padx=16,
            pady=8,
            activebackground=COLORS['secondary_dark'],
            cursor='hand2'
        )
        btn_historial.pack(side='left', padx=(0, 10))
        
        # Información de estado
        self.lbl_status = tk.Label(
            toolbar,
            text="Lotes cargados: 0",
            font=FONTS['body_medium'],
            fg=COLORS['text_secondary'],
            bg=COLORS['background']
        )
        self.lbl_status.pack(side='right', padx=10)
        
        # Información adicional sobre FEFO
        info_frame = tk.Frame(toolbar, bg=COLORS['background'])
        info_frame.pack(side='right', padx=10)
        
        tk.Label(
            info_frame,
            text="🎯 Orden FEFO: Primero en vencer aparece primero",
            font=FONTS['body_small'],
            fg=COLORS['success'],
            bg=COLORS['background']
        ).pack(side='top')
        
        tk.Label(
            info_frame,
            text="📊 Los lotes se ordenan globalmente por fecha de vencimiento",
            font=FONTS['body_small'],
            fg=COLORS['text_secondary'],
            bg=COLORS['background']
        ).pack(side='top')
        
        # Frame principal para la tabla
        main_frame = tk.Frame(self, bg=COLORS['background'])
        main_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['md'])
        
        # Tabla de lotes
        self.crear_tabla_lotes(main_frame)
        
        # Panel de información detallada
        self.crear_panel_detalle(main_frame)
    
    def crear_tabla_lotes(self, parent):
        """Crea la tabla para mostrar los lotes con mejor presentación visual"""
        # Frame para la tabla
        tabla_frame = tk.Frame(parent, bg=COLORS['background'])
        tabla_frame.pack(fill='both', expand=True, pady=(0, SPACING['md']))
        
        # Título de la tabla
        tk.Label(
            tabla_frame,
            text="📋 Lotes Disponibles (Ordenados por FEFO - Primero en Vencer)",
            font=FONTS['heading_medium'],
            fg=COLORS['primary'],
            bg=COLORS['background']
        ).pack(anchor='w', pady=(0, SPACING['md']))
        
        # Configurar estilos de la tabla
        style = ttk.Style()
        style.configure(
            "Treeview",
            font=FONTS['body_medium'],
            rowheight=35,  # Filas más altas para mejor legibilidad
            background=COLORS['surface'],
            fieldbackground=COLORS['surface']
        )
        style.configure(
            "Treeview.Heading",
            font=FONTS['heading_small'],
            background=COLORS['primary'],
            foreground=COLORS['surface'],
            relief='flat'
        )
        
        # Crear tabla
        columns = [
            "codigo", "nombre", "stock_actual", "fecha_vencimiento",
            "dias_vencimiento", "estado_vencimiento", "numero_lote"
        ]
        
        self.tabla_lotes = ttk.Treeview(
            tabla_frame,
            columns=columns,
            show='headings',
            style="Treeview",
            height=20  # Altura fija para mejor presentación
        )
        
        # Configurar columnas con mejor ancho y alineación
        headers = [
            ("codigo", "Código", 100, 'center'),
            ("nombre", "Nombre del Producto", 280, 'w'),
            ("stock_actual", "Stock", 80, 'center'),
            ("fecha_vencimiento", "Vencimiento", 120, 'center'),
            ("dias_vencimiento", "Días Restantes", 120, 'center'),
            ("estado_vencimiento", "Estado", 120, 'center'),
            ("numero_lote", "Número de Lote", 250, 'w')
        ]
        
        for col, header, width, anchor in headers:
            self.tabla_lotes.heading(col, text=header)
            self.tabla_lotes.column(col, width=width, anchor=anchor, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tabla_lotes.yview)
        self.tabla_lotes.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.tabla_lotes.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar eventos
        self.tabla_lotes.bind('<<TreeviewSelect>>', self.on_lote_selected)
        
        # Configurar tags para colorear filas con mejor contraste
        self.tabla_lotes.tag_configure('vencimiento_proximo', background='#fff3cd', foreground='#856404')  # Amarillo con texto oscuro
        self.tabla_lotes.tag_configure('vencimiento_critico', background='#f8d7da', foreground='#721c24')  # Rojo con texto oscuro
        self.tabla_lotes.tag_configure('sin_vencimiento', background='#d1ecf1', foreground='#0c5460')    # Azul con texto oscuro
    
    def crear_panel_detalle(self, parent):
        """Crea el panel de información detallada del lote seleccionado"""
        # Frame para detalles
        detalle_frame = tk.Frame(parent, bg=COLORS['surface'], relief='solid', borderwidth=1)
        detalle_frame.pack(fill='x', pady=(SPACING['md'], 0))
        
        # Título del panel de detalles
        tk.Label(
            detalle_frame,
            text="📊 Detalles del Lote Seleccionado",
            font=FONTS['heading_small'],
            fg=COLORS['primary'],
            bg=COLORS['surface']
        ).pack(anchor='w', padx=SPACING['md'], pady=SPACING['sm'])
        
        # Frame para la información
        info_frame = tk.Frame(detalle_frame, bg=COLORS['surface'])
        info_frame.pack(fill='x', padx=SPACING['md'], pady=(0, SPACING['md']))
        
        # Variables para mostrar información
        self.lbl_codigo = tk.Label(info_frame, text="Código: -", font=FONTS['body_medium'], bg=COLORS['surface'])
        self.lbl_codigo.grid(row=0, column=0, sticky='w', padx=(0, SPACING['lg']), pady=2)
        
        self.lbl_nombre = tk.Label(info_frame, text="Nombre: -", font=FONTS['body_medium'], bg=COLORS['surface'])
        self.lbl_nombre.grid(row=0, column=1, sticky='w', padx=(0, SPACING['lg']), pady=2)
        
        self.lbl_stock = tk.Label(info_frame, text="Stock: -", font=FONTS['body_medium'], bg=COLORS['surface'])
        self.lbl_stock.grid(row=0, column=2, sticky='w', padx=(0, SPACING['lg']), pady=2)
        
        self.lbl_vencimiento = tk.Label(info_frame, text="Vencimiento: -", font=FONTS['body_medium'], bg=COLORS['surface'])
        self.lbl_vencimiento.grid(row=1, column=0, sticky='w', padx=(0, SPACING['lg']), pady=2)
        
        self.lbl_dias = tk.Label(info_frame, text="Días para vencer: -", font=FONTS['body_medium'], bg=COLORS['surface'])
        self.lbl_dias.grid(row=1, column=1, sticky='w', padx=(0, SPACING['lg']), pady=2)
        
        self.lbl_lote = tk.Label(info_frame, text="Lote: -", font=FONTS['body_medium'], bg=COLORS['surface'])
        self.lbl_lote.grid(row=1, column=2, sticky='w', padx=(0, SPACING['lg']), pady=2)
    
    def cargar_lotes(self):
        """Carga y muestra todos los lotes disponibles ordenados globalmente por FEFO"""
        try:
            # Obtener todos los productos
            from services.api import get
            resp = get("/products")
            if not resp.success:
                raise Exception(resp.message or "Error al obtener productos")
            
            productos = resp.data or []
            self.tabla_lotes.delete(*self.tabla_lotes.get_children())
            
            # Lista para almacenar todos los lotes antes de ordenar
            todos_lotes = []
            fecha_actual = datetime.date.today()
            
            for producto in productos:
                if producto.get("estado") == "baja":
                    continue
                
                try:
                    # Usar el servicio FEFO para obtener todos los lotes del producto
                    lotes_producto = FEFOService.obtener_lotes_producto(producto['id'])
                    
                    if lotes_producto:
                        # Agregar cada lote a la lista general
                        for lote in lotes_producto:
                            fecha_vencimiento = lote.fecha_vencimiento
                            cantidad_lote = lote.cantidad
                            
                            if fecha_vencimiento == '9999-12-31':
                                fecha_vencimiento = 'Sin fecha'
                                dias_vencimiento = 999999  # Para ordenar al final
                                estado_vencimiento = 'Sin vencimiento'
                                tag = 'sin_vencimiento'
                            else:
                                try:
                                    fecha_venc = datetime.datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
                                    dias_vencimiento = (fecha_venc - fecha_actual).days
                                    
                                    if dias_vencimiento < 0:
                                        estado_vencimiento = 'Vencido'
                                        tag = 'vencimiento_critico'
                                    elif dias_vencimiento <= 30:
                                        estado_vencimiento = 'Próximo a vencer'
                                        tag = 'vencimiento_proximo'
                                    else:
                                        estado_vencimiento = 'Vigente'
                                        tag = ''
                                    
                                except Exception:
                                    fecha_vencimiento = 'Error en fecha'
                                    dias_vencimiento = 999998  # Para ordenar al final
                                    estado_vencimiento = 'Error'
                                    tag = ''
                            
                            # Crear objeto de lote para ordenamiento
                            lote_info = {
                                'producto': producto,
                                'lote': lote,
                                'fecha_vencimiento': fecha_vencimiento,
                                'dias_vencimiento': dias_vencimiento,
                                'estado_vencimiento': estado_vencimiento,
                                'tag': tag,
                                'cantidad_lote': cantidad_lote
                            }
                            
                            todos_lotes.append(lote_info)
                    else:
                        # Fallback: crear lote principal si no hay lotes FEFO
                        fecha_vencimiento = producto.get('fecha_vencimiento')
                        stock_actual = producto.get('stock_actual', 0)
                        
                        if not fecha_vencimiento:
                            fecha_vencimiento = 'Sin fecha'
                            dias_vencimiento = 999999
                            estado_vencimiento = 'Sin vencimiento'
                            tag = 'sin_vencimiento'
                        else:
                            try:
                                fecha_venc = datetime.datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
                                dias_vencimiento = (fecha_venc - fecha_actual).days
                                
                                if dias_vencimiento < 0:
                                    estado_vencimiento = 'Vencido'
                                    tag = 'vencimiento_critico'
                                elif dias_vencimiento <= 30:
                                    estado_vencimiento = 'Próximo a vencer'
                                    tag = 'vencimiento_proximo'
                                else:
                                    estado_vencimiento = 'Vigente'
                                    tag = ''
                                
                            except Exception:
                                fecha_vencimiento = 'Error en fecha'
                                dias_vencimiento = 999998
                                estado_vencimiento = 'Error'
                                tag = ''
                        
                        # Crear objeto de lote para ordenamiento
                        lote_info = {
                            'producto': producto,
                            'lote': None,
                            'fecha_vencimiento': fecha_vencimiento,
                            'dias_vencimiento': dias_vencimiento,
                            'estado_vencimiento': estado_vencimiento,
                            'tag': tag,
                            'cantidad_lote': stock_actual
                        }
                        
                        todos_lotes.append(lote_info)
                        
                except Exception as e:
                    print(f"Error al cargar lotes para producto {producto.get('nombre_item', '')}: {e}")
                    # Continuar con el siguiente producto
                    continue
            
            # ORDENAR TODOS LOS LOTES GLOBALMENTE POR FEFO (fecha de vencimiento)
            todos_lotes.sort(key=lambda x: x['dias_vencimiento'])
            
            # Insertar lotes ordenados en la tabla
            count = 0
            for lote_info in todos_lotes:
                producto = lote_info['producto']
                lote = lote_info['lote']
                fecha_vencimiento = lote_info['fecha_vencimiento']
                dias_vencimiento = lote_info['dias_vencimiento']
                estado_vencimiento = lote_info['estado_vencimiento']
                tag = lote_info['tag']
                cantidad_lote = lote_info['cantidad_lote']
                
                # Formatear días para mostrar
                if dias_vencimiento >= 999998:
                    dias_vencimiento_str = 'N/A'
                else:
                    dias_vencimiento_str = f"{dias_vencimiento} días"
                
                # Número de lote
                if lote:
                    numero_lote = lote.numero_lote
                else:
                    numero_lote = f"LOTE-{producto['id']}-{fecha_vencimiento}" if fecha_vencimiento != 'Sin fecha' else f"LOTE-{producto['id']}-SIN-VENCIMIENTO"
                
                # Insertar en la tabla
                self.tabla_lotes.insert('', 'end', values=(
                    producto.get('codigo_item', ''),
                    producto.get('nombre_item', ''),
                    cantidad_lote,
                    fecha_vencimiento,
                    dias_vencimiento_str,
                    estado_vencimiento,
                    numero_lote
                ), tags=(tag,) if tag else ())
                
                count += 1
            
            self.lbl_status.config(text=f"Lotes cargados: {count} (Ordenados por FEFO)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar lotes: {str(e)}")
    
    def on_lote_selected(self, event):
        """Maneja la selección de un lote en la tabla"""
        selection = self.tabla_lotes.selection()
        if not selection:
            return
        
        # Obtener datos del lote seleccionado
        item = self.tabla_lotes.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        # Actualizar panel de detalles
        self.lbl_codigo.config(text=f"Código: {values[0]}")
        self.lbl_nombre.config(text=f"Nombre: {values[1]}")
        self.lbl_stock.config(text=f"Stock: {values[2]}")
        self.lbl_vencimiento.config(text=f"Vencimiento: {values[3]}")
        self.lbl_dias.config(text=f"Días para vencer: {values[4]}")
        self.lbl_lote.config(text=f"Lote: {values[6]}")
    
    def simular_salida_fefo(self):
        """Abre ventana para simular una salida FEFO"""
        # Obtener lote seleccionado
        selection = self.tabla_lotes.selection()
        if not selection:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un lote para simular la salida.")
            return
        
        item = self.tabla_lotes.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        # Extraer información del lote
        codigo = values[0]
        nombre = values[1]
        stock_actual = values[2]
        
        # Crear ventana de simulación
        self.crear_ventana_simulacion(codigo, nombre, stock_actual)
    
    def crear_ventana_simulacion(self, codigo, nombre, stock_actual):
        """Crea ventana para simular salida FEFO"""
        top = tk.Toplevel(self)
        top.title("Simular Salida FEFO")
        top.geometry("600x500")
        top.configure(bg=COLORS['background'])
        top.resizable(False, False)
        
        # Centrar ventana
        top.transient(self)
        top.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(top, bg=COLORS['background'])
        main_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Título
        tk.Label(
            main_frame,
            text="🧮 Simulación de Salida FEFO",
            font=FONTS['title_small'],
            fg=COLORS['primary'],
            bg=COLORS['background']
        ).pack(pady=(0, SPACING['lg']))
        
        # Información del producto
        info_frame = tk.Frame(main_frame, bg=COLORS['surface'], relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=(0, SPACING['md']))
        
        tk.Label(
            info_frame,
            text=f"Producto: {codigo} - {nombre}",
            font=FONTS['heading_small'],
            bg=COLORS['surface']
        ).pack(anchor='w', padx=SPACING['md'], pady=SPACING['sm'])
        
        tk.Label(
            info_frame,
            text=f"Stock disponible: {stock_actual} unidades",
            font=FONTS['body_medium'],
            bg=COLORS['surface']
        ).pack(anchor='w', padx=SPACING['md'], pady=(0, SPACING['sm']))
        
        # Campo de cantidad
        input_frame = tk.Frame(main_frame, bg=COLORS['background'])
        input_frame.pack(fill='x', pady=SPACING['md'])
        
        tk.Label(
            input_frame,
            text="Cantidad a simular:",
            font=FONTS['heading_small'],
            fg=COLORS['text_primary'],
            bg=COLORS['background']
        ).pack(anchor='w')
        
        cantidad_var = tk.StringVar()
        cantidad_entry = tk.Entry(
            input_frame,
            textvariable=cantidad_var,
            font=FONTS['body_medium'],
            width=20
        )
        cantidad_entry.pack(anchor='w', pady=(SPACING['sm'], 0))
        
        # Botón simular
        btn_frame = tk.Frame(main_frame, bg=COLORS['background'])
        btn_frame.pack(fill='x', pady=SPACING['md'])
        
        btn_simular = tk.Button(
            btn_frame,
            text="Simular Salida FEFO",
            command=lambda: self.ejecutar_simulacion(cantidad_var.get(), top),
            bg=COLORS['warning'],
            fg=COLORS['surface'],
            font=FONTS['button'],
            relief='flat',
            padx=16,
            pady=8,
            activebackground=COLORS['warning_dark'],
            cursor='hand2'
        )
        btn_simular.pack(side='left')
        
        # Área de resultados
        self.resultado_text = tk.Text(
            main_frame,
            height=15,
            font=FONTS['body_medium'],
            bg=COLORS['surface'],
            relief='solid',
            borderwidth=1
        )
        self.resultado_text.pack(fill='both', expand=True, pady=(SPACING['md'], 0))
        
        # Configurar como solo lectura
        self.resultado_text.config(state='disabled')
        
        # Botón cerrar
        btn_cerrar = tk.Button(
            main_frame,
            text="Cerrar",
            command=top.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['surface'],
            font=FONTS['button'],
            relief='flat',
            padx=16,
            pady=8,
            activebackground=COLORS['secondary_dark'],
            cursor='hand2'
        )
        btn_cerrar.pack(pady=SPACING['md'])
    
    def ejecutar_simulacion(self, cantidad_str, top):
        """Ejecuta la simulación FEFO"""
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero")
            
            # Obtener lote seleccionado
            selection = self.tabla_lotes.selection()
            if not selection:
                return
            
            item = self.tabla_lotes.item(selection[0])
            values = item['values']
            
            # Extraer código del producto (asumiendo que está en la primera columna)
            codigo_producto = values[0]
            
            # Buscar el producto por código
            from services.api import get
            resp = get("/products")
            if not resp.success:
                raise Exception(resp.message)
            
            productos = resp.data or []
            producto = None
            for p in productos:
                if p.get('codigo_item') == codigo_producto:
                    producto = p
                    break
            
            if not producto:
                raise Exception("Producto no encontrado")
            
            # Simular salida FEFO
            resultado = FEFOService.simular_salida_fefo(producto['id'], cantidad)
            
            # Mostrar resultados
            self.mostrar_resultado_simulacion(resultado)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la cantidad: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la simulación: {str(e)}")
    
    def mostrar_resultado_simulacion(self, resultado):
        """Muestra el resultado de la simulación"""
        self.resultado_text.config(state='normal')
        self.resultado_text.delete(1.0, tk.END)
        
        if resultado['success']:
            sim = resultado['simulacion']
            
            texto = f"✅ SIMULACIÓN FEFO EXITOSA\n"
            texto += f"{'='*50}\n\n"
            texto += f"📦 Cantidad solicitada: {sim['cantidad_solicitada']} unidades\n"
            texto += f"📊 Stock disponible: {sim['stock_disponible']} unidades\n"
            texto += f"📉 Stock restante: {sim['stock_restante']} unidades\n"
            texto += f"📋 Resumen: {sim['resumen']}\n\n"
            texto += f"🔍 DETALLE DE DISTRIBUCIÓN:\n"
            texto += f"{'='*30}\n"
            
            for i, lote in enumerate(sim['lotes_afectados'], 1):
                texto += f"\n📦 Lote {i}:\n"
                texto += f"   • Número: {lote['numero_lote']}\n"
                texto += f"   • Cantidad usada: {lote['cantidad_usada']} unidades\n"
                texto += f"   • Fecha vencimiento: {lote['fecha_vencimiento']}\n"
                texto += f"   • Motivo: {lote['motivo']}\n"
        else:
            texto = f"❌ ERROR EN LA SIMULACIÓN\n"
            texto += f"{'='*30}\n\n"
            texto += f"Error: {resultado['message']}\n"
        
        self.resultado_text.insert(1.0, texto)
        self.resultado_text.config(state='disabled')
    
    def mostrar_historial(self):
        """Muestra el historial de movimientos de lotes"""
        # Obtener lote seleccionado
        selection = self.tabla_lotes.selection()
        if not selection:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un lote para ver su historial.")
            return
        
        item = self.tabla_lotes.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        # Extraer código del producto
        codigo_producto = values[0]
        
        try:
            # Buscar el producto por código
            from services.api import get
            resp = get("/products")
            if not resp.success:
                raise Exception(resp.message)
            
            productos = resp.data or []
            producto = None
            for p in productos:
                if p.get('codigo_item') == codigo_producto:
                    producto = p
                    break
            
            if not producto:
                raise Exception("Producto no encontrado")
            
            # Obtener historial
            historial = FEFOService.obtener_historial_lotes(producto['id'])
            
            if not historial:
                messagebox.showinfo("Historial", "No hay movimientos FEFO registrados para este producto.")
                return
            
            # Mostrar historial en nueva ventana
            self.mostrar_ventana_historial(historial, producto)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener historial: {str(e)}")
    
    def mostrar_ventana_historial(self, historial, producto):
        """Muestra ventana con el historial de lotes"""
        top = tk.Toplevel(self)
        top.title(f"Historial FEFO - {producto.get('nombre_item', '')}")
        top.geometry("800x600")
        top.configure(bg=COLORS['background'])
        
        # Frame principal
        main_frame = tk.Frame(top, bg=COLORS['background'])
        main_frame.pack(fill='both', expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Título
        tk.Label(
            main_frame,
            text=f"📊 Historial FEFO - {producto.get('nombre_item', '')}",
            font=FONTS['title_small'],
            fg=COLORS['primary'],
            bg=COLORS['background']
        ).pack(pady=(0, SPACING['lg']))
        
        # Tabla de historial - Solo 3 columnas útiles
        columns = ("fecha", "cantidad", "observaciones")
        tabla = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        headers = [
            ("fecha", "Fecha Movimiento", 200),
            ("cantidad", "Cantidad", 150),
            ("observaciones", "Observaciones", 400)
        ]
        
        for col, header, width in headers:
            tabla.heading(col, text=header)
            tabla.column(col, width=width, anchor='center', minwidth=100)
        
        # Insertar datos
        for mov in historial:
            fecha = mov.get('fecha_movimiento', '')
            if fecha:
                try:
                    # Formatear fecha
                    if 'T' in str(fecha):
                        fecha = str(fecha).split('T')[0]
                    fecha = fecha[:10]  # Tomar solo la fecha
                except:
                    pass
            
            # Determinar cantidad según el tipo de movimiento
            cantidad = ''
            if mov.get('tipo') == 'Salida FEFO':
                cantidad = mov.get('cantidad_salida', '')
            elif mov.get('tipo') == 'Entrada de Lote':
                cantidad = mov.get('cantidad_entrada', '')
            
            # Determinar observaciones según el tipo
            observaciones = mov.get('observaciones', '')
            if mov.get('tipo') == 'Salida FEFO':
                observaciones = f"Salida FEFO - {observaciones}"
            elif mov.get('tipo') == 'Entrada de Lote':
                observaciones = f"Entrada de lote - {observaciones}"
            
            tabla.insert('', 'end', values=(
                fecha,
                cantidad,
                observaciones
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botón cerrar
        tk.Button(
            main_frame,
            text="Cerrar",
            command=top.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['surface'],
            font=FONTS['button'],
            relief='flat',
            padx=16,
            pady=8,
            activebackground=COLORS['secondary_dark'],
            cursor='hand2'
        ).pack(pady=SPACING['md'])
