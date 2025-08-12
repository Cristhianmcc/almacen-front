"""
Utilidades para mejorar la apariencia y legibilidad de las tablas
"""

import tkinter as tk
from tkinter import ttk
from ui.styles import TABLE_STYLES, TREEVIEW_STYLES, COLORS, FONTS

def apply_table_styles(treeview):
    """
    Aplica estilos mejorados a un Treeview (tabla)
    """
    try:
        # Configurar estilos para el Treeview
        style = ttk.Style()
        
        # Estilo para encabezados
        style.configure(
            "Treeview.Heading",
            background=COLORS['table_header_bg'],
            foreground=COLORS['text_table_header'],
            font=FONTS['heading_small'],
            relief="solid",
            borderwidth=1
        )
        
        # Estilo para filas
        style.configure(
            "Treeview",
            background=COLORS['surface'],
            foreground=COLORS['text_primary'],
            fieldbackground=COLORS['surface'],
            font=FONTS['body_medium'],
            rowheight=25
        )
        
        # Estilo para filas seleccionadas
        style.map(
            "Treeview",
            background=[
                ('selected', COLORS['primary_light']),
                ('active', COLORS['primary_light'])
            ],
            foreground=[
                ('selected', COLORS['surface']),
                ('active', COLORS['surface'])
            ]
        )
        
        # Configurar colores alternados para filas
        treeview.tag_configure('even_row', background=COLORS['table_row_even'])
        treeview.tag_configure('odd_row', background=COLORS['table_row_odd'])
        treeview.tag_configure('selected_row', background=COLORS['primary_light'], foreground=COLORS['surface'])
        
    except Exception as e:
        print(f"Error aplicando estilos de tabla: {e}")

def create_improved_table(parent, columns, headers, widths=None, height=10):
    """
    Crea una tabla mejorada con estilos aplicados
    
    Args:
        parent: Widget padre
        columns: Lista de nombres de columnas
        headers: Lista de títulos de encabezados
        widths: Lista de anchos de columnas (opcional)
        height: Altura de la tabla
    
    Returns:
        Treeview configurado con estilos mejorados
    """
    try:
        # Crear frame para la tabla
        table_frame = tk.Frame(parent, bg=COLORS['background'])
        
        # Crear scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        
        # Crear tabla
        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=vsb.set,
            height=height
        )
        table.pack(side='left', fill='both', expand=True)
        
        # Configurar scrollbar
        vsb.config(command=table.yview)
        
        # Configurar columnas
        if widths is None:
            widths = [150] * len(columns)  # Ancho por defecto
        
        for i, (col, header, width) in enumerate(zip(columns, headers, widths)):
            table.heading(col, text=header)
            table.column(col, width=width, anchor='center', minwidth=80)
        
        # Aplicar estilos
        apply_table_styles(table)
        
        return table, table_frame
        
    except Exception as e:
        print(f"Error creando tabla mejorada: {e}")
        return None, None

def insert_table_row_with_style(table, values, row_index):
    """
    Inserta una fila en la tabla con estilo alternado
    
    Args:
        table: Treeview de la tabla
        values: Valores de la fila
        row_index: Índice de la fila (para alternar colores)
    """
    try:
        # Determinar el tag para el color alternado
        tag = 'even_row' if row_index % 2 == 0 else 'odd_row'
        
        # Insertar la fila con el tag apropiado
        item = table.insert('', 'end', values=values, tags=(tag,))
        
        return item
        
    except Exception as e:
        print(f"Error insertando fila en tabla: {e}")
        return None

def highlight_selected_row(table, event):
    """
    Resalta la fila seleccionada en la tabla
    """
    try:
        # Obtener item seleccionado
        selection = table.selection()
        if selection:
            # Aplicar tag de selección
            for item in selection:
                table.item(item, tags=('selected_row',))
        else:
            # Restaurar colores alternados
            for i, item in enumerate(table.get_children()):
                tag = 'even_row' if i % 2 == 0 else 'odd_row'
                table.item(item, tags=(tag,))
                
    except Exception as e:
        print(f"Error resaltando fila seleccionada: {e}")

def setup_table_selection_events(table):
    """
    Configura eventos para la selección de filas en la tabla
    """
    try:
        # Evento de selección
        table.bind('<<TreeviewSelect>>', lambda e: highlight_selected_row(table, e))
        
        # Evento de doble clic
        table.bind('<Double-1>', lambda e: on_table_double_click(table, e))
        
    except Exception as e:
        print(f"Error configurando eventos de tabla: {e}")

def on_table_double_click(table, event):
    """
    Maneja el doble clic en una fila de la tabla
    """
    try:
        # Obtener item seleccionado
        selection = table.selection()
        if selection:
            item = selection[0]
            values = table.item(item, 'values')
            print(f"Fila seleccionada: {values}")
            # Aquí puedes agregar la lógica para editar o mostrar detalles
            
    except Exception as e:
        print(f"Error en doble clic de tabla: {e}")

def clear_table(table):
    """
    Limpia todas las filas de la tabla
    """
    try:
        for item in table.get_children():
            table.delete(item)
    except Exception as e:
        print(f"Error limpiando tabla: {e}")

def get_selected_row_data(table):
    """
    Obtiene los datos de la fila seleccionada
    
    Returns:
        Lista de valores de la fila seleccionada o None si no hay selección
    """
    try:
        selection = table.selection()
        if selection:
            return table.item(selection[0], 'values')
        return None
    except Exception as e:
        print(f"Error obteniendo datos de fila seleccionada: {e}")
        return None
