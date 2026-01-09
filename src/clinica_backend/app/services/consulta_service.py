# src/clinica_backend/app/services/consulta_service.py

from app.extensions import db
"""
¿QUÉ ES 'db'?
-------------
Es la instancia de SQLAlchemy configurada para tu app.

ANALOGÍA: El Conductor del Autobús
-----------------------------------
- db = El conductor que sabe cómo llevar datos a la DB
- db.session = El autobús que transporta las operaciones
- db.session.add() = Subir pasajero al autobús
- db.session.commit() = Arrancar el viaje
- db.session.rollback() = Dar vuelta atrás

¿POR QUÉ NO IMPORTAR SQLAlchemy DIRECTAMENTE?
---------------------------------------------
Porque necesitas UNA instancia compartida por toda la app.

En extensions.py:
    db = SQLAlchemy()

En __init__.py:
    db.init_app(app)
mTodos usan el MISMO 'db'.
"""

from app.models.consulta import Consulta, ConsultaServicio, ConsumoProducto
from app.models.paciente import Paciente
from app.models.servicio import Servicio
from app.models.producto import Producto

# ------------------------------------
# CLASE DEL SERVICIO 
# ------------------------------------

class ConsulaService:
    """
    Servicio para manejar operaciones relacionadas con consultas medicas 
    
    Patron: Serice Layer (Capa de Service)
    Responsabilidades: 
    - Validar reglas de Negocio
    - Orquestar Operaciones complejas
    - Centralizar logica Reutilizable
    """
    @staticmethod
    def crear_consulta_completa(data):
        """
        Crear una consulta Medica Completa con sus Servicios y consumos.
        Maneja la Transaccion Atomica
        
        Args:
            data (dict): Datos Validados del Schema
            
        Returns:
            Consulta: Objeto de la consulta Creada
            
        Raises:
            ValueError: Si hay datos inavlidos
            Exception: Si hay error en la BD
        """
        paciente = Paciente.query.get(data['id_paciente'])
        """
        ¿QUÉ HACE query.get()?
        ----------------------
        Busca un registro por PRIMARY KEY.

        EQUIVALENTE SQL:
        SELECT * FROM pacientes WHERE id_paciente = ?;

        VENTAJAS SOBRE filter_by():
        - query.get(1) → Busca por PK (más rápido)
        - query.filter_by(id_paciente=1) → Busca general (más lento)

        ¿QUÉ DEVUELVE?
        --------------
        - Si existe: Objeto Paciente
        - Si no existe: None

        NO lanza excepción, solo devuelve None.
        """
        if not paciente: # Excepcion Python para Valores Invalidos - > mensaje Descriptivo
            # Devuelv 400 -> Bad Request al Frontend - db.session.rollback() se ejecuta automaticamente 
            raise ValueError(f"Paciente {data['id_paciente']} no existe")
        
        try:
            # A. Crear Cabecera
            consulta = Consulta(
                id_paciente = data["id_paciente"],
                notas_generales = data.get("notas_generales"),
                fecha_consulta = data.get("fecha_consulta") # Puede ser None(Usara Default)
                total_historico = 0 # Calcularemos esto Sumando
            )
            db.session.add(consulta)
            db.session.flush() # Para obtener el id_consulta generado
            total_acumulado = 0 
        
            """
            -------------------------------------
            Recuerda: load_instance=False en el schema.

            Schema devuelve dict, nosotros creamos el objeto.

            VENTAJA: Control total sobre la creación.

            ¿QUÉ ES data.get('notas_generales')?
            -----------------------------------
            dict.get(key, default=None)

            DIFERENCIA:
            - data['notas_generales'] → KeyError si no existe
            - data.get('notas_generales') → None si no existe

            ¿POR QUÉ total_historico=0?
            --------------------------
            Lo calcularemos sumando precios.
            Empezamos en 0 y vamos acumulando.
            """
            
            db.session.flush()
            """
            ¿QUÉ ES flush()?
            ----------------
            Ejecuta las operaciones PENDIENTES pero SIN confirmar la transacción.

            VENTAJAS:
            - Obtiene IDs generados (AUTO_INCREMENT)
            - Valida constraints (FK, etc.)
            - Pero puedes hacer rollback si quieres

            EJEMPLO:
            --------
            consulta = Consulta(...)
            db.session.add(consulta)
            db.session.flush()
            print(consulta.id_consulta)  # ¡Ya tiene ID generado!

            SIN flush():
            print(consulta.id_consulta)  # None (todavía no tiene ID)

            ¿POR QUÉ HACEMOS FLUSH AQUÍ?
            ---------------------------
            Necesitamos id_consulta para crear ConsultaServicio.
            """
            
            # B. Procesar Servicios
            for serv_data in data["servicios"]:
                # data["servicios"] Lista de Diccionarios, Cada uno representando un servicio
                ''' 
                EJEMPLO:
                [
                    {
                        "id_servicio": 5,
                        "precio_servicio": 500,
                        "productos_usados": [...]
                    },
                    {
                        "id_servicio": 8,
                        "precio_servicio": 100,
                        "productos_usados": [...]
                    }
                ]
                
                El loop procesa CADA servicio uno por uno.
                '''
                
                servicio_db = Servicio.query.get(serv_data["id_servicio"])
                if not servicio_db:
                    raise ValueError(f"Servicio {serv_data['id_servicio']} no existe")
                
                """
                MISMA LOGICA QUE CON PACIENTE
                - Verificar que existe antes de usar
                - Mejor Error temprano 
                """
                
                nuevo_servicio = ConsultaServicio(
                    id_consulta = consulta.id_consulta, 
                    id_servicio = serv_data ['id_servicio'],
                    precio_servicio= serv_data["precio_servicio"]
                )
                
                """
                Eleccion: Precio Servicio y NO precio del Catalago
                -------------------------------------------------
                    - El precio puede Variar a otras variables (Descuento Aplicado, etc.)
                """
                db.session.add(nuevo_servicio)
                db.session.flush() # Permite Obtenenr el `id_consulta_servicio` si es necesario
                
                total_acumulado += float(serv_data["precio_servicio"])
                
                """ 
                data["precio_servicio"] es Decimal (de Marshmallow). float lo convierte a numero para Sumar
                
                Seacumula el Total para poder Calcular el Total
                """
                
                # ===========================
                # PROCESAR CONSUMOS
                #   - productos usados
                # ===========================
                
                if 'productos_usados' in serv_data:
                    # Recuerda que productos_usdos es opcional en el Schema
                    # Si no hay productos, no procesamos consumos
                    for prod_data in serv_data["productos_usados"]:
                        # Validar Producto
                        producto_db = Producto.query.get(prod_data["id_producto"])
                        if not producto_db:
                            raise ValueError(f"Producto {prod_data['id_producto']} no existe")
                        
                        # VALIDACION DE STOCK (Seguridad Adicional)
                        cantidad = float(prod_data["cantidad_consumida"])
                        if producto_db.stock_actual < cantidad:
                            raise ValueError(f"Stock Insuficiente para {producto_db.nombre_producto}. Tienes {producto_db.stock_actual}, se requieren {cantidad}")
                        
                        importe = cantidad * float(prod_data['cantidad_consumida'])
                        # `importe` es el precio total por este consumo especifico
                        nuevo_consumo = ConsumoProducto(
                            id_consulta_servicio = nuevo_servicio.id_consulta_servicio, 
                            id_producto = prod_data['id_producto'],
                            cantidad_consumida = cantidad,
                            precio_producto = prod_data['precio_producto'],
                            importe_venta = importe
                        )
                        db.session.add(nuevo_consumo)
                        
            # ═══════════════════════════════════════════════════════════
            # PASO 5: FINALIZAR TRANSACCIÓN
            # ═══════════════════════════════════════════════════════════

            # D. Actualizar Total y Cerrar
            consulta.total_historico = total_acumulado
            db.session.commit()
            return consulta
        
        except Exception as e:
            db.session.rollback()
            raise e
        