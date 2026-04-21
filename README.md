# EduQuery 🚀

EduQuery is a modern, feature-rich discussion forum built specifically for educational environments. It connects students and teachers through a robust Q&A system and dynamic community spaces.

## 🌟 Key Features

*   **Role-Based Access Control:** Differentiated experiences for Students and Teachers.
*   **Dynamic Q&A System:**
    *   Ask questions with detailed formatting.
    *   Answer questions to help peers.
    *   Like/upvote helpful answers to ensure quality content floats to the top.
*   **Communities (Groups):**
    *   Create dedicated spaces for specific subjects, projects, or interests.
    *   Set group access (open to all, restricted).
    *   Customizable group descriptions, rules, tags, and icons.
    *   Post questions and have discussions directly within communities.
*   **Interactive Polling:** Run instant polls within groups to gauge opinions or make quick decisions.
*   **Rich Media Support:** Upload custom group icons for a personalized feel.
  
## 🛠️ Technology Stack

*   **Backend:** Django (Python), focusing on a clean `MVT` (Model-View-Template) architecture.
*   **Database:** MySQL (configured via `django.db.backends.mysql`).
*   **Frontend:** HTML5, CSS3, JavaScript (Django Templates).
*   **Authentication:** Django's built-in robust authentication system integrated with a custom User model.

## 🚀 Getting Started

Follow these steps to set up EduQuery locally on your machine.

### Prerequisites

*   Python 3.8+
*   MySQL Server (Ensure it's running)
*   `mysqlclient` prerequisites (e.g., MySQL C connector) for your OS if not using a pre-compiled wheel.

### 1. Clone the Repository
```bash
git clone <repository_url>
cd EdQuery
```

### 2. Set up a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

1.  Open your MySQL command-line client or a GUI tool (like MySQL Workbench, phpMyAdmin).
2.  Create the database:
    ```sql
    CREATE DATABASE eduquery_db;
    ```
3.  Update the database configuration in `eduquery_core/settings.py` to match your local setup:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'eduquery_db',
            'USER': 'root',          # Your MySQL username
            'PASSWORD': 'root123',   # Your MySQL password
            'HOST': 'localhost',
            'PORT': '3307',          # Ensure this matches your MySQL port (default is usually 3306)
        }
    }
    ```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional but recommended)
Create an admin account to manage the platform via the Django Admin panel.
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will now be running at `http://127.0.0.1:8000/`.

## 🌐 Project Structure

*   `eduquery_core/`: The core Django project settings, routing, and configurations.
*   `discussion/`: The main Django app handling Q&A, communities, polls, and user profiles.
    *   `models.py`: Database schemas (User, Group, Question, Answer, Poll).
    *   `views.py`: Application logic and request handling.
    *   `urls.py`: URL routing specific to the discussion app.
*   `templates/`: HTML templates for rendering the frontend.
*   `static/`: CSS, JavaScript, and image assets.
*   `media/`: Directory for user-uploaded content (like group icons).

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).
