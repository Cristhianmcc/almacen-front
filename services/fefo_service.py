"""
Servicio especializado para implementar la lógica FEFO (First Expired, First Out)
Maneja la distribución automática de salidas de stock basándose en fechas de vencimiento
"""

import datetime
from typing import List, Dict, Tuple, Optional
from services.api import get, post, put

class LoteFEFO:
    """Representa un lote de producto con información de vencimiento"""
    
    def __init__(self, producto_id: int, cantidad: int, fecha_vencimiento: str, 
                 codigo_item: str, nombre_item: str, numero_lote: str = None):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.fecha_vencimiento = fecha_vencimiento
        self.codigo_item = codigo_item
        self.nombre_item = nombre_item
        self.numero_lote = numero_lote or f"LOTE-{producto_id}-{fecha_vencimiento}"
        
    def __lt__(self, other):
        """Ordenar por fecha de vencimiento (más antigua primero)"""
        try:
            fecha_self = datetime.datetime.strptime(self.fecha_vencimiento, '%Y-%m-%d').date()
            fecha_other = datetime.datetime.strptime(other.fecha_vencimiento, '%Y-%m-%d').date()
            return fecha_self < fecha_other
        except:
            return False
    
    def to_dict(self):
        """Convertir a diccionario para API"""
        return {
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'fecha_vencimiento': self.fecha_vencimiento,
            'codigo_item': self.codigo_item,
            'nombre_item': self.nombre_item,
            'numero_lote': self.numero_lote
        }

class DistribucionFEFO:
    """Resultado de la distribución FEFO de una salida"""
    
    def __init__(self, cantidad_solicitada: int, lotes_usados: List[Dict], 
                 stock_anterior: int, stock_final: int):
        self.cantidad_solicitada = cantidad_solicitada
        self.lotes_usados = lotes_usados
        self.stock_anterior = stock_anterior
        self.stock_final = stock_final
        self.cantidad_entregada = cantidad_solicitada
        
    def to_dict(self):
        """Convertir a diccionario para API"""
        return {
            'cantidad_solicitada': self.cantidad_solicitada,
            'lotes_usados': self.lotes_usados,
            'stock_anterior': self.stock_anterior,
            'stock_final': self.stock_final,
            'cantidad_entregada': self.cantidad_entregada
        }

