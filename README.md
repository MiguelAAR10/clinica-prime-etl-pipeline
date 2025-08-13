# 🏛️ Proyecto ETL: Clínica Prime

**Versión 1.0.0**

## 🎯 1. Resumen Ejecutivo 

Este proyecto implementa un pipeline de ETL (Extract, Transform, Load) robusto y modular, construido en Python con la librería Pandas. Su misión es ingerir, limpiar, transformar y consolidar los registros históricos de pacientes y consultas de la Clínica Prime, que actualmente residen en un archivo Excel multi-hoja con una estructura inconsistente y datos de baja calidad. El destino final de los datos limpios es una base de datos PostgreSQL relacional, sentando las bases para futuras iniciativas de Business Intelligence y análisis de negocio.

---

## 🗺️ 2. Arquitectura del Pipeline

El pipeline sigue una arquitectura ETL (Extract-Transform-Load) modular, donde la lógica de limpieza y transformación se encapsula en un taller de herramientas reutilizables (`limpieza_utils.py`) y es orquestada desde un notebook principal (`main.ipynb`).

```mermaid
graph TD;
    A[📄 Excel Crudo Múltiples Hojas] -->|1. Extracción| B 🐼 DataFrame Maestro en Pandas;
    B -->|2. Transformación en Cascada| C{⚙️ Pipeline de Limpieza};
    C -->|Lógica A| D[🔧 Estandarización de Esquema];
    C -->|Lógica B| E[🔧 Cirugía de Tipos de Datos];
    C -->|Lógica C| F[🔧 Reconstrucción de Identidades];
    C -->|Lógica D| G[🔧 Extracción de Características Notas];
    G --> H[📊 DataFrame Limpio y Consolidado];
    H -->|3. Carga| I🐘 Base de Datos PostgreSQL;
```

---

## 🛠️ 3. Stack Tecnológico

*   **Lenguaje Principal:** Python 3.10+
*   **Análisis y Manipulación de Datos:** Pandas
*   **Conectividad de Base de Datos:** SQLAlchemy, Psycopg2
*   **Base de Datos de Destino:** PostgreSQL
*   **Entorno de Desarrollo:** Jupyter Notebooks, Visual Studio Code

---

## 📂 4. Estructura del Proyecto

Un taller bien organizado es la clave para un proyecto mantenible.

```
/clinica-prime-etl-pipeline
│
├── data/
│   └── 📄 (Archivos de datos brutos y sensibles - IGNORADO POR GIT)
│
├── notebooks/
│   └── 📓 main.ipynb         # Puesto de Mando: Orquesta el pipeline completo.
│
├── src/
│   └── 🐍 limpieza_utils.py  # La Armería: Contiene todas las funciones de limpieza.
│
├── output/
│   └── 📈 (Resultados, CSVs limpios, gráficos - IGNORADO POR GIT)
│
├── .gitignore               # El Manto de Invisibilidad
└── README.md                # El Alma del Proyecto (este archivo)
```

---

## 🚀 5. Instrucciones de Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone git@github.com:TuUsuario/clinica-prime-etl-pipeline.git
    cd clinica-prime-etl-pipeline
    ```
2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar las dependencias:**
    ```bash
    pip install pandas numpy sqlalchemy psycopg2-binary openpyxl
    ```
4.  **Configurar los Datos:** Colocar el archivo `clientes_work.xlsx` dentro de la carpeta `data/`.
5.  **Ejecutar el Pipeline:** Abrir `notebooks/main.ipynb` y ejecutar las celdas en orden.

---

## 🧠 6. Lógica de Negocio y Decisiones de Limpieza Clave

*   **Reconstrucción de Identidad:** Se implementó un sistema de "mapa de la verdad" para rellenar DNI y nombres de pacientes faltantes, maximizando la retención de datos.
*   **Inferencia de Contexto en 'Deuda':** Se utiliza una expresión regular con `negative lookbehind` (o una estrategia de dos pasos) para diferenciar entre la creación de una deuda y el pago de una deuda existente.
*   **Extracción de Características de 'Notas':** Se aplican `regex` para extraer datos estructurados (Unidades, Jeringas, etc.) de la columna de texto libre `notas`.
