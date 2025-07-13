# Application Architecture Documentation

This document outlines the high-level architecture of the Frank Site Django application.

## Project Structure

The project follows a modular Django application structure, with distinct apps for different functionalities.

```
frank_site/
├── APPS/
│   ├── BLOG/           # Blog application (posts, categories, comments)
│   ├── PAYMENTS/       # Payment processing (integrates with PayPal)
│   ├── PORTFOLIO/      # Portfolio management (projects, categories)
│   └── STORE/          # E-commerce store (products, cart, checkout)
├── HOME/               # Main landing page and core site functionalities
├── frank_site/         # Main Django project settings, URLs, WSGI, ASGI
├── TEMPLATES/          # Global HTML templates (base.html) and app-specific templates
├── static/             # Global static files (CSS, JS, images)
├── media/              # User-uploaded media files
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── ...                 # Other project files (.git, .vscode, env, etc.)
```

## Key Components and Responsibilities

*   **`frank_site/settings.py`**:
    *   Central configuration for the Django project.
    *   Manages `INSTALLED_APPS`, `MIDDLEWARE`, database settings, static/media file configurations.
    *   **Security**: `SECRET_KEY` and `DEBUG` are configured to be loaded from environment variables for production readiness. `ALLOWED_HOSTS` is set with placeholders.
*   **`frank_site/urls.py`**:
    *   Main URL dispatcher for the entire project.
    *   Includes URLs from individual applications.
*   **`HOME` App**:
    *   Handles the main landing page and general site views.
    *   Integrates dynamic content like recent blog posts and client showcases.
*   **`APPS/BLOG` App**:
    *   Manages blog posts, categories, and related functionalities.
    *   Provides views for listing posts, viewing individual posts, and filtering by category.
*   **`APPS/PORTFOLIO` App**:
    *   Manages portfolio projects and their categories.
    *   Features dynamic filtering and display of projects.
*   **`APPS/STORE` App**:
    *   Core e-commerce functionality.
    *   Manages products, shopping cart, and checkout processes.
    *   Includes product listings, detail views, and cart management.
*   **`APPS/PAYMENTS` App**:
    *   Handles payment processing logic.
    *   **PayPal Integration**: Utilizes `django-paypal` for PayPal payments. The `process_paypal_payment` view initiates the PayPal transaction, and `paypal_return`/`paypal_cancel` handle the callbacks.
    *   Manages credit card payments (simulated for now, but extensible for real gateways).
    *   Manages saved payment methods and order history.
*   **`TEMPLATES/` Directory**:
    *   Contains `base.html`, which serves as the base template for all other HTML files, ensuring consistent header, navigation, and footer.
    *   App-specific templates are organized within subdirectories (e.g., `TEMPLATES/apps/blog/`).
*   **`static/` Directory**:
    *   Houses global static assets like `global.css` and `global.js`.
    *   `global.css` consolidates all common styles, promoting a consistent visual identity and reducing redundancy.
    *   `global.js` contains global JavaScript functionalities, including AJAX loading and UI interactions.
*   **`media/` Directory**:
    *   Stores user-uploaded content, such as product images and portfolio project images.

## Styling Approach

The application adopts a centralized styling approach:

*   **`global.css`**: All common and global styles are defined here. This includes resets, typography, layout basics, and reusable component styles.
*   **`base.html`**: All other templates extend `base.html`, which links to `global.css`, ensuring that global styles are applied consistently across the entire site.
*   **Bootstrap 5**: The project leverages Bootstrap 5 for responsive design and pre-built UI components, which are then customized via `global.css`.

## Production Readiness Considerations

*   **Environment Variables**: Sensitive information like `SECRET_KEY` and `PAYPAL_RECEIVER_EMAIL` are configured to be loaded from environment variables. This is crucial for security in production.
*   **`DEBUG=False`**: `DEBUG` mode should always be `False` in production to prevent exposure of sensitive error information.
*   **Database**: For production, SQLite should be replaced with a robust database like PostgreSQL or MySQL.
*   **Static Files**: `collectstatic` command is used to gather all static files into a single directory for efficient serving by a web server (e.g., Nginx, Apache).
*   **HTTPS**: The application should be served over HTTPS in a production environment.
*   **Web Server**: A production-ready web server (e.g., Gunicorn + Nginx/Apache) should be used to serve the Django application.
*   **Error Logging**: Implement robust error logging and monitoring.
