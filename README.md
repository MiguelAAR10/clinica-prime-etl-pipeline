# 🏥 MediStock Core: Clinical Data Pipeline & ERP

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Ops-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)

## 🎯 Executive Summary

**MediStock Core** is a robust **ETL (Extract, Transform, Load)** pipeline and backend system designed to modernize legacy healthcare operations. 

The project addresses a critical business problem: transforming unstructured, inconsistent historical data (Excel spreadsheets) into a normalized, ACID-compliant **PostgreSQL Data Warehouse**. This system serves as the foundation for real-time inventory tracking, patient management, and business intelligence analytics.

---

## 🗺️ Architecture Overview

The system follows a modular architecture where data cleaning logic is decoupled from the ingestion layer. It utilizes a **"Taller" pattern** (utility workshop) to handle complex data transformation before loading it into the transactional database.

```mermaid
graph TD;
    A[📄 Raw Legacy Excel Data] -->|1. Ingestion| B(Pandas Staging Engine);
    B -->|2. Transformation Pipeline| C{Data Cleaning Logic};
    C -->|Schema Standardization| D[Strict Type Enforcement];
    C -->|Heuristics| E[Identity Reconstruction Map];
    C -->|NLP / Regex| F[Feature Extraction from Notes];
    F --> G[✅ Cleaned & Consolidated Data];
    G -->|3. Transactional Load| H[(PostgreSQL Warehouse)];
    H <-->|4. API Layer| I[Flask Backend API];
```

