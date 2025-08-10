"""
Archivo de estilos centralizado para la aplicación de almacén
Define colores, fuentes y estilos consistentes en toda la aplicación
"""

# Paleta de colores profesional y moderna
COLORS = {
    'primary': '#2563eb',      # Azul profesional principal
    'primary_dark': '#1d4ed8', # Azul oscuro para hover
    'primary_light': '#3b82f6', # Azul claro para elementos secundarios
    'secondary': '#64748b',    # Gris elegante secundario
    'secondary_dark': '#475569', # Gris oscuro para hover
    'secondary_light': '#94a3b8', # Gris claro para elementos sutiles
    'success': '#059669',      # Verde suave para éxito
    'success_dark': '#047857', # Verde oscuro para hover
    'success_light': '#10b981', # Verde claro para elementos secundarios
    'warning': '#d97706',      # Naranja cálido para advertencias
    'warning_dark': '#b45309', # Naranja oscuro para hover
    'warning_light': '#f59e0b', # Naranja claro para elementos secundarios
    'danger': '#dc2626',       # Rojo profesional para peligro
    'danger_dark': '#b91c1c',  # Rojo oscuro para hover
    'danger_light': '#ef4444', # Rojo claro para elementos secundarios
    'background': '#f8fafc',   # Fondo muy claro y elegante
    'background_dark': '#f1f5f9', # Fondo alternativo
    'surface': '#ffffff',      # Superficies blancas
    'surface_hover': '#f8fafc', # Superficie en hover
    'text_primary': '#1e293b', # Texto principal oscuro
    'text_secondary': '#64748b', # Texto secundario
    'text_muted': '#94a3b8',   # Texto atenuado
    'border': '#e2e8f0',      # Bordes sutiles
    'border_light': '#f1f5f9', # Bordes muy sutiles
    'accent': '#8b5cf6',       # Acento púrpura para elementos especiales
    'accent_dark': '#7c3aed',  # Acento púrpura oscuro
    'accent_light': '#a78bfa'  # Acento púrpura claro
}

# Configuración de fuentes
FONTS = {
    'title_large': ('Segoe UI', 32, 'bold'),
    'title_medium': ('Segoe UI', 24, 'bold'),
    'title_small': ('Segoe UI', 18, 'bold'),
    'heading_large': ('Segoe UI', 16, 'bold'),
    'heading_medium': ('Segoe UI', 14, 'bold'),
    'heading_small': ('Segoe UI', 12, 'bold'),
    'body_large': ('Segoe UI', 13, 'normal'),
    'body_medium': ('Segoe UI', 12, 'normal'),
    'body_small': ('Segoe UI', 11, 'normal'),
    'caption': ('Segoe UI', 10, 'normal'),
    'button': ('Segoe UI', 12, 'bold'),
    'button_large': ('Segoe UI', 14, 'bold')
}

