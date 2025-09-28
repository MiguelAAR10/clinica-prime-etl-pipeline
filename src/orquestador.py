# ======================================================================
# MIGRATION ORCHESTRATOR
# Misión: Aplicar cambios ESTRUCTURALES a la base de datos de forma
# secuencial, robusta y reproducible.
# Herramienta Principal: psql (por su poder y fiabilidad con DDL).
# ======================================================================
import sys
import subprocess
from pathlib import Path
import argparse

# --- PASO 1: Carga Centralizada de Secretos ---
# Importamos la función desde tu archivo hidden.py.
# Esto centraliza la gestión de credenciales, lo cual es excelente.
from hidden import secret_credentials

def cargar_configuracion():
    """Carga las credenciales de la base de datos desde hidden.py."""
    print("  -> 🔑 Cargando credenciales...")
    try:
        secrets = secret_credentials()
        # Creamos un diccionario de configuración limpio para usarlo en todo el script.
        config = {
            "user": secrets['user'],
            "password": secrets['password'],
            "host": secrets['host'],
            "port": secrets['port'],
            "database": secrets['database']
        }
        print("     ✅ Credenciales cargadas con éxito.")
        return config
    except Exception as e:
        print(f"     ❌ ¡FALLO CATASTRÓFICO! No se pudieron cargar las credenciales desde hidden.py.")
        print(f"     Error: {e}")
        # Si no podemos conectarnos a la DB, el programa no puede continuar.
        print(f"--- ❌ Error inesperado: {e}")
        sys.exit(1)

# --- PASO 2: El Motor de Ejecución (Función Pura) ---
# Esta función tiene UNA responsabilidad: ejecutar un archivo SQL.
def ejecutar_plano_sql(sql_path: Path, db_config: dict):
    """
    Ejecuta un único script SQL usando el comando psql del sistema.
    
    Args:
        sql_path: La ruta al archivo .sql a ejecutar.
        db_config: Un diccionario con las credenciales de la base de datos.
    """
    print(f"  -> 🏛️ Forjando plano de migración: {sql_path.name}...")
    
    # Comprobación de seguridad: asegúrate de que el archivo existe antes de intentar ejecutarlo.
    if not sql_path.is_file():
        print(f"     ❌ ¡ERROR CRÍTICO! El archivo de plano no existe en la ruta: {sql_path}")
        # Lanzamos una excepción para detener el proceso inmediatamente.
        raise FileNotFoundError(f"Archivo de migración no encontrado: {sql_path}")
        
    try:
        # Construimos el comando psql.
        command = [
            'psql',
            '--username', db_config['user'],
            '--dbname', db_config['database'],
            '--host', db_config['host'],
            '--port', str(db_config['port']),
            '--file', str(sql_path),
            '--single-transaction' # ¡MAGIA! Ejecuta el archivo entero dentro de una transacción.
                                   # Si algo falla, se revierte todo el archivo automáticamente.
        ]
        
        # El entorno para pasar la contraseña de forma segura.
        env = {'PGPASSWORD': db_config['password']}
        
        resultado = subprocess.run(
            command,
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"     ✅ Éxito: {sql_path.name} forjado e integrado en el Templo.")
        
    except subprocess.CalledProcessError as e:
        print(f"     ❌ ¡FALLO CATASTRÓFICO! La migración {sql_path.name} ha fallado.")
        print("     --- INICIO DEL REPORTE DE ERROR DE POSTGRESQL ---")
        # El error de psql es muy informativo y nos dirá exactamente qué línea falló.
        print(e.stderr)
        print("     --- FIN DEL REPORTE DE ERROR ---")
        raise e

# --- PASO 3: El Orquestador Principal (El Cerebro) ---
if __name__ == "__main__":
    # --- Definición de la Estrategia de Migración ---
    RUTA_MIGRACIONES = Path('src/sql/migrations')
    
    # La lista maestra de migraciones. EL ORDEN ES LA LEY.
    # Esta es la única parte que necesitarás editar en el futuro cuando añadas nuevas misiones.
    PLANOS_DE_MIGRACION = [
        RUTA_MIGRACIONES / '001_stock_ledger_trigger.sql',
        RUTA_MIGRACIONES / '002_stock_ledger_sync.sql',
        RUTA_MIGRACIONES / '003_sp_register_entrada.sql', 
        RUTA_MIGRACIONES / '004_backfill_historical_data.sql'
    ]

    print("--- ⚔️ INICIANDO RITUAL DE MIGRACIÓN DEL TEMPLO DE DATOS ⚔️ ---")
    
    # Cargamos la configuración una sola vez al inicio.
    config_db = cargar_configuracion()
    
    try:
        print("\n--- Aplicando migraciones estructurales en secuencia... ---")
        # Iteramos sobre nuestra lista maestra y ejecutamos cada plano.
        for plano in PLANOS_DE_MIGRACION:
            ejecutar_plano_sql(plano, config_db)
        
        print("\n--- ✅ ¡RITUAL DE MIGRACIÓN FINALIZADO! El Templo ha evolucionado. ---")
        
    except Exception:
        print("\n--- ❌ ¡LA EVOLUCIÓN HA FALLADO! El Templo puede estar en un estado inconsistente. Revisa el error. ---")
        sys.exit(1)