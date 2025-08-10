import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.api import get
from tkcalendar import DateEntry
import datetime

class ReportesPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#ab47bc")
        header.pack(fill='x', pady=(0, 0))
        tk.Label(header, text="Reportes", font=("Segoe UI", 28, "bold"), fg="#fff", bg="#ab47bc").pack(anchor='center', pady=18)
        
        # Frame de filtros por fechas
        filtros_frame = tk.Frame(self, bg="#f7f7f7")
        filtros_frame.pack(fill='x', pady=(10, 5))
        
        # Título de filtros
        tk.Label(filtros_frame, text="Filtros de Fecha:", font=("Segoe UI", 12, "bold"), 
                fg="#ab47bc", bg="#f7f7f7").pack(anchor='center', pady=(5, 10))
        
        # Frame para los campos de fecha
        fechas_frame = tk.Frame(filtros_frame, bg="#f7f7f7")
        fechas_frame.pack(anchor='center', pady=(0, 10))
        
        # Fecha desde
        tk.Label(fechas_frame, text="Desde:", font=("Segoe UI", 11, "bold"), 
                fg="#333", bg="#f7f7f7").pack(side='left', padx=(0, 5))
        
        # Calcular fecha de hace 30 días por defecto
        fecha_desde = datetime.date.today() - datetime.timedelta(days=30)
        self.fecha_desde_var = tk.StringVar(value=fecha_desde.strftime('%Y-%m-%d'))
        self.fecha_desde_entry = DateEntry(fechas_frame, textvariable=self.fecha_desde_var, 
                                          date_pattern='yyyy-mm-dd', font=("Segoe UI", 11), 
                                          width=12, background="#fff", foreground="#333")
        self.fecha_desde_entry.pack(side='left', padx=(0, 20))
        
        # Fecha hasta
        tk.Label(fechas_frame, text="Hasta:", font=("Segoe UI", 11, "bold"), 
                fg="#333", bg="#f7f7f7").pack(side='left', padx=(0, 5))
        
        # Fecha de hoy por defecto
        fecha_hasta = datetime.date.today()
        self.fecha_hasta_var = tk.StringVar(value=fecha_hasta.strftime('%Y-%m-%d'))
        self.fecha_hasta_entry = DateEntry(fechas_frame, textvariable=self.fecha_hasta_var, 
                                          date_pattern='yyyy-mm-dd', font=("Segoe UI", 11), 
                                          width=12, background="#fff", foreground="#333")
        self.fecha_hasta_entry.pack(side='left', padx=(0, 20))
        
        # Botón para aplicar filtros
        tk.Button(fechas_frame, text="Aplicar Filtros", command=self.aplicar_filtros_fecha, 
                 bg="#ab47bc", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", 
                 padx=16, pady=6, activebackground="#8e24aa", cursor="hand2").pack(side='left')
        
        # Botón para limpiar filtros
        tk.Button(fechas_frame, text="Limpiar Filtros", command=self.limpiar_filtros_fecha, 
                 bg="#757575", fg="#fff", font=("Segoe UI", 11, "bold"), relief="flat", 
                 padx=16, pady=6, activebackground="#616161", cursor="hand2").pack(side='left', padx=(10, 0))
        
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
        
        # Variables para almacenar datos filtrados
        self.datos_filtrados = []
        self.filtros_activos = False
        
        # Label para mostrar estado de filtros
        self.lbl_filtros = tk.Label(filtros_frame, text="", font=("Segoe UI", 10), 
                                   fg="#666", bg="#f7f7f7")
        self.lbl_filtros.pack(anchor='center', pady=(0, 5))
        
        # Label para mostrar estadísticas de filtros
        self.lbl_stats = tk.Label(filtros_frame, text="", font=("Segoe UI", 9), 
                                 fg="#888", bg="#f7f7f7")
        self.lbl_stats.pack(anchor='center', pady=(0, 5))

    def reporte_inventario(self):
        self.mostrar_reporte("/products")

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
                self.column_mapping = []
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
                        if 'producto' in row and isinstance(row['producto'], dict):
                            new_row['Codigo Producto'] = row['producto'].get('codigo', '')
                            new_row['Nombre'] = row['producto'].get('nombre', '')
                        else:
                            new_row['Codigo Producto'] = row.get('producto', '')
                            new_row['Nombre'] = ''
                        new_row['Tipo'] = row.get('tipo', '')
                        new_row['Fecha'] = row.get('fecha', '')
                        new_row['Cantidad'] = row.get('cantidad', '')
                        new_row['Stock anterior'] = row.get('stock_anterior', '')
                        new_row['Stock posterior'] = row.get('stock_posterior', '')
                        display_data.append(new_row)
                    self.current_table_data = display_data
                    self.current_table_columns = columns
                    # Para movimientos, la clave y el título son iguales
                    self.column_mapping = [(col, col) for col in columns]
                    # Guardar datos originales para filtros
                    self.datos_originales = display_data.copy()
                    self.tree_result = ttk.Treeview(self.result_frame, columns=columns, show='headings', style="Treeview")
                    for col in columns:
                        self.tree_result.heading(col, text=col, anchor='center')
                        self.tree_result.column(col, width=120, anchor='center')
                    for row in display_data:
                        self.tree_result.insert('', 'end', values=[row.get(col, '') for col in columns])
                    self.tree_result.pack(fill='both', expand=True, padx=10, pady=10)
                else:
                    columns = [
                        ("codigo_item", "Código"),
                        ("nombre_item", "Nombre"),
                        ("nombre_marca", "Marca"),
                        ("orden_compra", "Orden Compra"),
                        ("nombre_medida", "Medida"),
                        ("mayor", "Mayor"),
                        ("sub_cta", "Subcuenta"),
                        ("stock_actual", "Stock"),
                        ("fecha_ingreso", "F. Ingreso"),
                        ("fecha_vencimiento", "F. Vencimiento")
                    ]
                    display_data = []
                    for row in items:
                        new_row = {}
                        for key, _ in columns:
                            new_row[key] = row.get(key, '')
                        display_data.append(new_row)
                    self.current_table_data = display_data
                    col_titles = [title for _, title in columns]
                    self.current_table_columns = col_titles
                    # Para inventario, guardar el mapeo de clave a título
                    self.column_mapping = columns
                    # Guardar datos originales para filtros
                    self.datos_originales = display_data.copy()
                    self.tree_result = ttk.Treeview(self.result_frame, columns=col_titles, show='headings', style="Treeview")
                    for idx, (key, title) in enumerate(columns):
                        self.tree_result.heading(title, text=title, anchor='center')
                        self.tree_result.column(title, width=120, anchor='center')
                    for row in display_data:
                        self.tree_result.insert('', 'end', values=[row.get(key, '') for key, _ in columns])
                    self.tree_result.pack(fill='both', expand=True, padx=10, pady=10)
                
                # Mostrar información sobre filtros si están activos
                if self.filtros_activos:
                    # Asegurar que tenemos los datos originales guardados antes de aplicar filtros
                    if not hasattr(self, 'datos_originales'):
                        self.datos_originales = display_data.copy()
                    
                    self.aplicar_filtros_a_datos_existentes(
                        datetime.datetime.strptime(self.fecha_desde_var.get(), '%Y-%m-%d').date(),
                        datetime.datetime.strptime(self.fecha_hasta_var.get(), '%Y-%m-%d').date()
                    )
            else:
                self.txt_result.pack(fill='both', expand=True, padx=10, pady=10)
                self.txt_result.delete(1.0, tk.END)
                self.txt_result.insert(tk.END, "No hay datos tabulares para mostrar.")
                self.current_table_data = []
                self.current_table_columns = []
                self.column_mapping = []
                self.datos_originales = []
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
            
            # Verificar si hay datos para exportar
            if not hasattr(self, 'current_table_data') or not self.current_table_data:
                messagebox.showwarning("Exportar PDF", "No hay datos para exportar.")
                return
            
            # Mostrar información sobre qué se va a exportar
            mensaje_exportacion = "Se exportarán los datos del reporte"
            if self.filtros_activos:
                mensaje_exportacion += f" con filtros aplicados (desde {self.fecha_desde_var.get()} hasta {self.fecha_hasta_var.get()})"
            mensaje_exportacion += "."
            
            # Mostrar mensaje informativo
            messagebox.showinfo("Exportar PDF", mensaje_exportacion)
            
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
            # Crear título con información de filtros si están activos
            titulo_reporte = "Reporte de datos"
            if self.filtros_activos:
                titulo_reporte += f" (Filtrado: {self.fecha_desde_var.get()} - {self.fecha_hasta_var.get()})"
            
            title = Paragraph(f"<b>{titulo_reporte}</b>", ParagraphStyle('title', fontName=header_font, fontSize=14, alignment=1))
            
            # Agregar información de filtros si están activos
            elements = [title, Spacer(1, 12)]
            
            if self.filtros_activos:
                info_filtros = [
                    f"Filtros aplicados: Sí",
                    f"Fecha desde: {self.fecha_desde_var.get()}",
                    f"Fecha hasta: {self.fecha_hasta_var.get()}",
                    f"Total registros originales: {len(self.datos_originales) if hasattr(self, 'datos_originales') else 0}",
                    f"Registros filtrados: {len(self.current_table_data)}"
                ]
                
                for info in info_filtros:
                    info_para = Paragraph(info, ParagraphStyle('info', fontName=cell_font, fontSize=9, leading=11, alignment=0))
                    elements.append(info_para)
                
                elements.append(Spacer(1, 12))
            
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
            elements.append(table)
            doc.build(elements)
            
            # Mostrar información sobre el PDF generado
            mensaje_final = f"PDF generado: {file_path}"
            if self.filtros_activos:
                mensaje_final += f"\n\nContiene {len(self.current_table_data)} registros filtrados de {len(self.datos_originales) if hasattr(self, 'datos_originales') else 0} totales."
            
            messagebox.showinfo("Exportar PDF", mensaje_final)
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
            
            # Verificar si hay datos para exportar
            if not hasattr(self, 'current_table_data') or not self.current_table_data:
                messagebox.showwarning("Exportar Excel", "No hay datos para exportar.")
                return
            
            # Mostrar información sobre qué se va a exportar
            mensaje_exportacion = "Se exportarán los datos del reporte"
            if self.filtros_activos:
                mensaje_exportacion += f" con filtros aplicados (desde {self.fecha_desde_var.get()} hasta {self.fecha_hasta_var.get()})"
            mensaje_exportacion += "."
            
            # Mostrar mensaje informativo
            messagebox.showinfo("Exportar Excel", mensaje_exportacion)
            
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
            # Agregar información sobre filtros si están activos
            if self.filtros_activos:
                # Crear un DataFrame con información de filtros
                info_filtros = pd.DataFrame({
                    'Información': ['Filtros aplicados', 'Fecha desde', 'Fecha hasta', 'Total registros originales', 'Registros filtrados'],
                    'Valor': [
                        'Sí',
                        self.fecha_desde_var.get(),
                        self.fecha_hasta_var.get(),
                        len(self.datos_originales) if hasattr(self, 'datos_originales') else 0,
                        len(self.current_table_data)
                    ]
                })
                
                # Escribir información de filtros en hojas separadas
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Datos', index=False)
                    info_filtros.to_excel(writer, sheet_name='Información de Filtros', index=False)
                    
                # Mostrar información sobre las hojas creadas
                messagebox.showinfo("Exportar Excel", f"Excel generado con {len(df)} registros filtrados.\nSe crearon 2 hojas:\n- 'Datos': Contiene los registros filtrados\n- 'Información de Filtros': Detalles de los filtros aplicados")
            else:
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
            
            # Verificar si hay datos para imprimir
            if not hasattr(self, 'current_table_data') or not self.current_table_data:
                messagebox.showwarning("Imprimir", "No hay datos para imprimir.")
                return
            
            # Mostrar información sobre qué se va a imprimir
            mensaje_impresion = "Se imprimirán los datos del reporte"
            if self.filtros_activos:
                mensaje_impresion += f" con filtros aplicados (desde {self.fecha_desde_var.get()} hasta {self.fecha_hasta_var.get()})"
            mensaje_impresion += "."
            
            # Mostrar mensaje informativo
            messagebox.showinfo("Imprimir", mensaje_impresion)
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
            
            # Agregar información sobre filtros si están activos
            if self.filtros_activos:
                info_frame = tk.Frame(top, bg="#f0f0f0")
                info_frame.pack(fill='x', padx=10, pady=5)
                
                # Información principal de filtros
                tk.Label(info_frame, text=f"Filtros aplicados: {self.fecha_desde_var.get()} hasta {self.fecha_hasta_var.get()}", 
                        font=("Segoe UI", 10, "bold"), fg="#ab47bc", bg="#f0f0f0").pack(anchor='w')
                
                # Estadísticas adicionales
                if hasattr(self, 'datos_originales'):
                    total_original = len(self.datos_originales)
                    total_filtrado = len(self.current_table_data)
                    porcentaje = (total_filtrado / total_original * 100) if total_original > 0 else 0
                    
                    stats_text = f"Total registros originales: {total_original} | Registros filtrados: {total_filtrado} ({porcentaje:.1f}%)"
                    tk.Label(info_frame, text=stats_text, font=("Segoe UI", 9), fg="#666", bg="#f0f0f0").pack(anchor='w')
            
            txt = tk.Text(top, width=180, height=40)
            txt.pack(fill='both', expand=True, padx=10, pady=5)
            txt.insert(tk.END, df.to_string(index=False))
            btn_print = tk.Button(top, text="Imprimir", font=("Segoe UI", 11, "bold"), command=lambda: self._print_dataframe(df))
            btn_print.pack(pady=10)
            
            # Agregar información sobre el total de registros
            total_registros = len(self.current_table_data)
            if self.filtros_activos and hasattr(self, 'datos_originales'):
                total_original = len(self.datos_originales)
                tk.Label(top, text=f"Total de registros a imprimir: {total_registros} de {total_original}", 
                        font=("Segoe UI", 10), fg="#666").pack(pady=5)
            else:
                tk.Label(top, text=f"Total de registros a imprimir: {total_registros}", 
                        font=("Segoe UI", 10), fg="#666").pack(pady=5)
        except Exception as e:
            messagebox.showerror("Imprimir", str(e))

    def actualizar_estadisticas_filtros(self):
        """Actualiza las estadísticas de los filtros aplicados"""
        try:
            if hasattr(self, 'current_table_data') and hasattr(self, 'datos_originales'):
                total_original = len(self.datos_originales)
                total_filtrado = len(self.current_table_data)
                porcentaje = (total_filtrado / total_original * 100) if total_original > 0 else 0
                
                stats_text = f"Total registros: {total_original} | Filtrados: {total_filtrado} ({porcentaje:.1f}%)"
                self.lbl_stats.config(text=stats_text, fg="#666")
        except Exception as e:
            self.lbl_stats.config(text="", fg="#888")

    def cargar_reportes(self):
        """Método para recargar reportes (llamado desde main_window)"""
        # Si hay filtros activos, limpiarlos primero
        if self.filtros_activos:
            self.limpiar_filtros_fecha()
        # Los reportes se cargarán automáticamente cuando se cambie de pestaña

    def aplicar_filtros_fecha(self):
        """Aplica los filtros de fecha seleccionados"""
        try:
            fecha_desde = datetime.datetime.strptime(self.fecha_desde_var.get(), '%Y-%m-%d').date()
            fecha_hasta = datetime.datetime.strptime(self.fecha_hasta_var.get(), '%Y-%m-%d').date()
            
            if fecha_desde > fecha_hasta:
                messagebox.showerror("Error de Fechas", "La fecha 'Desde' no puede ser mayor que la fecha 'Hasta'")
                return
            
            # Marcar que hay filtros activos
            self.filtros_activos = True
            
            # Actualizar label de estado
            self.lbl_filtros.config(text=f"Filtros activos: {fecha_desde} hasta {fecha_hasta}", fg="#ab47bc")
            
            # Si ya hay datos cargados, aplicar filtros
            if hasattr(self, 'current_table_data') and self.current_table_data:
                # Asegurar que tenemos los datos originales guardados
                if not hasattr(self, 'datos_originales'):
                    self.datos_originales = self.current_table_data.copy()
                
                self.aplicar_filtros_a_datos_existentes(fecha_desde, fecha_hasta)
                # Actualizar estadísticas
                self.actualizar_estadisticas_filtros()
            
            messagebox.showinfo("Filtros Aplicados", f"Filtros aplicados desde {fecha_desde} hasta {fecha_hasta}")
            
        except ValueError as e:
            messagebox.showerror("Error de Fechas", "Por favor, ingrese fechas válidas en formato YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtros: {str(e)}")

    def limpiar_filtros_fecha(self):
        """Limpia los filtros de fecha y restaura los datos originales"""
        try:
            # Restaurar fechas por defecto
            fecha_desde = datetime.date.today() - datetime.timedelta(days=30)
            fecha_hasta = datetime.date.today()
            
            self.fecha_desde_var.set(fecha_desde.strftime('%Y-%m-%d'))
            self.fecha_hasta_var.set(fecha_hasta.strftime('%Y-%m-%d'))
            
            # Marcar que no hay filtros activos
            self.filtros_activos = False
            
            # Limpiar label de estado
            self.lbl_filtros.config(text="", fg="#666")
            
            # Limpiar estadísticas
            self.lbl_stats.config(text="", fg="#888")
            
            # Si hay datos originales, restaurarlos
            if hasattr(self, 'datos_originales') and self.datos_originales:
                self.current_table_data = self.datos_originales.copy()
                self.actualizar_vista_tabla()
            
            messagebox.showinfo("Filtros Limpiados", "Los filtros de fecha han sido limpiados")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar filtros: {str(e)}")

    def aplicar_filtros_a_datos_existentes(self, fecha_desde, fecha_hasta):
        """Aplica filtros de fecha a los datos ya cargados"""
        if not hasattr(self, 'current_table_data') or not self.current_table_data:
            return
        
        # Guardar datos originales si no se han guardado antes
        if not hasattr(self, 'datos_originales'):
            self.datos_originales = self.current_table_data.copy()
        
        # Siempre filtrar sobre los datos originales, no sobre los ya filtrados
        datos_originales = self.datos_originales
        
        print(f"DEBUG: Aplicando filtros desde {fecha_desde} hasta {fecha_hasta}")
        print(f"DEBUG: Total datos originales: {len(datos_originales)}")
        
        # Filtrar por fecha
        datos_filtrados = []
        for row in datos_originales:
            # Buscar el campo de fecha en la fila
            # Para reporte de movimientos, usar 'Fecha'
            # Para reporte de inventario, usar 'F. Ingreso' o 'fecha_ingreso'
            fecha_str = None
            
            if 'Fecha' in row:
                fecha_str = row.get('Fecha', '')
                print(f"DEBUG: Encontrada columna 'Fecha': {fecha_str}")
            elif 'F. Ingreso' in row:
                fecha_str = row.get('F. Ingreso', '')
                print(f"DEBUG: Encontrada columna 'F. Ingreso': {fecha_str}")
            elif 'fecha_ingreso' in row:
                fecha_str = row.get('fecha_ingreso', '')
                print(f"DEBUG: Encontrada columna 'fecha_ingreso': {fecha_str}")
            
            if not fecha_str:
                continue
            
            try:
                # Intentar parsear la fecha en diferentes formatos
                fecha_item = None
                
                # Formato DD/MM/YYYY HH:MM (con tiempo)
                if '/' in fecha_str and ':' in fecha_str:
                    try:
                        fecha_item = datetime.datetime.strptime(fecha_str, '%d/%m/%Y %H:%M').date()
                        print(f"DEBUG: Fecha parseada DD/MM/YYYY HH:MM: {fecha_str} -> {fecha_item}")
                    except ValueError:
                        print(f"DEBUG: Error parseando DD/MM/YYYY HH:MM: {fecha_str}")
                        pass
                
                # Formato DD/MM/YYYY (sin tiempo)
                if not fecha_item and '/' in fecha_str:
                    try:
                        fecha_item = datetime.datetime.strptime(fecha_str, '%d/%m/%Y').date()
                        print(f"DEBUG: Fecha parseada DD/MM/YYYY: {fecha_str} -> {fecha_item}")
                    except ValueError:
                        print(f"DEBUG: Error parseando DD/MM/YYYY: {fecha_str}")
                        pass
                
                # Formato YYYY-MM-DD HH:MM (con tiempo)
                if not fecha_item and '-' in fecha_str and ':' in fecha_str and len(fecha_str.split('-')[0]) == 4:
                    try:
                        fecha_item = datetime.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M').date()
                        print(f"DEBUG: Fecha parseada YYYY-MM-DD HH:MM: {fecha_str} -> {fecha_item}")
                    except ValueError:
                        print(f"DEBUG: Error parseando YYYY-MM-DD HH:MM: {fecha_str}")
                        pass
                
                # Formato YYYY-MM-DD (sin tiempo)
                if not fecha_item and '-' in fecha_str and len(fecha_str.split('-')[0]) == 4:
                    try:
                        fecha_item = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
                        print(f"DEBUG: Fecha parseada YYYY-MM-DD: {fecha_str} -> {fecha_item}")
                    except ValueError:
                        print(f"DEBUG: Error parseando YYYY-MM-DD: {fecha_str}")
                        pass
                
                # Si se pudo parsear la fecha, verificar si está en el rango
                if fecha_item and fecha_desde <= fecha_item <= fecha_hasta:
                    datos_filtrados.append(row)
                    print(f"DEBUG: Fecha {fecha_item} está en rango, fila incluida")
                elif fecha_item:
                    print(f"DEBUG: Fecha {fecha_item} NO está en rango, fila omitida")
                    
            except Exception as e:
                # Si hay algún error al procesar la fecha, omitir la fila
                print(f"DEBUG: Error procesando fecha {fecha_str}: {e}")
                continue
        
        print(f"DEBUG: Total datos filtrados: {len(datos_filtrados)}")
        print(f"DEBUG: Columnas disponibles: {self.current_table_columns}")
        print(f"DEBUG: Primer dato filtrado: {datos_filtrados[0] if datos_filtrados else 'No hay datos'}")
        
        # Actualizar datos y vista
        self.current_table_data = datos_filtrados
        self.actualizar_vista_tabla()

    def actualizar_vista_tabla(self):
        """Actualiza la vista de la tabla con los datos filtrados"""
        # Limpiar tabla anterior si existe
        if hasattr(self, 'tree_result') and self.tree_result:
            self.tree_result.destroy()
            self.tree_result = None
        
        # Crear nueva tabla con datos filtrados
        if hasattr(self, 'current_table_columns') and self.current_table_columns:
            # Usar el mapeo de columnas para obtener los valores correctos
            if hasattr(self, 'column_mapping') and self.column_mapping:
                print(f"DEBUG: Usando mapeo de columnas: {self.column_mapping}")
                print(f"DEBUG: Datos a insertar: {len(self.current_table_data)} filas")
                
                # Crear la tabla con los títulos de las columnas
                col_titles = [title for _, title in self.column_mapping]
                self.tree_result = ttk.Treeview(self.result_frame, columns=col_titles, show='headings', style="Treeview")
                
                # Configurar columnas
                for _, title in self.column_mapping:
                    self.tree_result.heading(title, text=title, anchor='center')
                    self.tree_result.column(title, width=120, anchor='center')
                
                # Insertar datos filtrados usando las claves correctas
                for i, row in enumerate(self.current_table_data):
                    values = [row.get(key, '') for key, _ in self.column_mapping]
                    print(f"DEBUG: Fila {i}: {values}")
                    self.tree_result.insert('', 'end', values=values)
                
            else:
                # Fallback: usar columnas directamente (para compatibilidad)
                print(f"DEBUG: No hay mapeo de columnas, usando columnas directamente: {self.current_table_columns}")
                self.tree_result = ttk.Treeview(self.result_frame, columns=self.current_table_columns, show='headings', style="Treeview")
                
                # Configurar columnas
                for col in self.current_table_columns:
                    self.tree_result.heading(col, text=col, anchor='center')
                    self.tree_result.column(col, width=120, anchor='center')
                
                # Insertar datos filtrados
                for i, row in enumerate(self.current_table_data):
                    values = [row.get(col, '') for col in self.current_table_columns]
                    print(f"DEBUG: Fila {i}: {values}")
                    self.tree_result.insert('', 'end', values=values)
            
            self.tree_result.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Mostrar contador de registros filtrados
            total_registros = len(self.current_table_data)
            if self.filtros_activos and hasattr(self, 'datos_originales'):
                total_original = len(self.datos_originales)
                # Obtener las fechas de los filtros activos
                fecha_desde_str = self.fecha_desde_var.get()
                fecha_hasta_str = self.fecha_hasta_var.get()
                self.lbl_filtros.config(text=f"Filtros activos: {fecha_desde_str} hasta {fecha_hasta_str} | Mostrando {total_registros} de {total_original} registros", fg="#ab47bc")
                # Actualizar estadísticas
                self.actualizar_estadisticas_filtros()
        else:
            print("DEBUG: No hay columnas disponibles para crear la tabla")
