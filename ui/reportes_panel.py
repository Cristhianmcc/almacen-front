import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        # tk.Button(btn_frame, text="Reporte SIGA", command=self.reporte_siga, bg="#ab47bc", activebackground="#8e24aa", **btn_style).pack(side='left', padx=8, pady=4)

        export_frame = tk.Frame(self, bg="#f7f7f7")
        export_frame.pack(fill='x', pady=(0, 0))
        tk.Button(export_frame, text="Exportar PDF", command=self.exportar_pdf, bg="#d32f2f", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#b71c1c").pack(side='left', padx=8)
        tk.Button(export_frame, text="Exportar Excel", command=self.exportar_excel, bg="#1976d2", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#1565c0").pack(side='left', padx=8)
        tk.Button(export_frame, text="Imprimir", command=self.imprimir_reporte, bg="#43a047", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=4, activebackground="#388e3c").pack(side='left', padx=8)

        self.result_frame = tk.Frame(self, bg="#f7f7f7", bd=1, relief="flat")
        self.result_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.txt_result = tk.Text(self.result_frame, height=20, bg="#ffffff", fg="#222", font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.txt_result.pack(fill='both', expand=True, padx=10, pady=10)
        self.tree_result = None

    def reporte_inventario(self):
        self.mostrar_reporte("/reports/inventory")

    def reporte_movimientos(self):
        self.mostrar_reporte("/reports/movements")

    # def reporte_siga(self):
    #     self.mostrar_reporte("/reports/siga")

    def mostrar_reporte(self, endpoint):
        try:
            response = get(endpoint)
            self.txt_result.pack_forget()
            if self.tree_result:
                self.tree_result.destroy()
                self.tree_result = None
            if not response.success:
                self.txt_result.pack(fill='both', expand=True, padx=10, pady=10)
                self.txt_result.delete(1.0, tk.END)
                self.txt_result.insert(tk.END, f"Error: {response.message}")
                self.current_table_data = []
                self.current_table_columns = []
                return
            data = response.data
            # Buscar lista de dicts (movimientos, productos, etc)
            items = None
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        items = v
                        break
            elif isinstance(data, list) and data and isinstance(data[0], dict):
                items = data
            if items:
                # Detecta si es reporte de movimientos
                if endpoint == '/reports/movements':
                    columns = ['Codigo Producto', 'Nombre', 'Tipo', 'Fecha', 'Cantidad', 'Stock anterior', 'Stock posterior']
                    display_data = []
                    for row in items:
                        new_row = {}
                        # Extrae datos del producto
                        if 'producto' in row and isinstance(row['producto'], dict):
                            new_row['Codigo Producto'] = row['producto'].get('codigo', '')
                            new_row['Nombre'] = row['producto'].get('nombre', '')
                        else:
                            new_row['Codigo Producto'] = row.get('producto', '')
                            new_row['Nombre'] = ''
                        # Resto de columnas
                        new_row['Tipo'] = row.get('tipo', '')
                        new_row['Fecha'] = row.get('fecha', '')
                        new_row['Cantidad'] = row.get('cantidad', '')
                        new_row['Stock anterior'] = row.get('stock_anterior', '')
                        new_row['Stock posterior'] = row.get('stock_posterior', '')
                        display_data.append(new_row)
                    self.current_table_data = display_data
                    self.current_table_columns = columns
                else:
                    # Para inventario y otros reportes, columnas dinámicas como antes
                    columns = list(items[0].keys())
                    display_data = []
                    for row in items:
                        new_row = row.copy()
                        if 'producto' in new_row and isinstance(new_row['producto'], dict):
                            nombre = new_row['producto'].get('nombre', '')
                            new_row['producto'] = nombre
                        display_data.append(new_row)
                    self.current_table_data = display_data
                    self.current_table_columns = columns
                self.tree_result = ttk.Treeview(self.result_frame, columns=columns, show='headings', style="Treeview")
                for col in columns:
                    self.tree_result.heading(col, text=col.replace('_', ' ').capitalize())
                    self.tree_result.column(col, width=120)
                for row in display_data:
                    self.tree_result.insert('', 'end', values=[row.get(col, '') for col in columns])
                self.tree_result.pack(fill='both', expand=True, padx=10, pady=10)
            else:
                self.txt_result.pack(fill='both', expand=True, padx=10, pady=10)
                self.txt_result.delete(1.0, tk.END)
                self.txt_result.insert(tk.END, "No hay datos tabulares para mostrar.")
                self.current_table_data = []
                self.current_table_columns = []
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def exportar_pdf(self):
        try:
            import pandas as pd
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import landscape, letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.pdfbase import pdfmetrics
            import os
            # Usar solo la fuente local DejaVuSans.ttf en ui/
            font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
            font_ok = False
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path))
                    font_ok = True
                except Exception:
                    font_ok = False
            else:
                font_ok = False
            if not hasattr(self, 'current_table_data') or not self.current_table_data:
                messagebox.showwarning("Exportar PDF", "No hay datos para exportar.")
                return
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Guardar reporte como PDF"
            )
            if not file_path:
                return
            messagebox.showinfo("Ruta de guardado", f"El PDF se guardará en:\n{file_path}")
            import unicodedata
            def normalize_text(text):
                if text is None:
                    return ''
                if not isinstance(text, str):
                    text = str(text)
                # Normaliza y fuerza encoding utf-8, reemplazando explícitamente 'ó' y 'í' si se pierden
                text = unicodedata.normalize('NFKC', text)
                # Si por alguna razón la 'ó' o 'í' se pierden, las reponemos
                text = text.replace('\u00f3', 'ó').replace('Ã³', 'ó').replace('Ã­', 'í').replace('\u00ed', 'í')
                try:
                    text = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
                except:
                    pass
                return text
            def clean_row(row):
                # Oculta las columnas problemáticas
                return {k: normalize_text(v) for k, v in row.items() if k.lower() not in ['usuario', 'observaciones', 'observacion']}
            df = pd.DataFrame([clean_row(row) for row in self.current_table_data])
            # Landscape y ancho dinámico
            page_size = landscape(letter)
            total_width = page_size[0] - 60  # margen
            num_cols = len(df.columns)
            max_col_width = min(180, total_width // num_cols)
            col_widths = [max_col_width for _ in df.columns]
            styles = getSampleStyleSheet()
            # Usar fuente DejaVuSans si está disponible, si no Helvetica
            cell_font = 'DejaVuSans' if font_ok else 'Helvetica'
            header_font = 'DejaVuSans-Bold' if font_ok else 'Helvetica-Bold'
            if not font_ok:
                messagebox.showwarning(
                    "Exportar PDF",
                    "No se encontró la fuente DejaVuSans.ttf en la carpeta ui/.\nDescárgala desde:\nhttps://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf\ny colócala en: " + font_path + "\nSe usará una fuente estándar. Los caracteres especiales pueden no verse correctamente."
                )
            cell_style = ParagraphStyle('cell', fontName=cell_font, fontSize=9, leading=11, alignment=0)
            title = Paragraph("<b>Reporte de datos</b>", ParagraphStyle('title', fontName=header_font, fontSize=14, alignment=1))
            # Convertir cada celda en Paragraph para permitir salto de línea y codificación correcta
            data = [[Paragraph(str(col), ParagraphStyle('header', fontName=header_font, fontSize=10, alignment=1, textColor=colors.whitesmoke)) for col in df.columns]]
            for row in df.values.tolist():
                data.append([Paragraph(str(cell), cell_style) for cell in row])
            table = Table(data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#757575')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,0), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), header_font),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f9f7e3')),
                ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
                ('ALIGN', (0,1), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,1), (-1,-1), cell_font),
                ('FONTSIZE', (0,1), (-1,-1), 9),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ]))
            doc = SimpleDocTemplate(file_path, pagesize=page_size, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=18)
            elements = [title, Spacer(1, 12), table]
            doc.build(elements)
            messagebox.showinfo("Exportar PDF", f"PDF generado: {file_path}")
        except Exception as e:
            messagebox.showerror("Exportar PDF", str(e))

    def exportar_excel(self):
        try:
            import pandas as pd
            import unicodedata
            from openpyxl import load_workbook
            from openpyxl.utils import get_column_letter
            from openpyxl.worksheet.page import PageMargins
            from openpyxl.styles import Font
            if not hasattr(self, 'current_table_data') or not self.current_table_data:
                messagebox.showwarning("Exportar Excel", "No hay datos para exportar.")
                return
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar reporte como Excel"
            )
            if not file_path:
                return
            messagebox.showinfo("Ruta de guardado", f"El Excel se guardará en:\n{file_path}")
            # Solo normalizar texto, no reemplazar ni eliminar caracteres especiales
            def normalize_text(text):
                if text is None:
                    return ''
                if not isinstance(text, str):
                    text = str(text)
                return unicodedata.normalize('NFKC', text)
            df = pd.DataFrame([{k: normalize_text(v) for k, v in row.items() if k.lower() not in ['usuario', 'observaciones', 'observacion']} for row in self.current_table_data])
            df.to_excel(file_path, index=False, engine='openpyxl')
            # Ajustar ancho de columnas, fuente y configuración de impresión
            try:
                wb = load_workbook(file_path)
                ws = wb.active
                try:
                    font = Font(name='Arial Unicode MS', size=8)
                except:
                    font = Font(name='Arial', size=8)
                for row in ws.iter_rows():
                    for cell in row:
                        cell.font = font
                for col in ws.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col:
                        try:
                            if cell.value:
                                max_length = max(max_length, len(str(cell.value)))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    ws.column_dimensions[column].width = adjusted_width
                ws.page_setup.orientation = 'landscape'
                ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
                ws.page_setup.fitToWidth = 1
                ws.page_setup.fitToHeight = 1
                max_col = ws.max_column
                max_row = ws.max_row
                ws.print_area = f"A1:{get_column_letter(max_col)}{max_row}"
                ws.page_margins = PageMargins(left=0.3, right=0.3, top=0.5, bottom=0.5)
                wb.save(file_path)
            except Exception:
                pass
            messagebox.showinfo("Exportar Excel", f"Excel generado: {file_path}")
        except ImportError:
            messagebox.showerror("Exportar Excel", "Falta el módulo 'openpyxl'. Instala con: pip install openpyxl")
        except Exception as e:
            messagebox.showerror("Exportar Excel", str(e))

    def imprimir_reporte(self):
        try:
            import pandas as pd
            if not hasattr(self, 'current_table_data') or not self.current_table_data:
                messagebox.showwarning("Imprimir", "No hay datos para imprimir.")
                return
            # Oculta las columnas problemáticas en la previsualización
            import unicodedata
            def normalize_text(text):
                if text is None:
                    return ''
                if not isinstance(text, str):
                    text = str(text)
                return unicodedata.normalize('NFKC', text)
            def clean_row(row):
                return {k: normalize_text(v) for k, v in row.items() if k.lower() not in ['usuario', 'observaciones', 'observacion']}
            df = pd.DataFrame([clean_row(row) for row in self.current_table_data])
            top = tk.Toplevel(self)
            top.title("Vista previa de impresión")
            txt = tk.Text(top, width=180, height=40)
            txt.pack(fill='both', expand=True)
            txt.insert(tk.END, df.to_string(index=False))
            btn_print = tk.Button(top, text="Imprimir", font=("Segoe UI", 11, "bold"), command=lambda: self._print_dataframe(df))
            btn_print.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Imprimir", str(e))
