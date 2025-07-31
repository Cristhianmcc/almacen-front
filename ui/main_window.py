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
    # Hacer la ventana responsiva
    root.geometry("1200x750")
    root.minsize(900, 600)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Tema visual profesional y responsivo
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', background='#f7f7f7', foreground='#222', font=("Segoe UI", 11))
    style.configure('TNotebook', background='#e9ecef', borderwidth=0)
    style.configure('TNotebook.Tab', background='#e9ecef', foreground='#222', padding=10, font=("Segoe UI", 12, "bold"))
    style.map('TNotebook.Tab', background=[('selected', '#ffffff')])
    style.configure('TFrame', background='#f7f7f7')
    style.configure('TLabel', background='#f7f7f7', foreground='#222', font=("Segoe UI", 12))
    style.configure('TButton', background='#1976d2', foreground='#fff', font=("Segoe UI", 11, "bold"), borderwidth=0, padding=8)
    style.map('TButton', background=[('active', '#1565c0')], foreground=[('active', '#fff')])
    style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', foreground='#222', rowheight=32, font=("Segoe UI", 12))
    style.configure('Treeview.Heading', background='#1976d2', foreground='#fff', font=("Segoe UI", 13, "bold"))
    style.map('Treeview', background=[('selected', '#e3f2fd')], foreground=[('selected', '#111')])

    # Menú superior
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    archivo_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Archivo", menu=archivo_menu)
    archivo_menu.add_command(label="Salir", command=root.quit)

    # Menú superior
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    archivo_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Archivo", menu=archivo_menu)
    archivo_menu.add_command(label="Salir", command=root.quit)



    # Barra de navegación moderna y responsiva
    nav_frame = tk.Frame(root, bg="#fff")
    nav_frame.pack(fill='x', side='top')
    # Frame principal para los paneles
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True)
    main_frame.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
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
            frame.grid_remove()
        tab_frames[tab_name].grid(row=0, column=0, sticky="nsew")
        active_tab.set(tab_name)
        for btn in nav_frame.winfo_children():
            if getattr(btn, 'tab_name', None) == tab_name:
                btn.configure(bg="#1976d2", fg="#fff", font=("Segoe UI", 12, "bold"))
            else:
                btn.configure(bg="#fff", fg="#1976d2", font=("Segoe UI", 12, "bold"))
    nav_btns = []
    for name, var in nav_tabs:
        btn = tk.Button(nav_frame, text=name, bd=0, relief="flat", padx=18, pady=8, bg="#fff", fg="#1976d2", font=("Segoe UI", 12, "bold"), activebackground="#e3f2fd", activeforeground="#1976d2", cursor="hand2", highlightthickness=0, highlightbackground="#fff")
        btn.tab_name = name
        btn.pack(side='left', padx=(0, 2), pady=0)
        btn.configure(command=lambda n=name: switch_tab(n))
        nav_btns.append(btn)
    # Botón Actualizar general al costado de Reportes
    def actualizar_todo():
        # Llama a cargar_movimientos y métodos de refresco de cada panel si existen
        try:
            if hasattr(tab_frames["Movimientos"], 'children'):
                for w in tab_frames["Movimientos"].winfo_children():
                    if hasattr(w, 'cargar_movimientos'):
                        w.cargar_movimientos()
            if hasattr(tab_frames["Productos"], 'children'):
                for w in tab_frames["Productos"].winfo_children():
                    if hasattr(w, 'cargar_productos'):
                        w.cargar_productos()
            if hasattr(tab_frames["Alertas"], 'children'):
                for w in tab_frames["Alertas"].winfo_children():
                    if hasattr(w, 'cargar_alertas'):
                        w.cargar_alertas()
            if hasattr(tab_frames["Bajas"], 'children'):
                for w in tab_frames["Bajas"].winfo_children():
                    if hasattr(w, 'cargar_bajas'):
                        w.cargar_bajas()
            if hasattr(tab_frames["Sobrantes"], 'children'):
                for w in tab_frames["Sobrantes"].winfo_children():
                    if hasattr(w, 'cargar_sobrantes'):
                        w.cargar_sobrantes()
            if hasattr(tab_frames["Reportes"], 'children'):
                for w in tab_frames["Reportes"].winfo_children():
                    if hasattr(w, 'cargar_reportes'):
                        w.cargar_reportes()
            if hasattr(tab_frames["Dashboard"], 'children'):
                for w in tab_frames["Dashboard"].winfo_children():
                    if hasattr(w, 'cargar_dashboard'):
                        w.cargar_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")
    # Botón Actualizar general destacado
    # Botón Actualizar general con ícono y diseño especial
    actualizar_btn = tk.Button(
        nav_frame,
        text="🔄 Actualizar",
        bd=0,
        relief="groove",
        padx=20,
        pady=8,
        bg="#ff9800",
        fg="#fff",
        font=("Segoe UI", 13, "bold"),
        activebackground="#fb8c00",
        activeforeground="#fff",
        cursor="hand2",
        highlightthickness=3,
        highlightbackground="#fff3e0",
        highlightcolor="#fff3e0",
        command=actualizar_todo
    )
    actualizar_btn.pack(side='left', padx=(24, 0), pady=0)
    # Crear frames para cada panel y hacerlos responsivos dentro de main_frame
    for tab in ["Dashboard", "Productos", "Movimientos", "Alertas", "Bajas", "Sobrantes", "Reportes"]:
        frame = ttk.Frame(main_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_remove()
        tab_frames[tab] = frame
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
