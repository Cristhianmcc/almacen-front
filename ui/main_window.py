import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import COLORS, FONTS, SPACING, DIMENSIONS

from ui.dashboard_panel import DashboardPanel
from ui.productos_panel import ProductosPanel
from ui.movimientos_panel import MovimientosPanel
from ui.lotes_panel import LotesPanel
from ui.alertas_panel import AlertasPanel
from ui.bajas_panel import BajasPanel
from ui.sobrantes_panel import SobrantesPanel
from ui.reportes_panel import ReportesPanel


class MainWindow:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Almacén - Instituto")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Configurar icono si está disponible
        try:
            self.root.iconbitmap("ui/img/icono.ico")
        except:
            pass
        
        # Sistema de cache para paneles (inicializar ANTES de crear widgets)
        self.panel_cache = {}
        self.data_cache = {}
        self.last_data_update = {}
        
        # Configurar estilo global
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Configurar eventos
        self.setup_events()
        
        # NO cargar dashboard por defecto - solo mostrar la UI
        # Los datos se cargarán cuando el usuario haga clic en "Actualizar Dashboard"

    def setup_styles(self):
        """Configura estilos globales de la aplicación"""
        style = ttk.Style()
        
        # Configurar tema y colores
        style.theme_use('clam')
        
        # Estilo para el notebook (pestañas)
        style.configure(
            'TNotebook', 
            background=COLORS['background'],
            borderwidth=0
        )
        style.configure(
            'TNotebook.Tab', 
            background=COLORS['surface'],
            foreground=COLORS['text_primary'],
            padding=[20, 12],
            font=FONTS['button']
        )
        style.map(
            'TNotebook.Tab',
            background=[
                ('selected', COLORS['primary']),
                ('active', COLORS['primary_dark'])
            ],
            foreground=[
                ('selected', COLORS['surface']),
                ('active', COLORS['surface'])
            ]
        )
        
        # Estilo para frames
        style.configure(
            'TFrame', 
            background=COLORS['background']
        )
        
        # Estilo para botones
        style.configure(
            'TButton',
            background=COLORS['primary'],
            foreground=COLORS['surface'],
            font=FONTS['button'],
            padding=[16, 8]
        )
        style.map(
            'TButton',
            background=[
                ('active', COLORS['primary_dark']),
                ('pressed', COLORS['primary_dark'])
            ]
        )

    def create_widgets(self):
        """Crea todos los widgets de la interfaz principal"""
        # Configurar color de fondo principal
        self.root.configure(bg=COLORS['background'])
        
        # Header principal con mejor diseño
        header = tk.Frame(
            self.root, 
            bg=COLORS['primary'], 
            height=80,
            relief="flat"
        )
        header.pack(fill='x', pady=0)
        header.pack_propagate(False)
        
        # Título principal con mejor tipografía
        title_label = tk.Label(
            header, 
            text="Sistema de Almacén", 
            font=FONTS['title_large'], 
            fg=COLORS['surface'], 
            bg=COLORS['primary']
        )
        title_label.pack(anchor='center', pady=20)
        
        # Subtitle con información del instituto
        subtitle_label = tk.Label(
            header, 
            text="Instituto de Educación Superior", 
            font=FONTS['body_large'], 
            fg=COLORS['surface'], 
            bg=COLORS['primary']
        )
        subtitle_label.pack(anchor='center', pady=(0, 15))
        
        # Frame principal para contenido
        self.main_frame = tk.Frame(
            self.root, 
            bg=COLORS['background'],
            relief="flat"
        )
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Notebook (pestañas) con mejor diseño
        self.notebook = ttk.Notebook(
            self.main_frame, 
            style='TNotebook'
        )
        self.notebook.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Crear paneles con mejor diseño
        self.create_panels()
        
        # Barra de estado con mejor diseño
        self.create_status_bar()

    def create_panels(self):
        """Crea solo el panel del dashboard inicialmente, los demás se crean bajo demanda"""
        # Solo crear el dashboard al inicio
        self.dashboard_panel = DashboardPanel(self.notebook)
        self.notebook.add(
            self.dashboard_panel, 
            text="📊 Panel", 
            padding=[10, 15]
        )
        
        # Marcar dashboard como creado y actualizado
        self.panel_cache["Dashboard"] = True
        self.mark_data_updated("Dashboard")
        
        # Crear pestañas con frames temporales que se reemplazarán
        self.create_temp_tabs()
        
        # Los demás paneles se crearán cuando se seleccione su pestaña
        self.productos_panel = None
        self.movimientos_panel = None
        self.lotes_panel = None
        self.bajas_panel = None
        self.sobrantes_panel = None
        self.alertas_panel = None
        self.reportes_panel = None
        
        # Configurar el evento de cambio de pestaña
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)

    def create_temp_tabs(self):
        """Crea pestañas temporales que se reemplazarán con paneles reales"""
        # Frame temporal para productos
        self.temp_productos = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.temp_productos, text="📦 Productos", padding=[10, 15])
        
        # Frame temporal para movimientos
        self.temp_movimientos = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.temp_movimientos, text="🔄 Movimientos", padding=[10, 15])
        
        # Frame temporal para lotes
        self.temp_lotes = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.temp_lotes, text="📦 Lotes FEFO", padding=[10, 15])
        
        # Frame temporal para bajas
        self.temp_bajas = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.temp_bajas, text="🗑️ Bajas", padding=[10, 15])
        
        # Frame temporal para sobrantes
        self.temp_sobrantes = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.temp_sobrantes, text="➕ Sobrantes", padding=[10, 15])
        
        # Frame temporal para alertas
        self.temp_alertas = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.temp_alertas, text="⚠️ Alertas", padding=[10, 15])
        
        # Frame temporal para reportes
        self.temp_reportes = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.temp_reportes, text="📋 Reportes", padding=[10, 15])
        
        # Agregar mensajes informativos en los frames temporales
        self.add_temp_content()

    def add_temp_content(self):
        """Agrega contenido informativo en los frames temporales"""
        # Mensaje para productos
        tk.Label(
            self.temp_productos,
            text="💡 Haz clic en esta pestaña para cargar el panel de productos",
            font=FONTS['body_medium'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(expand=True, fill='both')
        
        # Mensaje para movimientos
        tk.Label(
            self.temp_movimientos,
            text="💡 Haz clic en esta pestaña para cargar el panel de movimientos",
            font=FONTS['body_medium'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(expand=True, fill='both')
        
        # Mensaje para lotes
        tk.Label(
            self.temp_lotes,
            text="💡 Haz clic en esta pestaña para cargar el panel de lotes FEFO",
            font=FONTS['body_medium'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(expand=True, fill='both')
        
        # Mensaje para bajas
        tk.Label(
            self.temp_bajas,
            text="💡 Haz clic en esta pestaña para cargar el panel de bajas",
            font=FONTS['body_medium'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(expand=True, fill='both')
        
        # Mensaje para sobrantes
        tk.Label(
            self.temp_sobrantes,
            text="💡 Haz clic en esta pestaña para cargar el panel de sobrantes",
            font=FONTS['body_medium'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(expand=True, fill='both')
        
        # Mensaje para alertas
        tk.Label(
            self.temp_alertas,
            text="💡 Haz clic en esta pestaña para cargar el panel de alertas",
            font=FONTS['body_medium'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(expand=True, fill='both')
        
        # Mensaje para reportes
        tk.Label(
            self.temp_reportes,
            text="💡 Haz clic en esta pestaña para cargar el panel de reportes",
            font=FONTS['body_medium'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        ).pack(expand=True, fill='both')

    def create_status_bar(self):
        """Crea la barra de estado inferior"""
        status_frame = tk.Frame(
            self.root, 
            bg=COLORS['surface'],
            height=30,
            relief="solid",
            bd=1,
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        status_frame.pack(fill='x', side='bottom', pady=0)
        status_frame.pack_propagate(False)
        
        # Información de estado
        status_label = tk.Label(
            status_frame, 
            text="Sistema listo | Usuario: Administrador", 
            font=FONTS['caption'], 
            fg=COLORS['text_secondary'], 
            bg=COLORS['surface']
        )
        status_label.pack(side='left', padx=15, pady=5)
        
        # Indicador de estado
        status_indicator = tk.Label(
            status_frame, 
            text="●", 
            font=FONTS['body_medium'], 
            fg=COLORS['success'], 
            bg=COLORS['surface']
        )
        status_indicator.pack(side='right', padx=15, pady=5)

    def setup_events(self):
        """Configura eventos de la aplicación"""
        # Evento de cambio de pestaña
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Evento de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Evento de redimensionamiento
        self.root.bind('<Configure>', self.on_resize)

    def on_tab_changed(self, event):
        """Maneja el cambio de pestañas con carga inteligente"""
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        
        # Actualizar barra de estado
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Pestaña activa: {tab_name}")
        
        # Mostrar indicador de carga si es necesario
        self.show_loading_indicator(tab_name)
        
        # Crear y mostrar paneles según la pestaña seleccionada
        if "Dashboard" in tab_name:
            self.show_dashboard()
        elif "Productos" in tab_name:
            self.show_productos()
        elif "Movimientos" in tab_name:
            self.show_movimientos()
        elif "Bajas" in tab_name:
            self.show_bajas()
        elif "Sobrantes" in tab_name:
            self.show_sobrantes()
        elif "Alertas" in tab_name:
            self.show_alertas()
        elif "Reportes" in tab_name:
            self.show_reportes()
        elif "Lotes FEFO" in tab_name:
            self.show_lotes()

    def on_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        # Aquí se pueden agregar lógicas de redimensionamiento responsivo
        pass

    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        # Aquí se pueden agregar lógicas de limpieza antes de cerrar
        self.root.destroy()

    # Métodos para mostrar cada panel
    def show_dashboard(self):
        """Muestra el panel de dashboard con carga inteligente"""
        panel_name = "Dashboard"
        
        # Si es la primera vez o los datos están desactualizados, cargar
        if panel_name not in self.last_data_update or self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.dashboard_panel, 'cargar_estadisticas'):
                self.dashboard_panel.cargar_estadisticas()
                self.mark_data_updated(panel_name)

    def show_productos(self):
        """Muestra el panel de productos con carga inteligente"""
        panel_name = "Productos"
        
        # Crear panel si no existe
        if self.productos_panel is None:
            # Crear el panel de productos
            self.productos_panel = ProductosPanel(self.notebook)
            
            # Limpiar el frame temporal y agregar el panel real
            for widget in self.temp_productos.winfo_children():
                widget.destroy()
            self.productos_panel.pack(in_=self.temp_productos, fill='both', expand=True)
            
            # Marcar panel como creado
            self.panel_cache[panel_name] = True
            self.mark_data_updated(panel_name)
        
        # Solo recargar datos si es necesario (cada 5 minutos)
        if self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.productos_panel, 'cargar_productos'):
                self.productos_panel.cargar_productos()
                self.mark_data_updated(panel_name)

    def show_movimientos(self):
        """Muestra el panel de movimientos con carga inteligente"""
        panel_name = "Movimientos"
        
        # Crear panel si no existe
        if self.movimientos_panel is None:
            # Crear el panel de movimientos
            self.movimientos_panel = MovimientosPanel(self.notebook)
            
            # Limpiar el frame temporal y agregar el panel real
            for widget in self.temp_movimientos.winfo_children():
                widget.destroy()
            self.movimientos_panel.pack(in_=self.temp_movimientos, fill='both', expand=True)
            
            # Marcar panel como creado
            self.panel_cache[panel_name] = True
            self.mark_data_updated(panel_name)
        
        # Solo recargar datos si es necesario (cada 5 minutos)
        if self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.movimientos_panel, 'cargar_movimientos'):
                self.movimientos_panel.cargar_movimientos()
                self.mark_data_updated(panel_name)

    def show_lotes(self):
        """Muestra el panel de lotes FEFO con carga inteligente"""
        panel_name = "Lotes FEFO"
        
        # Crear panel si no existe
        if self.lotes_panel is None:
            # Crear el panel de lotes
            self.lotes_panel = LotesPanel(self.notebook)
            
            # Limpiar el frame temporal y agregar el panel real
            for widget in self.temp_lotes.winfo_children():
                widget.destroy()
            self.lotes_panel.pack(in_=self.temp_lotes, fill='both', expand=True)
            
            # Marcar panel como creado
            self.panel_cache[panel_name] = True
            self.mark_data_updated(panel_name)
        
        # Solo recargar datos si es necesario (cada 5 minutos)
        if self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.lotes_panel, 'cargar_lotes'):
                self.lotes_panel.cargar_lotes()
                self.mark_data_updated(panel_name)

    def show_bajas(self):
        """Muestra el panel de bajas con carga inteligente"""
        panel_name = "Bajas"
        
        # Crear panel si no existe
        if self.bajas_panel is None:
            # Crear el panel de bajas
            self.bajas_panel = BajasPanel(self.notebook)
            
            # Limpiar el frame temporal y agregar el panel real
            for widget in self.temp_bajas.winfo_children():
                widget.destroy()
            self.bajas_panel.pack(in_=self.temp_bajas, fill='both', expand=True)
            
            # Marcar panel como creado
            self.panel_cache[panel_name] = True
            self.mark_data_updated(panel_name)
        
        # Solo recargar datos si es necesario (cada 5 minutos)
        if self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.bajas_panel, 'cargar_bajas'):
                self.bajas_panel.cargar_bajas()
                self.mark_data_updated(panel_name)

    def show_sobrantes(self):
        """Muestra el panel de sobrantes con carga inteligente"""
        panel_name = "Sobrantes"
        
        # Crear panel si no existe
        if self.sobrantes_panel is None:
            # Crear el panel de sobrantes
            self.sobrantes_panel = SobrantesPanel(self.notebook)
            
            # Limpiar el frame temporal y agregar el panel real
            for widget in self.temp_sobrantes.winfo_children():
                widget.destroy()
            self.sobrantes_panel.pack(in_=self.temp_sobrantes, fill='both', expand=True)
            
            # Marcar panel como creado
            self.panel_cache[panel_name] = True
            self.mark_data_updated(panel_name)
        
        # Solo recargar datos si es necesario (cada 5 minutos)
        if self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.sobrantes_panel, 'cargar_sobrantes'):
                self.sobrantes_panel.cargar_sobrantes()
                self.mark_data_updated(panel_name)

    def show_alertas(self):
        """Muestra el panel de alertas con carga inteligente"""
        panel_name = "Alertas"
        
        # Crear panel si no existe
        if self.alertas_panel is None:
            # Crear el panel de alertas
            self.alertas_panel = AlertasPanel(self.notebook)
            
            # Limpiar el frame temporal y agregar el panel real
            for widget in self.temp_alertas.winfo_children():
                widget.destroy()
            self.alertas_panel.pack(in_=self.temp_alertas, fill='both', expand=True)
            
            # Marcar panel como creado
            self.panel_cache[panel_name] = True
            self.mark_data_updated(panel_name)
        
        # Solo recargar datos si es necesario (cada 5 minutos)
        if self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.alertas_panel, 'cargar_alertas'):
                self.alertas_panel.cargar_alertas()
                self.mark_data_updated(panel_name)

    def show_reportes(self):
        """Muestra el panel de reportes con carga inteligente"""
        panel_name = "Reportes"
        
        # Crear panel si no existe
        if self.reportes_panel is None:
            # Crear el panel de reportes
            self.reportes_panel = ReportesPanel(self.notebook)
            
            # Limpiar el frame temporal y agregar el panel real
            for widget in self.temp_reportes.winfo_children():
                widget.destroy()
            self.reportes_panel.pack(in_=self.temp_reportes, fill='both', expand=True)
            
            # Marcar panel como creado
            self.panel_cache[panel_name] = True
            self.mark_data_updated(panel_name)
        
        # Solo recargar datos si es necesario (cada 5 minutos)
        if self.should_reload_data(panel_name, max_age_minutes=5):
            if hasattr(self.reportes_panel, 'cargar_reportes'):
                self.reportes_panel.cargar_reportes()
                self.mark_data_updated(panel_name)

    def show_loading_indicator(self, tab_name):
        """Muestra un indicador de carga sutil para mejorar la experiencia del usuario"""
        try:
            # Actualizar el texto de la pestaña para mostrar estado de carga
            current_tab = self.notebook.select()
            
            # Solo mostrar indicador si no es la primera vez
            if tab_name in self.panel_cache:
                # Cambiar temporalmente el texto para mostrar que está cargando
                original_text = tab_name
                self.notebook.tab(current_tab, text=f"⏳ {tab_name}")
                
                # Restaurar el texto original después de un breve delay
                self.root.after(500, lambda: self.restore_tab_text(current_tab, original_text))
                
        except Exception as e:
            print(f"Error mostrando indicador de carga: {e}")

    def restore_tab_text(self, tab_id, original_text):
        """Restaura el texto original de la pestaña"""
        try:
            self.notebook.tab(tab_id, text=original_text)
        except Exception as e:
            print(f"Error restaurando texto de pestaña: {e}")

    def should_reload_data(self, panel_name, max_age_minutes=5):
        """Determina si los datos del panel deben recargarse"""
        try:
            if panel_name not in self.last_data_update:
                return True
            
            import time
            current_time = time.time()
            last_update = self.last_data_update[panel_name]
            
            # Recargar si han pasado más de max_age_minutes
            return (current_time - last_update) > (max_age_minutes * 60)
            
        except Exception as e:
            print(f"Error verificando si recargar datos: {e}")
            return True

    def mark_data_updated(self, panel_name):
        """Marca que los datos del panel han sido actualizados"""
        try:
            import time
            self.last_data_update[panel_name] = time.time()
        except Exception as e:
            print(f"Error marcando datos como actualizados: {e}")

    def force_reload_panel(self, panel_name):
        """Fuerza la recarga de datos de un panel específico"""
        try:
            # Limpiar timestamp de última actualización para forzar recarga
            if panel_name in self.last_data_update:
                del self.last_data_update[panel_name]
            
            # Recargar panel según el nombre
            if "Productos" in panel_name:
                self.show_productos()
            elif "Movimientos" in panel_name:
                self.show_movimientos()
            elif "Lotes FEFO" in panel_name:
                self.show_lotes()
            elif "Bajas" in panel_name:
                self.show_bajas()
            elif "Sobrantes" in panel_name:
                self.show_sobrantes()
            elif "Alertas" in panel_name:
                self.show_alertas()
            elif "Reportes" in panel_name:
                self.show_reportes()
            elif "Dashboard" in panel_name:
                self.show_dashboard()
                
        except Exception as e:
            print(f"Error forzando recarga del panel {panel_name}: {e}")

    def clear_all_cache(self):
        """Limpia todo el cache de datos"""
        try:
            self.data_cache.clear()
            self.last_data_update.clear()
            print("Cache de datos limpiado")
        except Exception as e:
            print(f"Error limpiando cache: {e}")

    def get_cache_status(self):
        """Obtiene el estado del cache para debugging"""
        try:
            import time
            current_time = time.time()
            status = {}
            
            for panel_name, last_update in self.last_data_update.items():
                age_minutes = (current_time - last_update) / 60
                status[panel_name] = {
                    'last_update': last_update,
                    'age_minutes': round(age_minutes, 2),
                    'needs_reload': age_minutes > 5
                }
            
            return status
        except Exception as e:
            print(f"Error obteniendo estado del cache: {e}")
            return {}

    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


def run_app():
    """Función principal para ejecutar la aplicación"""
    app = MainWindow()
    app.run()