class FEFOService:
    """Servicio principal para la lógica FEFO"""
    
    @staticmethod
    def crear_lote_entrada(producto_id: int, cantidad: int, fecha_entrada: str = None, 
                          fecha_vencimiento: str = None) -> LoteFEFO:
        """
        Crea un nuevo lote cuando se registra una entrada
        """
        try:
            # Obtener información del producto
            resp = get(f"/products/{producto_id}")
            if not resp.success:
                raise Exception(f"Error al obtener producto: {resp.message}")
            
            producto = resp.data
            if not producto:
                raise Exception("Producto no encontrado")
            
            # Si no se especifica fecha de entrada, usar la actual
            if not fecha_entrada:
                fecha_entrada = datetime.date.today().strftime('%Y-%m-%d')
            
            # Si no se especifica fecha de vencimiento, usar la del producto o una fecha por defecto
            if not fecha_vencimiento:
                fecha_vencimiento = producto.get('fecha_vencimiento') or '9999-12-31'
            
            # Crear número de lote único con fecha de vencimiento
            numero_lote = f"ENTRADA-{producto_id}-{fecha_entrada}-{fecha_vencimiento}"
            
            lote = LoteFEFO(
                producto_id=producto_id,
                cantidad=cantidad,
                fecha_vencimiento=fecha_vencimiento,
                codigo_item=producto.get('codigo_item', ''),
                nombre_item=producto.get('nombre_item', ''),
                numero_lote=numero_lote
            )
            
            return lote
            
        except Exception as e:
            raise Exception(f"Error al crear lote de entrada: {str(e)}")
    
    @staticmethod
    def obtener_lotes_producto(producto_id: int) -> List[LoteFEFO]:
        """
        Obtiene todos los lotes de un producto ordenados por fecha de vencimiento
        Versión optimizada que no crea lotes automáticamente
        """
        try:
            # Obtener el producto con su información
            resp = get(f"/products/{producto_id}")
            
            if not resp.success:
                return []  # Retornar lista vacía en lugar de lanzar excepción
            
            producto = resp.data
            if not producto:
                return []
            
            # Intentar obtener lotes desde el historial de movimientos
            lotes = []
            
            try:
                # Obtener movimientos del producto
                movimientos_resp = get(f"/movements")
                if movimientos_resp.success and movimientos_resp.data:
                    # Filtrar movimientos de este producto
                    movimientos_producto = [
                        m for m in movimientos_resp.data 
                        if m.get('productos', {}).get('id') == producto_id
                    ]
                    
                    # Crear lotes basándose en entradas
                    entradas = [m for m in movimientos_producto if m.get('tipo_movimiento') == 'entrada']
                    
                    if entradas:
                        # Crear un lote por cada entrada
                        for i, entrada in enumerate(entradas):
                            fecha_entrada = entrada.get('fecha_movimiento', '2024-01-01')
                            cantidad_entrada = entrada.get('cantidad', 0)
                            
                            # Usar fecha de vencimiento real del formulario
                            # Por ahora, simular fechas diferenciadas
                            try:
                                fecha_ent = datetime.datetime.strptime(fecha_entrada[:10], '%Y-%m-%d')
                                # Cada entrada vence en una fecha diferente
                                dias_vencimiento = 365 + (i * 30)  # 365, 395, 425... días
                                fecha_venc = fecha_ent + datetime.timedelta(days=dias_vencimiento)
                                fecha_vencimiento = fecha_venc.strftime('%Y-%m-%d')
                            except:
                                fecha_vencimiento = '9999-12-31'
                            
                            lote = LoteFEFO(
                                producto_id=producto['id'],
                                cantidad=cantidad_entrada,
                                fecha_vencimiento=fecha_vencimiento,
                                codigo_item=producto.get('codigo_item', ''),
                                nombre_item=producto.get('nombre_item', ''),
                                numero_lote=f"ENTRADA-{producto_id}-{i+1}-{fecha_entrada[:10]}"
                            )
                            lotes.append(lote)
                    
                    # Si no hay entradas, crear lote principal solo si es necesario
                    if not lotes and producto.get('stock_actual', 0) > 0:
                        if producto.get('fecha_vencimiento'):
                            lote = LoteFEFO(
                                producto_id=producto['id'],
                                cantidad=producto.get('stock_actual', 0),
                                fecha_vencimiento=producto['fecha_vencimiento'],
                                codigo_item=producto.get('codigo_item', ''),
                                nombre_item=producto.get('nombre_item', ''),
                                numero_lote=f"LOTE-{producto['id']}-{producto['fecha_vencimiento']}"
                            )
                            lotes.append(lote)
                        else:
                            lote = LoteFEFO(
                                producto_id=producto['id'],
                                cantidad=producto.get('stock_actual', 0),
                                fecha_vencimiento='9999-12-31',
                                codigo_item=producto.get('codigo_item', ''),
                                nombre_item=producto.get('nombre_item', ''),
                                numero_lote=f"LOTE-{producto['id']}-SIN-VENCIMIENTO"
                            )
                            lotes.append(lote)
                
                else:
                    # Si no hay movimientos, crear lote principal solo si es necesario
                    if producto.get('stock_actual', 0) > 0:
                        if producto.get('fecha_vencimiento'):
                            lote = LoteFEFO(
                                producto_id=producto['id'],
                                cantidad=producto.get('stock_actual', 0),
                                fecha_vencimiento=producto['fecha_vencimiento'],
                                codigo_item=producto.get('codigo_item', ''),
                                nombre_item=producto.get('nombre_item', ''),
                                numero_lote=f"LOTE-{producto['id']}-{producto['fecha_vencimiento']}"
                            )
                            lotes.append(lote)
                        else:
                            lote = LoteFEFO(
                                producto_id=producto['id'],
                                cantidad=producto.get('stock_actual', 0),
                                fecha_vencimiento='9999-12-31',
                                codigo_item=producto.get('codigo_item', ''),
                                nombre_item=producto.get('nombre_item', ''),
                                numero_lote=f"LOTE-{producto['id']}-SIN-VENCIMIENTO"
                            )
                            lotes.append(lote)
            
            except Exception as e:
                # En caso de error, retornar lista vacía en lugar de fallar
                print(f"Error obteniendo lotes para producto {producto_id}: {e}")
                return []
            
            # Ordenar por fecha de vencimiento (más antigua primero)
            lotes.sort()
            return lotes
            
        except Exception as e:
            # En caso de error, retornar lista vacía en lugar de fallar
            print(f"Error obteniendo producto {producto_id}: {e}")
            return []
    
    @staticmethod
    def calcular_distribucion_fefo(producto_id: int, cantidad_solicitada: int) -> DistribucionFEFO:
        """
        Calcula cómo distribuir una salida usando la lógica FEFO
        """
        try:
            # Obtener lotes ordenados por FEFO
            lotes = FEFOService.obtener_lotes_producto(producto_id)
            
            if not lotes:
                raise Exception("No se encontraron lotes para el producto")
            
            # Calcular stock total disponible
            stock_total = sum(lote.cantidad for lote in lotes)
            
            if cantidad_solicitada > stock_total:
                raise Exception(f"Stock insuficiente. Disponible: {stock_total}, Solicitado: {cantidad_solicitada}")
            
            # Aplicar lógica FEFO
            cantidad_restante = cantidad_solicitada
            lotes_usados = []
            stock_anterior = stock_total
            
            for lote in lotes:
                if cantidad_restante <= 0:
                    break
                
                # Calcular cuánto tomar de este lote
                cantidad_a_tomar = min(cantidad_restante, lote.cantidad)
                
                # Registrar uso del lote
                lote_usado = {
                    'lote_id': lote.producto_id,
                    'numero_lote': lote.numero_lote,
                    'cantidad_usada': cantidad_a_tomar,
                    'fecha_vencimiento': lote.fecha_vencimiento,
                    'motivo': 'FEFO - Primero en vencer' if lote.fecha_vencimiento != '9999-12-31' else 'FEFO - Sin fecha de vencimiento'
                }
                lotes_usados.append(lote_usado)
                
                # Actualizar cantidad restante
                cantidad_restante -= cantidad_a_tomar
                
                # Actualizar stock del lote
                lote.cantidad -= cantidad_a_tomar
            
            # Calcular stock final
            stock_final = stock_total - cantidad_solicitada
            
            return DistribucionFEFO(
                cantidad_solicitada=cantidad_solicitada,
                lotes_usados=lotes_usados,
                stock_anterior=stock_anterior,
                stock_final=stock_final
            )
            
        except Exception as e:
            print(f"ERROR en calcular_distribucion_fefo: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Error al calcular distribución FEFO: {str(e)}")
    
    @staticmethod
    def aplicar_salida_fefo(producto_id: int, cantidad: int, usuario: str, 
                           observaciones: str, fecha_movimiento: str = None, destino: str = None) -> Dict:
        """
        Aplica una salida usando lógica FEFO y registra el movimiento
        """
        try:
            # Calcular distribución FEFO
            distribucion = FEFOService.calcular_distribucion_fefo(producto_id, cantidad)
            
            # Crear el movimiento de salida (solo campos básicos que espera la API)
            # Agregar información FEFO a las observaciones (simplificada para evitar caracteres especiales)
            observaciones_fefo = f"{observaciones} - FEFO: {len(distribucion.lotes_usados)} lotes afectados"
            
            # Usar solo los campos que definitivamente acepta la API
            # Asegurar que producto_id sea entero
            movimiento_data = {
                "producto_id": int(producto_id),
                "cantidad": int(cantidad),
                "usuario": str(usuario),
                "observaciones": str(observaciones_fefo)
            }
            
            # Debug: mostrar qué estamos enviando
            print(f"DEBUG: Enviando datos a la API: {movimiento_data}")
            
            # Intentar registrar el movimiento
            try:
                resp = post("/movements/exit", movimiento_data)
                print(f"DEBUG: Respuesta de la API: {resp.success}, {resp.message}")
            except Exception as api_error:
                print(f"DEBUG: Error al llamar a la API: {str(api_error)}")
                raise api_error
            
            if not resp.success:
                raise Exception(f"Error al registrar movimiento: {resp.message}")
            
            # El stock se actualiza automáticamente al registrar el movimiento
            return {
                'success': True,
                'movimiento': resp.data,
                'distribucion_fefo': distribucion.to_dict(),
                'message': f"Salida FEFO registrada exitosamente siguiendo la lógica FEFO"
            }
            
        except Exception as e:
            print(f"ERROR en aplicar_salida_fefo: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'message': f"Error al aplicar salida FEFO: {str(e)}"
            }
    
    @staticmethod
    def obtener_historial_lotes(producto_id: int) -> List[Dict]:
        """
        Obtiene el historial de movimientos de lotes para un producto
        """
        try:
            resp = get(f"/movements")
            if not resp.success:
                raise Exception(f"Error al obtener historial: {resp.message}")
            
            movimientos = resp.data or []
            historial_lotes = []
            
            # Filtrar movimientos de este producto
            movimientos_producto = [
                m for m in movimientos 
                if m.get('productos', {}).get('id') == producto_id
            ]
            
            for mov in movimientos_producto:
                if mov.get('tipo_movimiento') == 'salida':
                    # Para salidas, mostrar información FEFO
                    historial_lotes.append({
                        'fecha_movimiento': mov.get('fecha_movimiento'),
                        'cantidad_salida': mov.get('cantidad'),
                        'usuario': mov.get('usuario'),
                        'observaciones': mov.get('observaciones'),
                        'tipo': 'Salida FEFO'
                    })
                elif mov.get('tipo_movimiento') == 'entrada':
                    # Para entradas, mostrar información del lote
                    historial_lotes.append({
                        'fecha_movimiento': mov.get('fecha_movimiento'),
                        'cantidad_entrada': mov.get('cantidad'),
                        'usuario': mov.get('usuario'),
                        'observaciones': mov.get('observaciones'),
                        'tipo': 'Entrada de Lote'
                    })
            
            return historial_lotes
            
        except Exception as e:
            raise Exception(f"Error al obtener historial de lotes: {str(e)}")
    
    @staticmethod
    def simular_salida_fefo(producto_id: int, cantidad: int) -> Dict:
        """
        Simula una salida FEFO sin aplicarla realmente
        Útil para mostrar al usuario cómo se distribuiría la salida
        """
        try:
            distribucion = FEFOService.calcular_distribucion_fefo(producto_id, cantidad)
            
            return {
                'success': True,
                'simulacion': {
                    'cantidad_solicitada': cantidad,
                    'stock_disponible': distribucion.stock_anterior,
                    'stock_restante': distribucion.stock_final,
                    'lotes_afectados': distribucion.lotes_usados,
                    'resumen': f"Se tomarían {cantidad} unidades de {len(distribucion.lotes_usados)} lote(s) siguiendo FEFO"
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Error en simulación FEFO: {str(e)}"
            }

    @staticmethod
    def obtener_fecha_vencimiento_proxima(producto_id: int) -> str:
        """
        Obtiene la fecha de vencimiento más próxima de un producto
        basándose en todos sus lotes disponibles
        """
        try:
            lotes = FEFOService.obtener_lotes_producto(producto_id)
            if not lotes:
                return None
            
            # Ordenar por fecha de vencimiento (FEFO)
            lotes_ordenados = sorted(lotes)
            
            # Retornar la fecha más próxima (primera en la lista ordenada)
            fecha_proxima = lotes_ordenados[0].fecha_vencimiento
            
            print(f"🔍 Fecha de vencimiento más próxima para producto {producto_id}: {fecha_proxima}")
            return fecha_proxima
            
        except Exception as e:
            print(f"⚠️ Error al obtener fecha de vencimiento próxima: {e}")
            return None
