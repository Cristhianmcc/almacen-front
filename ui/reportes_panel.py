import tkinter as tk
from tkinter import ttk, messagebox
from services.api import get

class ReportesPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#ab47bc")
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Reportes", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#ab47bc").pack(anchor='center', pady=18)
        self.configure(style='TFrame')
        btn_frame = tk.Frame(self, bg="#f7f7f7")
        btn_frame.pack(fill='x', pady=10)
        btn_style = {"fg": "#fff", "font": ("Segoe UI", 12, "bold"), "relief": "flat", "padx": 14, "pady": 6}
        tk.Button(btn_frame, text="Reporte Inventario", command=self.reporte_inventario, bg="#1976d2", activebackground="#1565c0", **btn_style).pack(side='left', padx=8, pady=4)
        tk.Button(btn_frame, text="Reporte Movimientos", command=self.reporte_movimientos, bg="#43a047", activebackground="#388e3c", **btn_style).pack(side='left', padx=8, pady=4)
        tk.Button(btn_frame, text="Reporte SIGA", command=self.reporte_siga, bg="#ab47bc", activebackground="#8e24aa", **btn_style).pack(side='left', padx=8, pady=4)

        result_frame = tk.Frame(self, bg="#f7f7f7", bd=1, relief="flat")
        result_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.txt_result = tk.Text(result_frame, height=20, bg="#ffffff", fg="#222", font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.txt_result.pack(fill='both', expand=True, padx=10, pady=10)

    def reporte_inventario(self):
        self.mostrar_reporte("/reports/inventory")

    def reporte_movimientos(self):
        self.mostrar_reporte("/reports/movements")

    def reporte_siga(self):
        self.mostrar_reporte("/reports/siga")

    def mostrar_reporte(self, endpoint):
        try:
            response = get(endpoint)
            self.txt_result.delete(1.0, tk.END)
            if not response.success:
                self.txt_result.insert(tk.END, f"Error: {response.message}")
            else:
                data = response.data
                if isinstance(data, list):
                    for item in data:
                        self.txt_result.insert(tk.END, f"- {item}\n")
                elif isinstance(data, dict):
                    for k, v in data.items():
                        self.txt_result.insert(tk.END, f"{k}: {v}\n")
                else:
                    self.txt_result.insert(tk.END, str(data))
        except Exception as e:
            messagebox.showerror("Error", str(e))
