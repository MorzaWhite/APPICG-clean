# System Architecture

## 1. High-Level Overview

This project is a monolithic web application built with the Django framework. It follows a classic Model-View-Template (MVT) architecture, which is Django's variation of the Model-View-Controller (MVC) pattern.

-   **Model:** Manages the data and business logic. It interacts with the database.
-   **View:** Handles the user's requests and returns responses. It contains the logic for processing user input and rendering templates.
-   **Template:** The presentation layer, responsible for generating the HTML that is sent to the user's browser.

## 2. Component Breakdown

### 2.1. Django Application (`certificacion`)

This is the core of the project, containing all the business logic for managing gem certifications.

-   **`models.py`:** Defines the database schema through Django's ORM. This includes models for `Orden` (Order), `Item`, `Componente`, and other related data.
-   **`views.py`:** Contains the functions and classes that handle HTTP requests. This is where the main application logic resides, such as creating orders, advancing their status, and calculating delivery times.
-   **`forms.py`:** Defines the forms used for data validation and rendering HTML form elements. This ensures that user input is clean and valid before it is processed.
-   **`urls.py`:** Maps URL patterns to their corresponding views, directing incoming requests to the correct logic.
-   **`business_hours.py`:** A dedicated module for the complex logic of calculating the suggested delivery date, taking into account the laboratory's business hours and holidays.
-   **`decorators.py`:** Contains custom decorators, such as `@retry_on_db_lock`, to add reusable functionality to views.

### 2.2. Templates (`templates/`)

The HTML templates are responsible for the user interface.

-   **`base.html`:** The main layout template, which all other templates extend. It includes the common header, footer, and navigation.
-   **`crear_orden.html`:** A complex template that implements the multi-step wizard for creating a new order. It contains a significant amount of JavaScript to handle the wizard's state, form validation, and AJAX calls.
-   **`ver_orden.html`:** Displays the details of a specific order, including its items and current status.

### 2.3. Static Files (`static/`)

This directory contains the static assets for the frontend.

-   **CSS:** Stylesheets for the application's appearance.
-   **JavaScript:** Custom scripts for interactive features, such as the "Add Item" modal and dynamic UI updates.
-   **Images:** Static images used in the UI.

### 2.4. Media Files (`media/`)

This directory is used to store user-uploaded files, such as QR codes and photos of the gems.

### 2.5. Database

The application uses SQLite as its database, which is suitable for development and small-scale deployments. For production, it is recommended to switch to a more robust database like PostgreSQL.

## 3. Data Flow

1.  A user's browser sends an HTTP request to the application.
2.  Django's URL router (`urls.py`) matches the request's URL to a specific view in `views.py`.
3.  The view processes the request. This may involve:
    -   Reading data from the database through the models (`models.py`).
    -   Validating user input with forms (`forms.py`).
    -   Performing business logic calculations (e.g., `business_hours.py`).
    -   Writing new data to the database.
4.  The view then renders an HTML template (`templates/`), passing it any necessary data.
5.  The rendered HTML is sent back to the user's browser as the HTTP response.
