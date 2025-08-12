"""
Configuración de optimización para la aplicación
"""

# Configuración de rendimiento
PERFORMANCE_CONFIG = {
    # Tiempo de actualización de la cola de datos (ms)
    'QUEUE_UPDATE_INTERVAL': 100,
    
    # Límite de lotes a mostrar en la tabla de vencimientos
    'MAX_VENCIMIENTOS_DISPLAY': 50,
    
    # Límite de alertas a mostrar
    'MAX_ALERTAS_DISPLAY': 5,
    
    # Tiempo de timeout para operaciones de API (segundos)
    'API_TIMEOUT': 10,
    
    # Habilitar cache de datos
    'ENABLE_CACHE': True,
    
    # Tiempo de vida del cache (segundos)
    'CACHE_TTL': 300,  # 5 minutos
}

# Configuración de la interfaz
UI_CONFIG = {
    # Mostrar indicadores de progreso
    'SHOW_PROGRESS': True,
    
    # Tiempo de fade para mensajes de estado
    'STATUS_FADE_TIME': 3000,  # 3 segundos
    
    # Habilitar animaciones
    'ENABLE_ANIMATIONS': False,  # Deshabilitado para mejor rendimiento
    
    # Tamaño máximo de tablas
    'MAX_TABLE_ROWS': 100,
}

# Configuración de debug
DEBUG_CONFIG = {
    # Habilitar logs de debug
    'ENABLE_DEBUG_LOGS': False,
    
    # Mostrar información de rendimiento
    'SHOW_PERFORMANCE_INFO': False,
    
    # Log de operaciones lentas (ms)
    'SLOW_OPERATION_THRESHOLD': 1000,
}
