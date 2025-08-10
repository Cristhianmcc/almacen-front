import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import COLORS, FONTS, SPACING, DIMENSIONS

from ui.dashboard_panel import DashboardPanel
from ui.productos_panel import ProductosPanel
from ui.movimientos_panel import MovimientosPanel
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
        
        # Configurar estilo global
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Configurar eventos
        self.setup_events()
        
        # Cargar dashboard por defecto
        self.show_dashboard()

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
        """Crea todos los paneles de la aplicación"""
        # Panel de Dashboard
        self.dashboard_panel = DashboardPanel(self.notebook)
        self.notebook.add(
            self.dashboard_panel, 
            text="📊 Dashboard", 
            padding=[10, 15]
        )
        
        # Panel de Productos
        self.productos_panel = ProductosPanel(self.notebook)
        self.notebook.add(
            self.productos_panel, 
            text="📦 Productos", 
            padding=[10, 15]
        )
        
        # Panel de Movimientos
        self.movimientos_panel = MovimientosPanel(self.notebook)
        self.notebook.add(
            self.movimientos_panel, 
            text="🔄 Movimientos", 
            padding=[10, 15]
        )
        
        # Panel de Bajas
        self.bajas_panel = BajasPanel(self.notebook)
        self.notebook.add(
            self.bajas_panel, 
            text="🗑️ Bajas", 
            padding=[10, 15]
        )
        
        # Panel de Sobrantes
        self.sobrantes_panel = SobrantesPanel(self.notebook)
        self.notebook.add(
            self.sobrantes_panel, 
            text="➕ Sobrantes", 
            padding=[10, 15]
        )
        
        # Panel de Alertas
        self.alertas_panel = AlertasPanel(self.notebook)
        self.notebook.add(
            self.alertas_panel, 
            text="⚠️ Alertas", 
            padding=[10, 15]
        )
        
        # Panel de Reportes
        self.reportes_panel = ReportesPanel(self.notebook)
        self.notebook.add(
            self.reportes_panel, 
            text="📋 Reportes", 
            padding=[10, 15]
        )

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
        """Maneja el cambio de pestañas"""
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        
        # Actualizar barra de estado
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Pestaña activa: {tab_name}")
        
        # Cargar datos específicos según la pestaña
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
        """Muestra el panel de dashboard"""
        if hasattr(self.dashboard_panel, 'cargar_estadisticas'):
            self.dashboard_panel.cargar_estadisticas()

    def show_productos(self):
        """Muestra el panel de productos"""
        if hasattr(self.productos_panel, 'cargar_productos'):
            self.productos_panel.cargar_productos()

    def show_movimientos(self):
        """Muestra el panel de movimientos"""
        if hasattr(self.movimientos_panel, 'cargar_movimientos'):
            self.movimientos_panel.cargar_movimientos()

    def show_bajas(self):
        """Muestra el panel de bajas"""
        if hasattr(self.bajas_panel, 'cargar_bajas'):
            self.bajas_panel.cargar_bajas()

    def show_sobrantes(self):
        """Muestra el panel de sobrantes"""
        if hasattr(self.sobrantes_panel, 'cargar_sobrantes'):
            self.sobrantes_panel.cargar_sobrantes()

    def show_alertas(self):
        """Muestra el panel de alertas"""
        if hasattr(self.alertas_panel, 'cargar_alertas'):
            self.alertas_panel.cargar_alertas()

    def show_reportes(self):
        """Muestra el panel de reportes"""
        if hasattr(self.reportes_panel, 'cargar_reportes'):
            self.reportes_panel.cargar_reportes()

    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


def run_app():
    """Función principal para ejecutar la aplicación"""
    app = MainWindow()
    app.run()
