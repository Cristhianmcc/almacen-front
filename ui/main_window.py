import tkinter as tk
from tkinter import ttk, messagebox


from ui.dashboard_panel import DashboardPanel
from ui.productos_panel import ProductosPanel
from ui.movimientos_panel import MovimientosPanel
from ui.alertas_panel import AlertasPanel
from ui.bajas_panel import BajasPanel
from ui.sobrantes_panel import SobrantesPanel
from ui.reportes_panel import ReportesPanel


def run_app():
    root = tk.Tk()
    root.title("Sistema de Almacén - Instituto Lurín")
    root.geometry("1100x700")

    # Tema visual claro
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', background='#f7f7f7', foreground='#222', font=("Segoe UI", 11))
    style.configure('TNotebook', background='#e9ecef', borderwidth=0)
    style.configure('TNotebook.Tab', background='#e9ecef', foreground='#222', padding=10)
    style.map('TNotebook.Tab', background=[('selected', '#ffffff')])
    style.configure('TFrame', background='#f7f7f7')
    style.configure('TLabel', background='#f7f7f7', foreground='#222')
    style.configure('TButton', background='#e9ecef', foreground='#222')
    style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', foreground='#222', rowheight=28)
    style.map('Treeview', background=[('selected', '#cce5ff')])

    # Menú superior
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    archivo_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Archivo", menu=archivo_menu)
    archivo_menu.add_command(label="Salir", command=root.quit)



    # Barra de navegación moderna
    nav_frame = tk.Frame(root, bg="#fff")
    nav_frame.pack(fill='x', side='top')
    nav_tabs = [
        ("Dashboard", "dashboard_tab"),
        ("Productos", "productos_tab"),
        ("Movimientos", "movimientos_tab"),
        ("Alertas", "alertas_tab"),
        ("Bajas", "bajas_tab"),
        ("Sobrantes", "sobrantes_tab"),
        ("Reportes", "reportes_tab")
    ]
    tab_frames = {}
    active_tab = tk.StringVar(value="Dashboard")
    def switch_tab(tab_name):
        for name, frame in tab_frames.items():
            frame.pack_forget()
        tab_frames[tab_name].pack(fill='both', expand=True)
        active_tab.set(tab_name)
        for btn in nav_frame.winfo_children():
            if getattr(btn, 'tab_name', None) == tab_name:
                btn.configure(bg="#1976d2", fg="#fff", font=("Segoe UI", 11, "bold"))
            else:
                btn.configure(bg="#fff", fg="#1976d2", font=("Segoe UI", 11, "bold"))
    for name, var in nav_tabs:
        btn = tk.Button(nav_frame, text=name, bd=0, relief="flat", padx=18, pady=8, bg="#fff", fg="#1976d2", font=("Segoe UI", 11, "bold"), activebackground="#e3f2fd", activeforeground="#1976d2", cursor="hand2", highlightthickness=0, highlightbackground="#fff")
        btn.tab_name = name
        btn.pack(side='left', padx=(0, 2), pady=0)
        btn.configure(command=lambda n=name: switch_tab(n))
    # Crear frames para cada panel
    tab_frames["Dashboard"] = ttk.Frame(root)
    tab_frames["Productos"] = ttk.Frame(root)
    tab_frames["Movimientos"] = ttk.Frame(root)
    tab_frames["Alertas"] = ttk.Frame(root)
    tab_frames["Bajas"] = ttk.Frame(root)
    tab_frames["Sobrantes"] = ttk.Frame(root)
    tab_frames["Reportes"] = ttk.Frame(root)
    # Inicializar paneles dentro de cada frame
    from ui.dashboard_panel import DashboardPanel
    from ui.productos_panel import ProductosPanel
    from ui.movimientos_panel import MovimientosPanel
    from ui.alertas_panel import AlertasPanel
    from ui.bajas_panel import BajasPanel
    from ui.sobrantes_panel import SobrantesPanel
    from ui.reportes_panel import ReportesPanel

    DashboardPanel(tab_frames["Dashboard"])
    ProductosPanel(tab_frames["Productos"])
    MovimientosPanel(tab_frames["Movimientos"])
    AlertasPanel(tab_frames["Alertas"])
    BajasPanel(tab_frames["Bajas"])
    SobrantesPanel(tab_frames["Sobrantes"])
    ReportesPanel(tab_frames["Reportes"])
    # Mostrar el tab inicial
    switch_tab("Dashboard")
    root.mainloop()
