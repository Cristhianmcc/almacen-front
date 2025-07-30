import unittest
from services.api import get, post, put, delete

class TestProductosAPI(unittest.TestCase):
    def test_get_all(self):
        resp = get("/products")
        self.assertTrue(resp.success)
        self.assertIsInstance(resp.data, list)

    def test_create_and_delete(self):
        # Crear producto de prueba con los campos y nombres exactos del modelo Java
        producto = {
            "codigo_item": "TEST123PY",
            "nombre_item": "Producto Test Python",
            "nombre_marca": "MarcaTest",
            "orden_compra": "OC-999",
            "nombre_medida": "UND",
            "mayor": 10.5,
            "sub_cta": "SUB-1",
            "stock_actual": 5,
            "estado": "activo"
        }
        try:
            resp = post("/products", producto)
        except Exception as e:
            # Intentar obtener el mensaje de error del backend
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print("\n[BACKEND ERROR MESSAGE]", e.response.json())
                except Exception:
                    print("\n[BACKEND ERROR RAW]", e.response.text)
            raise
        self.assertTrue(resp.success, msg=f"POST error: {resp.message}")
        prod_creado = resp.data
        self.assertIsInstance(prod_creado, dict)
        prod_id = prod_creado.get("id") or prod_creado.get("id_producto")
        # Eliminar producto
        del_resp = delete(f"/products/{prod_id}")
        self.assertTrue(del_resp.success, msg=f"DELETE error: {del_resp.message}")

if __name__ == "__main__":
    unittest.main()
