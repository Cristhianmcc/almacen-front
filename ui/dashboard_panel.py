import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get
from services.fefo_service import FEFOService
from ui.styles import COLORS, FONTS, SPACING, DIMENSIONS
import datetime
from typing import List, Dict

class DashboardPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        # NO cargar datos automáticamente - solo mostrar la UI
        # Los datos se cargarán SOLO cuando el usuario haga clic en "Actualizar Dashboard"
        # self.mostrar_estado_inicial()  # COMENTADO: No mostrar estado inicial automáticamente

    def create_widgets(self):
        # Configurar el frame principal
        self.configure(style='TFrame')
        
        # Título principal
        self.lbl_title = tk.Label(
            self, 
            text="Panel de Control de Almacén", 
            font=FONTS['title_large'], 
            background=COLORS['background'], 
            foreground=COLORS['primary']
        )
        self.lbl_title.pack(pady=(SPACING['lg'], SPACING['md']), anchor='center', fill='x')
        
        # ===== BOTÓN DE ACTUALIZACIÓN ARRIBA =====
        btn_frame = tk.Frame(self, bg=COLORS['background'])
        btn_frame.pack(fill='x', padx=SPACING['md'], pady=(0, SPACING['lg']))
        
        # Botón principal de actualización
        self.btn_actualizar = tk.Button(
            btn_frame,
            text="🔄 Actualizar Panel",
            command=self.cargar_estadisticas,
            font=FONTS['body_medium'],
            bg=COLORS['primary'],
            fg=COLORS['surface'],
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_actualizar.pack(anchor='center')
        
        # Indicador de estado de carga
        self.lbl_estado = tk.Label(
            btn_frame,
            text="💡 Haz clic en 'Actualizar Dashboard' para cargar los datos",
            font=FONTS['body_small'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        )
        self.lbl_estado.pack(anchor='center', pady=(SPACING['sm'], 0))
        
        # Frame principal con scroll - LAYOUT CORREGIDO
        main_frame = tk.Frame(self, bg=COLORS['background'])
        main_frame.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['sm'])
        
        # Canvas para scroll - SIN ESPACIOS EN BLANCO
        canvas = tk.Canvas(main_frame, bg=COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])
        
        # Configurar el canvas correctamente - SIN ESPACIOS
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar el scroll region cuando el frame se configure
        def _on_frame_configure(event):
            # Asegurar que el canvas se expanda completamente
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Hacer que el frame interno tenga el ancho completo del canvas
            canvas.itemconfig(canvas.find_withtag("all")[0], width=canvas.winfo_width())
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        
        # ===== SECCIÓN 1: ALERTAS CRÍTICAS =====
        self.crear_seccion_alertas(scrollable_frame)
        
        # Separador visual
        tk.Frame(scrollable_frame, height=2, bg=COLORS['border']).pack(fill='x', pady=SPACING['md'])
        
        # ===== SECCIÓN 2: MÉTRICAS FEFO =====
        self.crear_seccion_metricas_fefo(scrollable_frame)
        
        # Separador visual
        tk.Frame(scrollable_frame, height=2, bg=COLORS['border']).pack(fill='x', pady=SPACING['md'])
        
        # ===== SECCIÓN 3: ESTADÍSTICAS GENERALES =====
        self.crear_seccion_estadisticas(scrollable_frame)
        
        # Separador visual
        tk.Frame(scrollable_frame, height=2, bg=COLORS['border']).pack(fill='x', pady=SPACING['md'])
        
        # ===== SECCIÓN 4: PRODUCTOS PRÓXIMOS A VENCER =====
        self.crear_seccion_vencimientos(scrollable_frame)
        
        # Indicador de scroll
        indicador_frame = tk.Frame(scrollable_frame, bg=COLORS['background'])
        indicador_frame.pack(fill='x', pady=SPACING['md'])
        
        tk.Label(
            indicador_frame,
            text="📜 Usa la rueda del mouse o la barra de desplazamiento para ver más contenido",
            font=FONTS['body_small'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(anchor='center')
        
        # Configurar scroll - LAYOUT RESPONSIVE SIN ESPACIOS
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar eventos de scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Hacer el layout responsive
        def _on_canvas_resize(event):
            # Ajustar el ancho del frame interno cuando cambie el tamaño del canvas
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
        
        canvas.bind('<Configure>', _on_canvas_resize)

    def mostrar_estado_inicial(self):
        """Muestra el estado inicial del dashboard sin cargar datos"""
        try:
            # Mostrar valores iniciales en las métricas
            for key in self.metricas_fefo:
                self.metricas_fefo[key].config(text="--")
            for key in self.stats:
                self.stats[key].config(text="--")
            
            # Mostrar mensaje de estado inicial
            self.mostrar_mensaje_estado_inicial()
            
        except Exception as e:
            print(f"Error al mostrar estado inicial: {e}")
    
    def mostrar_mensaje_estado_inicial(self):
        """Muestra un mensaje indicando que el dashboard está listo para usar"""
        try:
            # Limpiar alertas anteriores
            for widget in self.alertas_container.winfo_children():
                widget.destroy()
            
            # Mensaje principal
            tk.Label(
                self.alertas_container,
                text="🚀 Dashboard FEFO Listo",
                font=FONTS['heading_small'],
                bg=COLORS['success'],
                fg=COLORS['surface'],
                relief="flat",
                padx=15,
                pady=8
            ).pack(fill='x', pady=2)
            
            # Instrucciones
            tk.Label(
                self.alertas_container,
                text="💡 Haz clic en 'Actualizar Dashboard' para cargar los datos",
                font=FONTS['body_small'],
                bg=COLORS['info'],
                fg=COLORS['surface'],
                relief="flat",
                padx=15,
                pady=6
            ).pack(fill='x', pady=2)
            
        except Exception as e:
            print(f"Error al mostrar mensaje de estado inicial: {e}")

    def crear_seccion_alertas(self, parent):
        """Crea la sección de alertas críticas"""
        alertas_frame = tk.Frame(parent, bg=COLORS['background'])
        alertas_frame.pack(fill='x', pady=(0, SPACING['lg']))
        
        # Título de sección
        tk.Label(
            alertas_frame,
            text="🚨 Alertas Críticas",
            font=FONTS['heading_large'],
            bg=COLORS['background'],
            fg=COLORS['danger']
        ).pack(anchor='w', pady=(0, SPACING['md']))
        
        # Frame para las alertas
        self.alertas_container = tk.Frame(alertas_frame, bg=COLORS['background'])
        self.alertas_container.pack(fill='x')

    def crear_seccion_metricas_fefo(self, parent):
        """Crea la sección de métricas FEFO"""
        fefo_frame = tk.Frame(parent, bg=COLORS['background'])
        fefo_frame.pack(fill='x', pady=(0, SPACING['lg']))
        
        # Título de sección
        tk.Label(
            fefo_frame,
            text="🎯 Métricas FEFO",
            font=FONTS['heading_large'],
            bg=COLORS['background'],
            fg=COLORS['accent']
        ).pack(anchor='w', pady=(0, SPACING['md']))
        
        # Grid de métricas FEFO
        self.metricas_fefo_frame = tk.Frame(fefo_frame, bg=COLORS['background'])
        self.metricas_fefo_frame.pack(fill='x')
        self.metricas_fefo_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='col')
        
        # Métricas FEFO
        self.metricas_fefo = {}
        metricas_info = [
            ("total_lotes", "📦 Total Lotes", COLORS['primary'], "Lotes activos"),
            ("lotes_vencen_30", "⏰ Vencen en 30 días", COLORS['warning'], "Próximos a vencer"),
            ("lotes_vencen_60", "⚠️ Vencen en 60 días", COLORS['warning'], "Atención"),
            ("lotes_vencidos", "🚨 Lotes Vencidos", COLORS['danger'], "Crítico")
        ]
        
        for i, (key, title, color, desc) in enumerate(metricas_info):
            self.crear_metrica_fefo(key, title, color, desc, i)

    def crear_metrica_fefo(self, key, title, color, desc, col):
        """Crea una métrica FEFO individual"""
        card = tk.Frame(
            self.metricas_fefo_frame,
            bg=COLORS['surface'],
            bd=0,
            highlightbackground=color,
            highlightthickness=2,
            relief="flat"
        )
        card.grid(row=0, column=col, padx=SPACING['sm'], pady=SPACING['sm'], sticky='nsew')
        
        # Valor
        self.metricas_fefo[key] = tk.Label(
            card,
            text="0",
            font=FONTS['title_large'],
            bg=COLORS['surface'],
            fg=color
        )
        self.metricas_fefo[key].pack(pady=(SPACING['md'], SPACING['xs']))
        
        # Título
        tk.Label(
            card,
            text=title,
            font=FONTS['heading_small'],
            bg=COLORS['surface'],
            fg=color
        ).pack(pady=(0, SPACING['xs']))
        
        # Descripción
        tk.Label(
            card,
            text=desc,
            font=FONTS['body_small'],
            bg=COLORS['surface'],
            fg=COLORS['text_secondary'],
            wraplength=200
        ).pack(pady=(0, SPACING['sm']))

    def crear_seccion_estadisticas(self, parent):
        """Crea la sección de estadísticas generales"""
        stats_frame = tk.Frame(parent, bg=COLORS['background'])
        stats_frame.pack(fill='x', pady=(0, SPACING['lg']))
        
        # Título de sección
        tk.Label(
            stats_frame,
            text="📊 Estadísticas Generales",
            font=FONTS['heading_large'],
            bg=COLORS['background'],
            fg=COLORS['primary']
        ).pack(anchor='w', pady=(0, SPACING['md']))
        
        # Grid de estadísticas
        self.stats_frame = tk.Frame(stats_frame, bg=COLORS['background'])
        self.stats_frame.pack(fill='x')
        self.stats_frame.columnconfigure((0, 1, 2), weight=1, uniform='col')
        
        # Estadísticas
        self.stats = {}
        stats_info = [
            ("total_productos", "📦 Total Productos", COLORS['primary'], "Productos activos"),
            ("total_movimientos", "🔄 Total Movimientos", COLORS['success'], "Entradas y salidas"),
            ("stock_bajo", "📉 Stock Bajo", COLORS['warning'], "≤10 unidades")
        ]
        
        for i, (key, title, color, desc) in enumerate(stats_info):
            self.crear_estadistica(key, title, color, desc, i)

    def crear_estadistica(self, key, title, color, desc, col):
        """Crea una estadística individual"""
        card = tk.Frame(
            self.stats_frame,
            bg=COLORS['surface'],
            bd=0,
            highlightbackground=color,
            highlightthickness=2,
            relief="flat"
        )
        card.grid(row=0, column=col, padx=SPACING['sm'], pady=SPACING['sm'], sticky='nsew')
        
        # Valor
        self.stats[key] = tk.Label(
            card,
            text="0",
            font=FONTS['title_large'],
            bg=COLORS['surface'],
            fg=color
        )
        self.stats[key].pack(pady=(SPACING['md'], SPACING['xs']))
        
        # Título
        tk.Label(
            card,
            text=title,
            font=FONTS['heading_small'],
            bg=COLORS['surface'],
            fg=color
        ).pack(pady=(0, SPACING['xs']))
        
        # Descripción
        tk.Label(
            card,
            text=desc,
            font=FONTS['body_small'],
            bg=COLORS['surface'],
            fg=COLORS['text_secondary'],
            wraplength=200
        ).pack(pady=(0, SPACING['sm']))

    def crear_seccion_vencimientos(self, parent):
        """Crea la sección de productos próximos a vencer"""
        vencimientos_frame = tk.Frame(parent, bg=COLORS['background'])
        vencimientos_frame.pack(fill='both', expand=True, pady=(0, SPACING['lg']))
        
        # Título de sección
        tk.Label(
            vencimientos_frame,
            text="⏰ Productos Próximos a Vencer",
            font=FONTS['heading_large'],
            bg=COLORS['background'],
            fg=COLORS['warning']
        ).pack(anchor='w', pady=(0, SPACING['md']))
        
        # Tabla de productos próximos a vencer
        self.crear_tabla_vencimientos(vencimientos_frame)

    def crear_tabla_vencimientos(self, parent):
        """Crea la tabla de productos próximos a vencer"""
        # Frame para la tabla
        tabla_frame = tk.Frame(parent, bg=COLORS['background'])
        tabla_frame.pack(fill='x', pady=(0, SPACING['md']))
        
        # Scrollbar
        vsb = tk.Scrollbar(tabla_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        
        # Tabla
        columns = ("producto", "lote", "cantidad", "fecha_vencimiento", "dias_restantes", "estado")
        self.tabla_vencimientos = ttk.Treeview(
            tabla_frame,
            columns=columns,
            show='headings',
            yscrollcommand=vsb.set,
            height=6  # Reducir altura para que no ocupe tanto espacio
        )
        self.tabla_vencimientos.pack(side='left', fill='x', expand=True)
        vsb.config(command=self.tabla_vencimientos.yview)
        
        # Configurar columnas
        headers = [
            ("producto", "Producto", 180),
            ("lote", "Número de Lote", 120),
            ("cantidad", "Cantidad", 80),
            ("fecha_vencimiento", "Fecha Vencimiento", 120),
            ("dias_restantes", "Días Restantes", 100),
            ("estado", "Estado", 80)
        ]
        
        for col, header, width in headers:
            self.tabla_vencimientos.heading(col, text=header)
            self.tabla_vencimientos.column(col, width=width, anchor='center', minwidth=80)
        
        # Configurar tags para colores
        self.tabla_vencimientos.tag_configure('vencido', background='#ffebee')
        self.tabla_vencimientos.tag_configure('proximo', background='#fff3e0')
        self.tabla_vencimientos.tag_configure('normal', background='#e8f5e8')

    def cargar_estadisticas(self):
        """Carga todas las estadísticas del dashboard de forma optimizada"""
        try:
            # Mostrar indicador de carga
            self.mostrar_indicador_carga()
            
            # Cargar datos de forma secuencial pero optimizada
            self.cargar_datos_basicos()
            
            # Finalizar carga y restaurar UI
            self.finalizar_carga()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estadísticas: {str(e)}")
            # Restaurar UI en caso de error
            self.finalizar_carga()
    
    def mostrar_indicador_carga(self):
        """Muestra un indicador de carga en las métricas y el botón"""
        try:
            # Deshabilitar botón durante la carga
            self.btn_actualizar.config(state="disabled", text="⏳ Cargando...")
            
            # Cambiar texto del estado
            self.lbl_estado.config(text="🔄 Cargando datos del dashboard...", fg=COLORS['primary'])
            
            # Mostrar indicador de carga en las métricas
            for key in self.metricas_fefo:
                self.metricas_fefo[key].config(text="⏳")
            for key in self.stats:
                self.stats[key].config(text="⏳")
                
        except Exception as e:
            print(f"❌ Error al mostrar indicador de carga: {e}")
    
    def finalizar_carga(self):
        """Finaliza el estado de carga y restaura el botón"""
        try:
            # Restaurar botón
            self.btn_actualizar.config(state="normal", text="🔄 Actualizar Dashboard")
            
            # Cambiar texto del estado
            self.lbl_estado.config(text="✅ Dashboard actualizado correctamente", fg=COLORS['success'])
            
            # Programar que el mensaje desaparezca en 3 segundos
            self.after(3000, lambda: self.lbl_estado.config(
                text="💡 Los datos se actualizan automáticamente cada 5 minutos",
                fg=COLORS['text_secondary']
            ))
            
        except Exception as e:
            print(f"❌ Error al finalizar carga: {e}")
    
    def cargar_datos_basicos(self):
        """Carga los datos básicos de forma optimizada"""
        try:
            # Obtener todos los productos de una sola vez
            productos_resp = get("/products")
            if not productos_resp.success:
                return
            
            productos = productos_resp.data or []
            productos_activos = [p for p in productos if p.get("estado") != "baja"]
            
            # Cargar estadísticas generales primero (más rápido)
            self.cargar_estadisticas_generales_rapido(productos_activos)
            
            # Cargar métricas FEFO optimizadas
            self.cargar_metricas_fefo_optimizado(productos_activos)
            
            # Cargar alertas críticas
            self.cargar_alertas_criticas_optimizado(productos_activos)
            
            # Cargar tabla de vencimientos
            self.cargar_productos_vencimientos_optimizado(productos_activos)
            
        except Exception as e:
            print(f"❌ Error al cargar datos básicos: {e}")
    
    def cargar_estadisticas_generales_rapido(self, productos_activos):
        """Carga estadísticas generales de forma rápida"""
        try:
            # Productos
            total_productos = len(productos_activos)
            
            # Stock bajo
            stock_bajo = sum(1 for p in productos_activos if p.get("stock_actual", 0) <= 10)
            
            # Movimientos (solo contamos, no cargamos detalles)
            movimientos_resp = get("/movements")
            total_movimientos = len(movimientos_resp.data or []) if movimientos_resp.success else 0
            
            # Actualizar estadísticas
            self.stats['total_productos'].config(text=str(total_productos))
            self.stats['total_movimientos'].config(text=str(total_movimientos))
            self.stats['stock_bajo'].config(text=str(stock_bajo))
            
        except Exception as e:
            print(f"Error al cargar estadísticas generales: {e}")
    
    def cargar_metricas_fefo_optimizado(self, productos_activos):
        """Carga métricas FEFO de forma optimizada"""
        try:
            total_lotes = 0
            lotes_vencen_30 = 0
            lotes_vencen_60 = 0
            lotes_vencidos = 0
            
            fecha_actual = datetime.date.today()
            
            for producto in productos_activos:
                try:
                    lotes = FEFOService.obtener_lotes_producto(producto['id'])
                    total_lotes += len(lotes)
                    
                    for lote in lotes:
                        fecha_venc = datetime.datetime.strptime(lote.fecha_vencimiento, '%Y-%m-%d').date()
                        dias_restantes = (fecha_venc - fecha_actual).days
                        
                        if dias_restantes <= 0:
                            lotes_vencidos += 1
                        elif dias_restantes <= 30:
                            lotes_vencen_30 += 1
                        elif dias_restantes <= 60:
                            lotes_vencen_60 += 1
                except:
                    pass
            
            # Actualizar métricas
            self.metricas_fefo['total_lotes'].config(text=str(total_lotes))
            self.metricas_fefo['lotes_vencen_30'].config(text=str(lotes_vencen_30))
            self.metricas_fefo['lotes_vencen_60'].config(text=str(lotes_vencen_60))
            self.metricas_fefo['lotes_vencidos'].config(text=str(lotes_vencidos))
            
        except Exception as e:
            print(f"Error al cargar métricas FEFO: {e}")
    
    def cargar_alertas_criticas_optimizado(self, productos_activos):
        """Carga alertas críticas de forma optimizada"""
        try:
            # Limpiar alertas anteriores
            for widget in self.alertas_container.winfo_children():
                widget.destroy()
            
            alertas = []
            fecha_actual = datetime.date.today()
            
            for producto in productos_activos:
                stock = producto.get("stock_actual", 0)
                if stock <= 5:
                    alertas.append(f"🚨 {producto.get('nombre_item', '')} - Stock crítico: {stock}")
                
                # Verificar vencimientos próximos (solo si hay stock)
                if stock > 0:
                    try:
                        lotes = FEFOService.obtener_lotes_producto(producto['id'])
                        if lotes:
                            lote_proximo = min(lotes)
                            fecha_venc = datetime.datetime.strptime(lote_proximo.fecha_vencimiento, '%Y-%m-%d').date()
                            dias_restantes = (fecha_venc - fecha_actual).days
                            
                            if dias_restantes <= 30:
                                alertas.append(f"⏰ {producto.get('nombre_item', '')} - Vence en {dias_restantes} días")
                            elif dias_restantes <= 0:
                                alertas.append(f"🚨 {producto.get('nombre_item', '')} - ¡VENCIDO!")
                    except:
                        pass
                
                # Limitar alertas para no sobrecargar la UI
                if len(alertas) >= 5:
                    break
            
            # Mostrar alertas
            if alertas:
                for alerta in alertas:
                    tk.Label(
                        self.alertas_container,
                        text=alerta,
                        font=FONTS['body_medium'],
                        bg=COLORS['danger'],
                        fg=COLORS['surface'],
                        relief="flat",
                        padx=15,
                        pady=8
                    ).pack(fill='x', pady=2)
            else:
                tk.Label(
                    self.alertas_container,
                    text="✅ No hay alertas críticas",
                    font=FONTS['body_medium'],
                    bg=COLORS['success'],
                    fg=COLORS['surface'],
                    relief="flat",
                    padx=15,
                    pady=8
                ).pack(fill='x', pady=2)
                
        except Exception as e:
            print(f"Error al cargar alertas: {e}")
    
    def cargar_productos_vencimientos_optimizado(self, productos_activos):
        """Carga productos próximos a vencer de forma optimizada"""
        try:
            # Limpiar tabla de vencimientos
            self.tabla_vencimientos.delete(*self.tabla_vencimientos.get_children())
            
            lotes_vencimientos = []
            fecha_actual = datetime.date.today()
            
            for producto in productos_activos:
                try:
                    lotes = FEFOService.obtener_lotes_producto(producto['id'])
                    
                    for lote in lotes:
                        fecha_venc = datetime.datetime.strptime(lote.fecha_vencimiento, '%Y-%m-%d').date()
                        dias_restantes = (fecha_venc - fecha_actual).days
                        
                        # Solo mostrar lotes que vencen en los próximos 90 días o ya vencieron
                        if dias_restantes <= 90:
                            lotes_vencimientos.append({
                                'producto': producto.get('nombre_item', ''),
                                'lote': lote.numero_lote,
                                'cantidad': lote.cantidad,
                                'fecha_vencimiento': lote.fecha_vencimiento,
                                'dias_restantes': dias_restantes,
                                'estado': self.obtener_estado_vencimiento(dias_restantes)
                            })
                except:
                    pass
                
                # Limitar para no sobrecargar la tabla
                if len(lotes_vencimientos) >= 50:
                    break
            
            # Ordenar por días restantes (más críticos primero)
            lotes_vencimientos.sort(key=lambda x: x['dias_restantes'])
            
            # Insertar en la tabla
            for lote in lotes_vencimientos:
                tags = []
                if lote['dias_restantes'] <= 0:
                    tags.append('vencido')
                elif lote['dias_restantes'] <= 30:
                    tags.append('proximo')
                else:
                    tags.append('normal')
                
                self.tabla_vencimientos.insert('', 'end', values=(
                    lote['producto'],
                    lote['lote'],
                    lote['cantidad'],
                    lote['fecha_vencimiento'],
                    f"{lote['dias_restantes']} días",
                    lote['estado']
                ), tags=tags)
                
        except Exception as e:
            print(f"Error al cargar productos próximos a vencer: {e}")

    def obtener_estado_vencimiento(self, dias_restantes):
        """Determina el estado de vencimiento"""
        if dias_restantes <= 0:
            return "VENCIDO"
        elif dias_restantes <= 30:
            return "CRÍTICO"
        elif dias_restantes <= 60:
            return "ATENCIÓN"
        else:
            return "NORMAL"
    def cargar_dashboard(self):
        """Método para compatibilidad con el sistema existente"""
        self.cargar_estadisticas()

