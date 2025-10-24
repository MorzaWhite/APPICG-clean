# TODO / Improvement Plan

This document outlines the planned improvements and features for future versions of the SGICG application.

## High Priority

-   **Switch to PostgreSQL:** Replace the SQLite database with PostgreSQL for the production environment to improve concurrency and prevent `database is locked` errors.
-   **User Authentication:** Implement a robust user authentication and authorization system to control access to different parts of the application.
-   **Production Deployment:** Create a comprehensive deployment guide and scripts for setting up the application on a production server.
-   **Comprehensive Test Suite:** Expand the test suite to include more unit and integration tests, aiming for higher code coverage.

## Medium Priority

-   **File Storage:** Move user-uploaded files to a cloud storage service (e.g., Amazon S3) for better scalability and reliability.
-   **Internationalization:** Add support for multiple languages in the user interface.
-   **Reporting:** Develop a reporting feature to generate statistics and insights from the order data.
-   **Email Notifications:** Implement email notifications to alert users about changes in order status.

## Low Priority

-   **"View Item" Page:** Fully implement the `ver_item` view to provide a detailed page for each individual item.
-   **Theme Customization:** Allow users to customize the visual theme of the application.
-   **API Expansion:** Expand the API to allow for third-party integrations.
-   **Real-time Updates:** Use WebSockets to provide real-time updates to the dashboard and order pages.
