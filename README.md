# 🚗 Carpoolr

> Connect with fellow travelers and make every trip more affordable

---

## About

A Django-based ridesharing web application built for college students to connect with drivers and passengers at their school. CarPoolr allows students to post rides, request to join rides, link rides to campus events, and review each other after completed trips.

### Features

- User Authentication — Register and log in with full validation (unique username, email, password strength, phone number)
- Driver & Passenger Accounts — Users register as a driver or passenger; drivers can post rides, passengers can request to join
- School-Based Filtering — Rides are filtered by school so students only see rides from people at their institution
- Ride Management — Drivers can post, edit, and delete rides with pickup location, destination, price, departure time, and seat count
- Ride Requests — Passengers can request to join rides; drivers can accept or deny requests from a notifications page
- Request Status — Passengers can track whether their request is pending, accepted, or denied
- Events — Users can create campus events and link rides to them; event detail pages show all associated rides
- Reviews — After a ride is completed, passengers can leave a review for the driver (only available after departure time has passed)
- User Profiles — Public profile pages show ride stats, average rating, and recent reviews
- Search & Filter — Rides can be filtered by location, max price, date, and sorted by price or departure time
- Maps Integration — Pickup locations link directly to Google Maps for easy navigation

### Tech Stack

- Backend — Python, Django
- Database — SQLite
- Frontend — HTML, CSS (custom)
- Auth — Django's built-in auth system extended with AbstractUser
- Location — django-location-field with Google Maps

## Setup
Prerequisites: Python 3.10+, pip

#### Clone the repository
git clone https://github.com/your-username/CarPoolr.git
cd CarPoolr

#### Create and activate a virtual environment
1. python -m venv .venv

2. source .venv/bin/activate (On Windows: .venv\Scripts\activate)

#### Install dependencies
pip install -r requirements.txt

#### Apply migrations
python manage.py migrate

#### Run the development server
python manage.py runserver
Then open http://127.0.0.1:8000 in your browser.

### Project Structure
```
CarPoolr/
├── account/        # User auth, registration, login, profiles
├── rides/          # Ride posting, requests, reviews, notifications
├── events/         # Event creation and listing
├── home/           # Landing page
├── templates/      # Base template (base.html)
└── carpoolr/       # Project settings and URL config
```

### Models
- User: Extended AbstractUser with Driver_Status, school, rating, phone
- Ride: A posted ride with driver, pickup, destination, price, seats
- RideRequest: A passenger's request to join a ride (pending/accepted/denied)
- Review: A review left by one user for another after a completed ride
- Event: A campus or local event that rides can be linked to

#### Team: Group 4
- Domanick Angel
- Joey Grottola
- Christine Samons
- Louise Spivey

##### 
Created for CSC 3400 - Software Engineering
