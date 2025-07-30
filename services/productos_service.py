from services.api import get, post, put, delete

# Obtener todos los productos
def get_all_products():
    resp = get("/products")
    if not resp.success:
        raise Exception(resp.message)
    return resp.data or []

# Obtener producto por ID
def get_product_by_id(id):
    resp = get(f"/products/{id}")
    if not resp.success:
        raise Exception(resp.message)
    return resp.data

# Crear producto (solo campos permitidos)
def create_product(producto):
    # No enviar campos automáticos ni nulos
    clean = {k: v for k, v in producto.items() if v is not None and k not in ["id", "fecha_ingreso", "created_at", "updated_at"]}
    resp = post("/products", clean)
    if not resp.success:
        raise Exception(resp.message)
    return resp.data

# Actualizar producto (solo campos editables)
def update_product(id, producto):
    editable = {k: v for k, v in producto.items() if k in [
        "codigo_item", "nombre_item", "nombre_marca", "orden_compra", "nombre_medida", "mayor", "sub_cta", "stock_actual", "fecha_vencimiento", "estado"
    ] and v is not None}
    resp = put(f"/products/{id}", editable)
    if not resp.success:
        raise Exception(resp.message)
    return resp.data

# Eliminar producto
def delete_product(id):
    resp = delete(f"/products/{id}")
    if not resp.success:
        raise Exception(resp.message)
    return resp.success

# Obtener productos con stock bajo
def get_low_stock_products():
    resp = get("/products/low-stock")
    if not resp.success:
        raise Exception(resp.message)
    return resp.data or []

# Obtener productos próximos a vencer
def get_expiring_products():
    resp = get("/products/expiring")
    if not resp.success:
        raise Exception(resp.message)
    return resp.data or []
