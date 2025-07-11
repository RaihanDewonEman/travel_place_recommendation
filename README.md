# 🌍 Travel Place Recommendation API(Bangladesh's Districts)

This Django REST API helps users find the best districts in Bangladesh for travel based on temperature and air quality using Open-Meteo API.

## Features

- Get Top 10 Best Districts for Travel based on following criteria:
  - coolest temperature (average temperature at 2 PM over the 7-day period)
  - better air quality (lower PM2.5 levels) 
- Get Travel Recommendation Between Two Locations based on temperature and air quality (Current Location to Destination District)

---
## Getting Started (Setup)

Follow these steps to set up and run the project locally.

---

### 1. Clone the Repository

```bash
git clone https://github.com/RaihanDewonEman/travel_place_recommendation.git
```

---

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
cd travel_place_recommendation
pip install -r requirements.txt
```

---

### 4. Configure the Database

Edit the PostgreSQL database configuration file:

```bash
sudo nano config/database.py
```

Update it with your own credentials and database name:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### 5. Prepare Migration Files

```bash
mkdir travel_recommendation/migrations
touch travel_recommendation/migrations/__init__.py
```

---

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---


### 7. Create a User
Create a user for token authentication

```bash
python manage.py createsuperuser
```

---


### 8. Load Initial Data

```bash
python manage.py create_district_data
python manage.py sync_forecast_api_data
```

---

### 9. Run the Development Server

```bash
python manage.py runserver
```


---

## Authentication

This API uses **Token Authentication**. You must include your token in the request headers:

```
Authorization: Token <your-token>
```

---

### To Obtain a Token

Make a POST request to the authentication endpoint:

```bash
POST /api/token-auth/
{
  "username": "your_username",
  "password": "your_password"
}
```

You will receive a response like:

```json
{
  "token": "your_token_string"
}
```

---

## API Endpoint (with parameters)
1. To Find the Coolest and Cleanest 10 Districts in Bangladesh
```
GET /api/best-districts/
```

2. Travel Recommendation API
```
GET /api/travel-suggestion/?current_latitude=22.335109&current_longitude=91.834073&destination=Cox%27s%20Bazar&travel_date=2025-07-14
```