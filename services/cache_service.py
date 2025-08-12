"""
Servicio de cache simple para mejorar el rendimiento de la aplicación
"""

import time
from typing import Any, Dict, Optional
from threading import Lock

class CacheService:
    """Servicio de cache simple con TTL (Time To Live)"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del cache si no ha expirado"""
        with self._lock:
            if key in self._cache:
                item = self._cache[key]
                if time.time() < item['expires_at']:
                    return item['value']
                else:
                    # Eliminar item expirado
                    del self._cache[key]
            return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Establece un valor en el cache con TTL en segundos"""
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
    
    def delete(self, key: str) -> None:
        """Elimina un item del cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def clear(self) -> None:
        """Limpia todo el cache"""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self) -> None:
        """Limpia items expirados del cache"""
        current_time = time.time()
        with self._lock:
            expired_keys = [
                key for key, item in self._cache.items()
                if current_time >= item['expires_at']
            ]
            for key in expired_keys:
                del self._cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cache"""
        with self._lock:
            current_time = time.time()
            total_items = len(self._cache)
            expired_items = sum(
                1 for item in self._cache.values()
                if current_time >= item['expires_at']
            )
            active_items = total_items - expired_items
            
            return {
                'total_items': total_items,
                'active_items': active_items,
                'expired_items': expired_items,
                'memory_usage': len(str(self._cache))
            }

# Instancia global del cache
cache = CacheService()
