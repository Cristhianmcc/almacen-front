import tkinter as tk
from tkinter import ttk
from services.api import get

class DashboardPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.cargar_estadisticas()

    def create_widgets(self):
        self.configure(style='TFrame')
        self.lbl_title = ttk.Label(self, text="Estadísticas Generales", font=("Segoe UI", 28, "bold"), background="#f7f7f7", foreground="#1565c0")
        self.lbl_title.pack(pady=30)
        self.stats = {}
        stats_frame = tk.Frame(self, bg="#f7f7f7")
        stats_frame.pack(fill='both', expand=True, pady=10)
        cards_info = [
            {"campo": "Total Productos", "color": "#1976d2", "icon": "📦", "desc": "Productos activos en inventario"},
            {"campo": "Total Movimientos", "color": "#43a047", "icon": "🔄", "desc": "Entradas y salidas registradas"},
            {"campo": "Total Bajas", "color": "#ff7043", "icon": "🗑️", "desc": "Productos dados de baja"},
            {"campo": "Total Sobrantes", "color": "#ab47bc", "icon": "➕", "desc": "Sobrantes en almacén"},
            {"campo": "Total Alertas", "color": "#d32f2f", "icon": "⚠️", "desc": "Alertas activas"},
        ]
        max_cards_per_row = 3
        card_min_width = 260
        card_max_width = 340
        card_height = 200
        self.card_widgets = []
        for i, info in enumerate(cards_info):
            row = i // max_cards_per_row
            col = i % max_cards_per_row
            card = tk.Frame(stats_frame, bg="#fff", bd=0, highlightbackground=info["color"], highlightthickness=3, width=card_max_width, height=card_height)
            card.grid(row=row, column=col, padx=18, pady=12, sticky="nsew")
            stats_frame.grid_columnconfigure(col, weight=1, minsize=card_min_width)
            card.grid_propagate(0)
            # Icono
            icon_lbl = tk.Label(card, text=info["icon"], font=("Segoe UI Emoji", 36), bg="#fff")
            icon_lbl.pack(pady=(18,0))
            # Valor grande (fuente más pequeña si el texto es largo)
            self.stats[info["campo"]] = tk.Label(card, text="-", font=("Segoe UI", 22, "bold"), bg="#fff", fg=info["color"], wraplength=card_max_width-24, justify="center")
            self.stats[info["campo"]].pack(pady=(0,0))
            # Título
            tk.Label(card, text=info["campo"], font=("Segoe UI", 13, "bold"), bg="#fff", fg=info["color"], wraplength=card_max_width-24, justify="center").pack()
            # Descripción
            tk.Label(card, text=info["desc"], font=("Segoe UI", 10), bg="#fff", fg="#888", wraplength=card_max_width-24, justify="center").pack(pady=(0,12))
            self.card_widgets.append(card)

    def cargar_estadisticas(self):
        try:
            productos = get("/products").data or []
            movimientos = get("/movements").data or []
            bajas = get("/withdrawals").data or []
            sobrantes = get("/surplus").data or []
            alertas = get("/alerts").data or []
            self.stats["Total Productos"].config(text=f"Total Productos: {len(productos)}")
            self.stats["Total Movimientos"].config(text=f"Total Movimientos: {len(movimientos)}")
            self.stats["Total Bajas"].config(text=f"Total Bajas: {len(bajas)}")
            self.stats["Total Sobrantes"].config(text=f"Total Sobrantes: {len(sobrantes)}")
            self.stats["Total Alertas"].config(text=f"Total Alertas: {len(alertas)}")
        except Exception as e:
            for campo in self.stats:
                self.stats[campo].config(text=f"Error: {e}")
