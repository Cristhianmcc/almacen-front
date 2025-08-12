# -*- mode: python ; coding: utf-8 -*-
# =============================================================================
# Archivo de especificación para PyInstaller - AlmacenInstituto
# Versión: 2.0 - Configuración Profesional
# Autor: CrisLissRen
# Fecha: 2025
# =============================================================================

import os
import sys

# Configuración de análisis
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Archivos de la interfaz
        ('ui/img', 'ui/img'),
        ('ui/DejaVuSans.ttf', 'ui'),
        ('ui/styles.py', 'ui'),
        ('ui/config.py', 'ui'),
        
        # Archivos de servicios
        ('services', 'services'),
        
        # Archivos de configuración
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('license.txt', '.'),
        ('CHANGELOG.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'tkinter.colorchooser',
        'tkinter.commondialog',
        'tkinter.constants',
        'tkinter.dnd',
        'tkinter.font',
        'tkinter.scrolledtext',
        'tkinter.tix',
        'tkinter.turtle',
        'tkinter.ttk',
        'tkinter.ttk._util',
        'tkinter.ttk._style',
        'tkinter.ttk._combobox',
        'tkinter.ttk._entry',
        'tkinter.ttk._frame',
        'tkinter.ttk._label',
        'tkinter.ttk._labelFrame',
        'tkinter.ttk._menubutton',
        'tkinter.ttk._notebook',
        'tkinter.ttk._panedwindow',
        'tkinter.ttk._progressbar',
        'tkinter.ttk._scale',
        'tkinter.ttk._scrollbar',
        'tkinter.ttk._separator',
        'tkinter.ttk._sizegrip',
        'tkinter.ttk._spinbox',
        'tkinter.ttk._treeview',
        'tkinter.ttk._widget',
        'threading',
        'queue',
        'datetime',
        'json',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'PIL',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
    ],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'scipy', 'IPython', 'jupyter',
        'qt5', 'pygame', 'sqlite3', 'test', 'unittest', 'doctest',
        'pydoc', 'pdb', 'profile', 'cProfile', 'trace', 'pickletools',
        'distutils', 'setuptools', 'pkg_resources', 'easy_install',
        'pip', 'wheel', 'virtualenv', 'venv'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Configuración de PyInstaller
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Configuración del ejecutable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AlmacenInstituto',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ui/img/icono.ico',
    version_file=None,
    uac_admin=False,
    uac_uiaccess=False,
)

# Configuración de recolección
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AlmacenInstituto',
)

# Configuraciones adicionales
app = BUNDLE(
    coll,
    name='AlmacenInstituto.app',
    icon='ui/img/icono.ico',
    bundle_identifier='com.almacen-instituto.app',
    info_plist={
        'CFBundleName': 'Sistema de Almacén - Instituto',
        'CFBundleDisplayName': 'Sistema de Almacén - Instituto',
        'CFBundleGetInfoString': 'Sistema profesional de gestión de inventario',
        'CFBundleIdentifier': 'com.almacen-instituto.app',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0.0',
        'NSHighResolutionCapable': 'True',
    },
)
