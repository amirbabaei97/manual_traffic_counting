# Manual Traffic Counting App

This project is an attempt at creating a web application for manually counting traffic. It's designed to help users log different types of vehicles passing a point over a period, providing a simple interface for starting counting sessions, logging each vehicle count, and ending sessions.

## Features

- **Start Counting Session**: Users can start a new counting session, specifying only the session name and direction.
- **Count Vehicles**: During a session, users can count various types of vehicles by clicking buttons corresponding to each vehicle type.
- **End Session**: Users can end a counting session, which timestamps the end of the session.
- **View Counts**: The application allows viewing the total counts for each vehicle type within a session.
- **Export Data**: Users can export aggeregated session data as well as individual count data to CSV from the Django admin panel.

## Setup

1. Clone this repository and enter the directory: `git clone git@github.com:amirbabaei97/manual_traffic_counting.git && cd manual_traffic_counting`
2. Set up a virtual environment and activate it: `python3 -m venv venv && source venv/bin/activate`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`
6. Access the web application at: `http://127.0.0.1:8000/`

## Usage

To use the app, navigate to the home page and start a new counting session. Click on the vehicle buttons to count each type as they pass, and end the session when finished.

## Contributing

Contributions to this project are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

---

This project is very much a work in progress and was created in an hour. Feedback and contributions are highly appreciated.