# Estilos de botones
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': COLORS['surface'],
        'activebackground': COLORS['primary_dark'],
        'activeforeground': COLORS['surface'],
        'font': FONTS['button'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 20,
        'pady': 8
    },
    'secondary': {
        'bg': COLORS['secondary'],
        'fg': COLORS['surface'],
        'activebackground': COLORS['secondary_dark'],
        'activeforeground': COLORS['surface'],
        'font': FONTS['button'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 20,
        'pady': 8
    },
    'success': {
        'bg': COLORS['success'],
        'fg': COLORS['surface'],
        'activebackground': COLORS['success_dark'],
        'activeforeground': COLORS['surface'],
        'font': FONTS['button'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 20,
        'pady': 8
    },
    'warning': {
        'bg': COLORS['warning'],
        'fg': COLORS['surface'],
        'activebackground': COLORS['warning_dark'],
        'activeforeground': COLORS['surface'],
        'font': FONTS['button'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 20,
        'pady': 8
    },
    'danger': {
        'bg': COLORS['danger'],
        'fg': COLORS['surface'],
        'activebackground': COLORS['danger_dark'],
        'activeforeground': COLORS['surface'],
        'font': FONTS['button'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 20,
        'pady': 8
    },
    'outline': {
        'bg': COLORS['surface'],
        'fg': COLORS['primary'],
        'activebackground': COLORS['background'],
        'activeforeground': COLORS['primary_dark'],
        'font': FONTS['button'],
        'relief': 'solid',
        'borderwidth': 2,
        'cursor': 'hand2',
        'padx': 20,
        'pady': 8,
        'highlightbackground': COLORS['primary'],
        'highlightthickness': 2
    }
}

# Estilos de entrada de texto
ENTRY_STYLES = {
    'default': {
        'background': COLORS['surface'],
        'foreground': COLORS['text_primary'],
        'relief': 'solid',
        'borderwidth': 1,
        'font': FONTS['body_medium'],
        'highlightbackground': COLORS['border'],
        'highlightthickness': 1
    },
    'focused': {
        'background': COLORS['surface'],
        'foreground': COLORS['text_primary'],
        'relief': 'solid',
        'borderwidth': 2,
        'font': FONTS['body_medium'],
        'highlightbackground': COLORS['primary'],
        'highlightthickness': 2
    }
}

# Estilos de etiquetas
LABEL_STYLES = {
    'title': {
        'font': FONTS['title_large'],
        'fg': COLORS['primary'],
        'bg': COLORS['background']
    },
    'heading': {
        'font': FONTS['heading_medium'],
        'fg': COLORS['text_primary'],
        'bg': COLORS['background']
    },
    'body': {
        'font': FONTS['body_medium'],
        'fg': COLORS['text_primary'],
        'bg': COLORS['background']
    },
    'caption': {
        'font': FONTS['caption'],
        'fg': COLORS['text_secondary'],
        'bg': COLORS['background']
    },
    'success': {
        'font': FONTS['body_medium'],
        'fg': COLORS['success'],
        'bg': COLORS['background']
    },
    'warning': {
        'font': FONTS['body_medium'],
        'fg': COLORS['warning'],
        'bg': COLORS['background']
    },
    'danger': {
        'font': FONTS['body_medium'],
        'fg': COLORS['danger'],
        'bg': COLORS['background']
    }
}

# Estilos de frames
FRAME_STYLES = {
    'card': {
        'bg': COLORS['surface'],
        'relief': 'flat',
        'borderwidth': 0,
        'highlightbackground': COLORS['border'],
        'highlightthickness': 1
    },
    'card_hover': {
        'bg': COLORS['surface_hover'],
        'relief': 'flat',
        'borderwidth': 0,
        'highlightbackground': COLORS['primary'],
        'highlightthickness': 2
    },
    'section': {
        'bg': COLORS['background'],
        'relief': 'flat',
        'borderwidth': 0
    },
    'header': {
        'bg': COLORS['primary'],
        'relief': 'flat',
        'borderwidth': 0
    }
}

# Estilos de tablas
TABLE_STYLES = {
    'header': {
        'font': FONTS['heading_small'],
        'fg': COLORS['text_primary'],
        'bg': COLORS['background']
    },
    'row_odd': {
        'bg': COLORS['background']
    },
    'row_even': {
        'bg': COLORS['surface']
    },
    'row_selected': {
        'bg': COLORS['primary_light']
    },
    'row_hover': {
        'bg': COLORS['background_dark']
    }
}

# Espaciado y dimensiones
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'xxl': 48
}

# Dimensiones de componentes
DIMENSIONS = {
    'button_height': 36,
    'button_min_width': 100,
    'input_height': 40,
    'card_padding': 20,
    'section_padding': 25,
    'table_row_height': 35
}

# Sombras y efectos
SHADOWS = {
    'small': {
        'relief': 'flat',
        'borderwidth': 0,
        'highlightbackground': COLORS['border'],
        'highlightthickness': 1
    },
    'medium': {
        'relief': 'flat',
        'borderwidth': 0,
        'highlightbackground': COLORS['border'],
        'highlightthickness': 2
    },
    'large': {
        'relief': 'flat',
        'borderwidth': 0,
        'highlightbackground': COLORS['primary'],
        'highlightthickness': 3
    }
}

# Función para aplicar estilos a widgets
def apply_style(widget, style_name, style_dict):
    """Aplica un estilo predefinido a un widget"""
    if style_name in style_dict:
        for key, value in style_dict[style_name].items():
            if hasattr(widget, key):
                setattr(widget, key, value)

# Función para crear un botón con estilo
def create_styled_button(parent, text, command, style_name='primary', **kwargs):
    """Crea un botón con estilo predefinido"""
    button = tk.Button(parent, text=text, command=command, **BUTTON_STYLES[style_name])
    if kwargs:
        button.configure(**kwargs)
    return button

# Función para crear una etiqueta con estilo
def create_styled_label(parent, text, style_name='body', **kwargs):
    """Crea una etiqueta con estilo predefinido"""
    label = tk.Label(parent, text=text, **LABEL_STYLES[style_name])
    if kwargs:
        label.configure(**kwargs)
    return label

# Función para crear un frame con estilo
def create_styled_frame(parent, style_name='section', **kwargs):
    """Crea un frame con estilo predefinido"""
    frame = tk.Frame(parent, **FRAME_STYLES[style_name])
    if kwargs:
        frame.configure(**kwargs)
    return frame
