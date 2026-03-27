# 🚀 Installation & Setup

# 1. Clone the Repository and Switch Branch

Make sure you are on the ssid-auth branch to use this version of the system.

```git clone https://github.com/VelogaWhite/VelogaWhite```

```cd election_app```


# 2. Setup a Virtual Environment

Create a virtual environment

```python -m venv venv```

Activate the virtual environment
  On Windows:
  ```venv\Scripts\activate```
  
  On macOS/Linux:
 ``` source venv/bin/activate```


# 3. Install Dependencies

```pip install -r requirements.txt```


# 4. Initialize the Database

Run Django's migration commands to build the database schema:

```python manage.py makemigrations```

```python manage.py migrate```


# 5. Generate Mock Data (Highly Recommended)

Populate your local database with sample categories, books, users, and dummy transactions to easily test the system out of the box:


```python election_app/setup_data.py```


# 6. Run the Development Server

```python manage.py runserver```
