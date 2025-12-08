# src/clinica_backend/app/services/catalogo_service

#-------------------------------------------------------------------------------
# SERVICE LAYER  - LOGICA DEL NEGOCIO/ REGLAS DEL NEGOCIO
#-------------------------------------------------------------------------------

# ======================================================================================================
# PARTE 1: IMPORTACIONES
# ======================================================================================================

from app.extensions import db
    # Objetoo SQLAlchemy ya inicialzado en Flask
    #   - Contiene: (Conexiones DB, Session Manger, Mapear ORM)
    #   - Recibe = add
    #   - Confirmar Transaccion = commit
    #   - Revertir Transaccion tras error = rollback
    
from app.models.producto import Producto
from app.models.marca import Marca 
from app.models.servicio import Servicio
    # Modelos: son las definciones de como luce un table en PostgreSQL
    # Cada Modelo  es una Clase que:
    #   - Repreenta un trabal
    #   - Tiene Columnas 
    #   - Tiene Tipos
    #   = Tiene Claves Primarias
    #   = Tiene Relaciones
    
from sqlalchemy import IntegrityError
    # Importa el error que ocurre cuando rompes reglas de BD 
    #   Ejemplo: INsertar duplicados, violar Claves Foraneas , insert null donde no debe
# ======================================================================================================


# ======================================================================================================
# PARTE 2: DEFINICION DE LA CLASE
# ======================================================================================================

class CatalogoService: 
    # Modulo que Contiene toda la logica del negocio dle Catalogo
    #   - Creacion de Marcas
    #   - Creacion de Productos
    #   - Listados 
    #   - Validaciones 
    #   - NO habla (HTTP, No recibe Request, No retonra JSON)
    
    # --------------------------- MARCAS ---------------------------------------
    @staticmethod # No necesitamos instanciar la Lcase 
    def crear_marca(data):
        
        # Verificar que no existe la Marca
        if Marca.query.filter_by(nombre_marca = ['nombre_marca']).first():
            # `filter_by` = 'SELECT * FROM marca WHERE nombre_marca = ?'
            raise ValueError(f"La Marca f{data['nombre_marca']} ya existe.")
        
        nueva_marca = Marca(**data)
        # Desempacado de parametros  
        
        # TRANSACCION SQL 
        # Realiar la inserrcion a la Base De Datos uso de SQLAlchemy
        try:
            db.session.add(nueva_marca)
            db.session.commit()
            return nueva_marca
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def listar_marcas(): 
        # `SQL`: 'SELECT * FROM marca ORDER BY nombre_marca
        return Marca.query.order_by(Marca.nonombre_marca).all()
    
    @staticmethod
    def crear_producto(data):
        # Regla 1: Cad prodcuto debe Corresponder a Una Marca (id)
        marca_id = data.get('id_marca')
        if not Marca.query.get(marca_id):
            # Get permite Busca en un diccionario en Python 
            raise ValueError(f"La Marca con ID {marca_id} no existe.")
        
        # TRANBSACCION SQL
        
        nuevo_producto = Producto(**data)
        try:
            db.session.add(nuevo_producto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def listar_productos():
        # `SQL`: 'SELECT * FROM producto ORDER BY nombre_producto
        return Producto.query.order_by(Producto.nombre_producto).all() 
    
    # ============ SERVICIOS =====================================
    @staticmethod # No necesitamos instanciar la CLASE
    def crear_servicios(data):
        nombre = data.get('nombre_servicio')
        if Servicio.query.filter(Servicio.nombre_servicio.ilike(nombre)).first():
            raise ValueError(f"El Servicio '{nombre} ya existe")
        
        nuevo_servicio = Servicio(**data)
        
        try:
            db.session.add(nuevo_servicio)
            db.session.commit()
            return nuevo_servicio
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod 
    def listar_servicios(): 
        return  Servicio.query.order_by(Servicio.nombre_servicio.asc()).all()
    
            
