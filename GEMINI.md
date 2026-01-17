Project Analysis: MediStock Core

  ---

  1. Project Purpose & Business Model

  Project Purpose:

   * MediStock Core is an ETL (Extract, Transform, Load) pipeline
     and backend system designed to modernize legacy healthcare
     operations for a clinic.
   * The primary goal is to solve the critical business problem of
     transforming unstructured, inconsistent historical data from
     Excel spreadsheets into a normalized, ACID-compliant PostgreSQL
     Data Warehouse.
   * This structured data serves as the single source of truth for
     real-time inventory tracking, patient management, and business
     intelligence analytics.

  Business Model Supported:

  The project supports the core operations of a private medical
  clinic, likely one that performs aesthetic or specialized
  treatments. The key business activities are:

   * Patient Management: The system manages a central registry of
     patients, tracking their identity and history. A key feature is
     the "Heuristic Identity Reconstruction" to backfill missing
     patient IDs from legacy data, which is crucial for data

     integrity.
   * Medical Consultations: The system records medical appointments,
     the services performed during those appointments, and the total
     cost. This forms the transactional core of the clinic's
     business.
   * Inventory and Stock Control: The clinic uses medical supplies
     (e.g., "Botox 50u", "Syringes 3ml"). The system extracts this
     information from unstructured text to enable precise stock
     tracking, manage inventory movements (entradas/salidas), and
     maintain a real-time view of stock levels. This is critical for
     avoiding stockouts and managing costs.
   * Financials: The system infers financial transactions (debts and
     payments) from unstructured notes, providing a clearer
     financial picture.

  In essence, MediStock Core acts as a lightweight, custom-built ERP
  (Enterprise Resource Planning) system for a clinic, centralizing
  its patient, clinical, and inventory data to improve operational
  efficiency and enable data-driven decisions.

  ---
---

## Project Log

**2026-01-17 14:08:21**

*   **Commit:** `3a05da9`
*   **Feature:** Frontend Patient Management
*   **Details:**
    *   Added `actualizar_paciente` and `eliminar_paciente` methods to the `ApiClient` in `src/clinica_frontend/modules/api_client.py`.
    *   This change enables the frontend application to update and delete patient records via the backend API.
    *   This is a key step towards providing full CRUD (Create, Read, Update, Delete) functionality for patient management in the user interface.