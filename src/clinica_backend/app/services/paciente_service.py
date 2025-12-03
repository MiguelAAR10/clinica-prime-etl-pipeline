# app/services/paciente_service.py
"""
Service Layer - Logica de Negocio para Paciente
FUNDAMENTO CS: Separación de Responsabilidades (Separation of Concerns)
¿Por qué un Service Layer?
1. ORGANIZACIÓN: Mantiene la lógica de negocio separada de rutas y modelos.
2. REUTILIZACIÓN: Permite reutilizar lógica en diferentes partes de la app.
3. MANTENIBILIDAD: Facilita pruebas y cambios en la lógica sin afectar otras
"""

from app.extensions import db
# Importamos modelos explícitamente para evitar confusión
from app.models.paciente import Paciente 
from app.models.distrito import Distrito
from sqlalchemy.exc import IntegrityError

class PacienteService:
    """
    Service Layer para operaciones de Paciente
    - Usa @staticmethod, por lo que actua como un "namespace"
    o "caja de Herramientas" Para la logica de Negocio relacionada con Paciente
    
    Arquitectura
    - Recibe Dicts (Python): snake_case del Guardian Schema
    - Devuelve Objetos de la Despensa (Modelos ORM) Al Mesero Routes
    """

    @staticmethod
    def crear_paciente(data):
        """
        Crea un Nuevo Paciente.
        
        Args:
            data (dict): Datos del Paciente (Ya Validados y en snake case)
        """
        
        # Regla de Negocio N1: Verificar que DNI no Exista
        if Paciente.buscar_por_dni(data.get('dni')):
            raise ValueError(f"Ya Existe un Paciente con ese DNI {data.get('dni')}")
        
        # Regla de Neocio N2: Verificar Distrito Existe
        if data.get('id_distrito'):
            if not Distrito.query.get(data.get('id_distrito')):
                raise ValueError(f"Distrito con id {data.get('id_distrito')} no Existe")

        # 3. Creacion de Objeto
        
        #---------------------------------------------------------------------------------------
        # TECNICA DE ARQUITECTO: DESEMPAQUETADO DE DICCIONARIO (DICT UNPACKING)
        #---------------------------------------------------------------------------------------
        #
        # En lugar de esto (manual y frágil):
        # paciente = Paciente(
        #     nombre_completo=data.get('nombre_completo'),
        #     dni=data.get('dni'),
        #     ...
        # )
        #
        # Usamos esto:
        # El operador (**) toma tu diccionario 'data' y lo
        # "desempaqueta" como argumentos para el constructor.
        #
        # Paciente(**data) es idéntico a:
        # Paciente(nombre_completo='Ana', dni='123', ...)
        #
        # Esto funciona *SOLO PORQUE* nuestro Schema (Guardián)
        # ya tradujo 'nombreCompleto' a 'nombre_completo'.
        # ¡Arquitectura Limpia en acción!

        paciente = Paciente(**data)
        
        # 3. Persistencia (El Chef controla la cocina)
        try:
            db.session.add(paciente) # Poner en la olla
            db.session.commit()      # ¡Cocinar! (Commit)
            return paciente
        except IntegrityError as e:
            db.session.rollback()    # ¡Apagar fuego!
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def obtener_paciente(id_paciente):
        """
        Obtiene un Paciente por su ID.
        
        Args:
            id_paciente (int): ID del Paciente
        Returns:
            Paciente o None si no existe
        """
        return Paciente.query.get(id_paciente)
    
    @staticmethod
    def listar_pacientes(page=1, per_page=20, search=None, distrito_id=None):
        """
        Lista Pacientes con paginación y filtros.
        IMPORTANTE: En la ruta (Controller) debes llamar a este método exactamente así:
        PacienteService.listar_pacientes(...)
        """
        query = Paciente.query
        
        # Filtro de Búsqueda (Nombre o DNI)
        if search:
            query = query.filter(
                (Paciente.nombre_completo.ilike(f'%{search}%')) | 
                (Paciente.dni.ilike(f'%{search}%'))
            )
        
        # Filtro por Distrito
        if distrito_id:
            query = query.filter_by(id_distrito=distrito_id)
        
        # Ordenamiento por defecto
        query = query.order_by(Paciente.nombre_completo.asc())
        
        # Paginación
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }
    
    @staticmethod
    def actualizar_paciente(id_paciente, data):
        paciente = Paciente.get_by_id(id_paciente)
        if not paciente:
            raise ValueError("Paciente no encontrado")

        # Validar cambio de DNI
        nuevo_dni = data.get('dni')
        if nuevo_dni and nuevo_dni != paciente.dni:
            if Paciente.buscar_por_dni(nuevo_dni):
                raise ValueError(f"El DNI {nuevo_dni} ya está en uso")

        paciente.update(data)

        try:
            db.session.commit()
            return paciente
        except Exception as e:
            db.session.rollback()
            raise e
    
    
    @staticmethod
    def eliminar_paciente(id_paciente):
        """ 
        Elimina un Paciente (Hard Delete)
        
        Args:
            id_paciente (int): ID del Paciente
        """
        
        paciente = PacienteService.obtener_paciente(id_paciente)
        if not paciente:
            raise ValueError(f"Paciente con ID {id_paciente} no encontrado")
        
        # Tu Modelo 'to_dict' maneja la serializacion 
        # Pero Cuidado El servicio no deberia sevolver dicts
        # sino objetos.El Mesero (Route) debe serializar
        # CORRECCIÓN DE ARQUITECTURA: El servicio devuelve
        # los datos crudos (objetos).
        
        # futuras_consultas = Consulta.query...filter_by(
        
        try:
            # --- CORRECCIÓN DE BUG ---
            # Antes devolvías un diccionario, ahora ELIMINAMOS de verdad.
            db.session.delete(paciente)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            # Probablemente error de Foreign Key (tiene consultas asociadas)
            raise ValueError(f"No se puede eliminar: {str(e)}")     
        