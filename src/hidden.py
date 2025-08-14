# Guardar Credenciales aqui de Postgres por Sefuridad 

def secret_credentials():
    return{
        'host': 'localhost',
        'port': 5432, 
        'database' : 'clinica_prime',
        'user' :  'postgres',
        'password' : 'postgres'
    }