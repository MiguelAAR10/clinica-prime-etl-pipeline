# src/clinica_backen/app/services/inventario_service.py

from app.extensions import db
from app.models.inventario import MovimientoStock
from app.models.producto import Producto

class InventarioService:
    """
    Orquestador Logistico
    ---------------------
    Su Trabajo es validar las reglas del negocio y registrar el hecho.
    Confia en que los Triggers de PostgreSQL actualizaran el stock_actual.
    """
    
    @staticmethod
    def registrar_movimiento_manual(data):
        """
        Procesa una ENTRADA (Compra) o Salida (Ajuste/Merma) manual
        """
        
        # 1. Existe el Producto?
        producto = Producto.query.get(data['id_producto'])
        if not producto:
            raise ValueError(f"Producto ID {data['id_producto']} no existe en el Catalogo")
        
        tipo  = data['tipo_movimiento']
        
        cantidad = float(data['cantidad'])
        
        # 2. Validacion de Negocio (Stock Negativo)
        
        # Aunque la DB podria protegerse es mejor validar aqui para dar un mensaje clato al usaurio antes de fallar
        if tipo == 'SALIDA':
            if producto.stock_actual < cantidad: 
                raise ValueError(f"Stock Insufiente. Tienes {producto.stock_actual}, intentas sacar {cantidad}")
        
        # 3. Registrar el Hecho (Solo Insertamos en movimientos_stock
        # No Tocamos la Tabla de Porductos Manualmente
        nuevo_movimiento = MovimientoStock(
            id_producto = data ['id_producto'],
            tipo_movimiento = tipo,
            cantidad = data['cantidad']
        )
        
        try:
            db.session.add(nuevo_movimiento)
            db.session.commit()
            
            # Refrescar la Memoria (Paso Critico)
            # El Trigger de SQL ya corrio en milisegundos y actualizo el producto 
            # Pero python tiene la fotografia vieja del porducto en Memoria
            # 'refresh' obliga a Python a pedirle los Datos Frescos a la DB
            
            db.session.refresh(producto)
            db.session.refresh(nuevo_movimiento)
            
            return nuevo_movimiento
        
        except Exception as e:
            db.session.rollback()
            raise e 
    
    @staticmethod
    def obtener_kardex(id_producto):
        """ Devuelve la Histotia comple de un producto"""
        return MovimientoStock.query.filter_by(
            id_producto = id_producto
        ).order_by(
            MovimientoStock.fecha_movimiento.desc()
        ).all()
        
        