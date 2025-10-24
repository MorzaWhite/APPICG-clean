# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-24

### Added

-   Initial version of the SGICG application.
-   Core functionality for creating and managing certification orders.
-   Multi-step wizard for adding items to an order.
-   Automatic calculation of suggested delivery dates based on business hours.
-   User interface for tracking the status of orders.

### Fixed

-   **Critical Bug:** Fixed the order creation process, which was previously failing to save orders to the database due to a data parsing issue.
-   **UI/UX:** Stabilized the "Add Item" modal, preventing it from crashing or showing a blank screen.
-   **UI/UX:** Ensured the "Add Item" modal resets correctly after an item is added.
-   **UI/UX:** The main page now updates dynamically after an item is added, without requiring a full page reload.
-   **Backend:** Resolved a `database is locked` error by implementing a retry mechanism for database transactions.
-   **Backend:** Fixed a circular import issue between `views.py` and `forms.py` that was causing the server to crash silently.
-   **UI/UX:** Removed the "Decorative Stones" feature, which was unstable and causing UI issues.
-   **UI/UX:** Corrected the logic for displaying success and error toasts.

### Changed

-   The "Add Item" wizard flow has been updated to conditionally skip jewelry-specific steps for non-jewelry items.
-   Improved error handling in the frontend to provide better user feedback.
