import tkinter as tk
from tkinter import ttk
from services.api import get
from ui.styles import COLORS, FONTS, SPACING, DIMENSIONS

class DashboardPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_estadisticas()

    def create_widgets(self):
        # Configurar el frame principal
        self.configure(style='TFrame')
        
        # Título principal con mejor diseño - más compacto
        self.lbl_title = tk.Label(
            self, 
            text="Estadísticas Generales", 
            font=FONTS['title_large'], 
            background=COLORS['background'], 
            foreground=COLORS['primary']
        )
        self.lbl_title.pack(pady=(SPACING['lg'], SPACING['md']), anchor='center', fill='x')
        
        self.stats = {}
        
        # Frame principal para las estadísticas con mejor layout - más compacto
        stats_frame = tk.Frame(self, bg=COLORS['background'])
        stats_frame.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['sm'])
        
        # Configurar grid para mejor distribución y responsividad
        stats_frame.columnconfigure((0, 1, 2), weight=1, uniform='col')
        stats_frame.rowconfigure((0, 1), weight=1, uniform='row')
        
        # Información de las tarjetas con colores más profesionales
        cards_info = [
            {
                "campo": "Total Productos", 
                "color": COLORS['primary'], 
                "icon": "📦", 
                "desc": "Productos activos en inventario"
            },
            {
                "campo": "Total Movimientos", 
                "color": COLORS['success'], 
                "icon": "🔄", 
                "desc": "Entradas y salidas registradas"
            },
            {
                "campo": "Total Bajas", 
                "color": COLORS['warning'], 
                "icon": "🗑️", 
                "desc": "Productos dados de baja"
            },
            {
                "campo": "Total Sobrantes", 
                "color": COLORS['accent'], 
                "icon": "➕", 
                "desc": "Sobrantes en almacén"
            },
            {
                "campo": "Total Alertas", 
                "color": COLORS['danger'], 
                "icon": "⚠️", 
                "desc": "Alertas activas"
            },
        ]
        
        self.card_widgets = []
        
        for i, info in enumerate(cards_info):
            row = i // 3
            col = i % 3
            
            # Crear tarjeta con mejor diseño y sombras - más compacta
            card = tk.Frame(
                stats_frame, 
                bg=COLORS['surface'], 
                bd=0, 
                highlightbackground=info["color"], 
                highlightthickness=2,
                relief="flat"
            )
            card.grid(row=row, column=col, padx=SPACING['sm'], pady=SPACING['sm'], sticky='nsew')
            
            # Configurar grid interno de la tarjeta para expansión
            card.columnconfigure(0, weight=1)
            card.rowconfigure(1, weight=1)
            
            # Icono con mejor tamaño y espaciado - más pequeño
            icon_lbl = tk.Label(
                card, 
                text=info["icon"], 
                font=("Segoe UI Emoji", 36), 
                bg=COLORS['surface']
            )
            icon_lbl.grid(row=0, column=0, pady=(SPACING['md'], SPACING['xs']))
            
            # Frame para el contenido de la tarjeta
            content_frame = tk.Frame(card, bg=COLORS['surface'])
            content_frame.grid(row=1, column=0, sticky='nsew', padx=SPACING['sm'])
            
            # Configurar grid interno del content_frame
            content_frame.columnconfigure(0, weight=1)
            content_frame.rowconfigure(1, weight=1)
            content_frame.rowconfigure(2, weight=1)
            content_frame.rowconfigure(3, weight=1)
            
            # Valor grande con mejor tipografía - más compacto
            self.stats[info["campo"]] = tk.Label(
                content_frame, 
                text="-", 
                font=FONTS['title_medium'], 
                bg=COLORS['surface'], 
                fg=info["color"], 
                justify="center"
            )
            self.stats[info["campo"]].grid(row=1, column=0, pady=(0, SPACING['xs']), sticky='ew')
            
            # Título con mejor diseño - más compacto
            title_label = tk.Label(
                content_frame, 
                text=info["campo"], 
                font=FONTS['heading_small'], 
                bg=COLORS['surface'], 
                fg=info["color"], 
                justify="center"
            )
            title_label.grid(row=2, column=0, pady=(0, SPACING['xs']), sticky='ew')
            
            # Descripción con mejor tipografía - más compacta
            desc_label = tk.Label(
                content_frame, 
                text=info["desc"], 
                font=FONTS['body_small'], 
                bg=COLORS['surface'], 
                fg=COLORS['text_secondary'], 
                justify="center",
                wraplength=250
            )
            desc_label.grid(row=3, column=0, pady=(0, SPACING['sm']), sticky='ew')
            
            self.card_widgets.append(card)

    def cargar_estadisticas(self):
        try:
            productos = get("/products").data or []
            productos_activos = [p for p in productos if p.get("estado") != "baja"]
            movimientos = get("/movements").data or []
            bajas = get("/withdrawals").data or []
            sobrantes = get("/surplus").data or []
            alertas = get("/alerts").data or []
            self.stats["Total Productos"].config(text=f"Total Productos: {len(productos_activos)}")
            self.stats["Total Movimientos"].config(text=f"Total Movimientos: {len(movimientos)}")
            self.stats["Total Bajas"].config(text=f"Total Bajas: {len(bajas)}")
            self.stats["Total Sobrantes"].config(text=f"Total Sobrantes: {len(sobrantes)}")
            self.stats["Total Alertas"].config(text=f"Total Alertas: {len(alertas)}")
        except Exception as e:
            for campo in self.stats:
                self.stats[campo].config(text=f"Error: {e}")
    
    def cargar_dashboard(self):
        self.cargar_estadisticas()
