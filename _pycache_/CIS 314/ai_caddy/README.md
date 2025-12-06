#AI Caddy

### CIS 314 — Final Project

AI Caddy is an interactive golf application that allows users to play local courses, track scores, and receive real-time club recommendations from an AI-powered virtual caddy. The system combines GPS data, club distances, and course information to deliver accurate suggestions and a smooth user experience.

## Features

### AI Club Recommendations

The AI caddy analyzes:

* The user’s current **club bag**
* **GPS location**
* **Hole location (pin coordinates)**
* **Course layout & hole data**

Using this information, it suggests the optimal club for each shot.

### GPS Distance Calculation

The app uses:

* `QGeoPositionInfoSource` for real-time device GPS
* `geopy` to calculate distance to the hole
* Automatic conversion to yards for golfers

### SQLite Database Integration

All course and player information is stored locally using SQLite, including:

* Users
* Courses
* Holes
* Rounds played
* Individual stroke data

### Sample Course

Running `admin.py` automatically creates a real-life sample course:
**Musket Ridge Golf Course (Myersville, MD)**
This provides a ready-to-play environment for testing.

## Project Structure

ai_caddy/
│
├── admin.py          # Initializes the database and sample course
├── golf_ai.py        # AI logic for club recommendations
├── golf_globals.py   # Global variables and shared state
├── main.py           # Application entry point
├── images/        # Images, icons, etc.
└── README.md

## 📝 Notes

* GPS functionality depends on device hardware and OS permissions.
* AI function doesnt work well when not on course. Recommend testing AI function directly from golf_ai.py
* Distance calculations use geodesic measurements for accuracy.
* The project was created as the final assignment for **CIS 314**.

Author

**Peyton Hollis**
📨 [phollis0216@gmail.com](mailto:phollis0216@gmail.com)
