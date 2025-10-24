# SGICG - Sistema de Gestión de Certificados

## Overview

This project is a Django-based web application designed to manage the workflow of a gem certification laboratory. It allows users to create orders, add items (gems or jewelry) to be certified, and track the progress of each item through the various stages of the certification process.

## Features

-   **Order Management:** Create and track certification orders.
-   **Item Management:** Add multiple items to an order, each with its own specific details.
-   **Workflow Tracking:** Monitor the progress of each order through a series of stages: Ingreso, Fotografía, Revisión, and Impresión.
-   **Dynamic Time Calculation:** The system automatically estimates the delivery date for each order based on the items it contains and the laboratory's business hours.
-   **File Management:** Upload and associate QR codes and professional photos with each item.

## Quickstart

### Prerequisites

-   Python 3.12 or higher
-   pip

### Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://localhost:8000`.
