# API and URL Endpoints

This document provides a comprehensive list of all URL endpoints in the SGICG application, along with their purpose, allowed HTTP methods, and a brief description.

## 1. Main Application URLs (`/`)

These are the primary user-facing pages for navigating and using the application.

-   **`/` (Dashboard)**
    -   **View:** `certificacion.views.dashboard`
    -   **Methods:** `GET`
    -   **Description:** The main dashboard of the application, displaying a summary of all orders and their current status.

-   **`/orden/crear/` (Create Order)**
    -   **View:** `certificacion.views.CrearOrdenView`
    -   **Methods:** `GET`, `POST`
    -   **Description:** A multi-step wizard for creating a new certification order. The `GET` request displays the initial form, while the `POST` request handles the form submission and order creation.

-   **`/orden/ver/<int:orden_id>/` (View Order)**
    -   **View:** `certificacion.views.ver_orden`
    -   **Methods:** `GET`
    -   **Description:** Displays the detailed information for a specific order, identified by `orden_id`. This includes the order's items, current status, and history.

-   **`/orden/<int:orden_id>/avanzar/` (Advance Order Status)**
    -   **View:** `certificacion.views.avanzar_etapa`
    -   **Methods:** `POST`
    -   **Description:** Advances the order to the next stage in the certification workflow. This endpoint is typically called via a button on the "View Order" page.

-   **`/orden/<int:orden_id>/subir_qr/` (Upload QR Code)**
    -   **View:** `certificacion.views.subir_qr`
    -   **Methods:** `POST`
    -   **Description:** Handles the upload of a QR code image for a specific order.

-   **`/orden/item/<int:item_id>/subir_foto/` (Upload Item Photo)**
    -   **View:** `certificacion.views.subir_foto`
    -   **Methods:** `POST`
    -   **Description:** Handles the upload of a photo for a specific item within an order.

-   **`/orden/item/<int:item_id>/` (View Item - Placeholder)**
    -   **View:** `certificacion.views.ver_item`
    -   **Methods:** `GET`
    -   **Description:** A placeholder view for displaying the details of a single item. This is not fully implemented.

## 2. Configuration URLs (`/configuracion/`)

These URLs are for managing the application's settings and configuration.

-   **`/configuracion/` (Configuration Page)**
    -   **View:** `certificacion.views.configuracion_tiempos`
    -   **Methods:** `GET`, `POST`
    -   **Description:** A page for setting the estimated time required for each type of item and process. The `GET` request displays the current settings, while the `POST` request saves any changes.

## 3. API Endpoints (`/api/`)

These endpoints are designed to be called via AJAX from the frontend to provide dynamic functionality.

-   **`/api/calcular_fecha_sugerida/` (Calculate Suggested Delivery Date)**
    -   **View:** `certificacion.views.api_calcular_fecha_sugerida`
    -   **Methods:** `POST`
    -   **Description:** Calculates the suggested delivery date for an order based on the items it contains. It expects a JSON payload with a list of item types and quantities. This is called from the "Create Order" page.
    -   **Payload Example:**
        ```json
        {
          "items": [
            { "tipo": "tipo_gema", "cantidad": 1 },
            { "tipo": "tipo_joya", "cantidad": 2 }
          ]
        }
        ```
    -   **Response Example:**
        ```json
        {
          "fecha_sugerida": "2025-10-28T14:30:00"
        }
        ```

-   **`/api/check_order_number/` (Check Order Number)**
    -   **View:** `certificacion.views.check_order_number`
    -   **Methods:** `GET`
    -   **Description:** Checks if a given order number already exists in the database. This is used for real-time validation on the "Create Order" form.
    -   **Query Parameter:** `numero_orden`
    -   **Response Example:**
        ```json
        {
          "exists": true
        }
        ```
