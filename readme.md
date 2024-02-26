# Manual Traffic Counting App

This project is an attempt at creating a web application for manually counting traffic. It's designed to help users log different types of vehicles passing a junction over a period, providing a simple interface for starting counting sessions, logging each vehicle count, and ending sessions.

## Features

- **Start Counting Session**: Users can start a new counting session, specifying the session name and explanations, as well as, the number of streams and car types.
- **Count Vehicles**: During a session, after choosing a stream, users can count various types of vehicles by clicking buttons corresponding to each vehicle type.
- **End Session**: Users can end a counting session, which timestamps the end of the session.
- **View Counts**: The application allows viewing the total counts for each vehicle type within a session.
- **Export Data**: Users can export aggregated session data as well as individual count data to CSV from the Django admin panel.

## Setup

1. Clone this repository and enter the directory: `git clone git@github.com:amirbabaei97/manual_traffic_counting.git && cd manual_traffic_counting`
2. Set up a virtual environment and activate it: `python3 -m venv venv && source venv/bin/activate`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`
6. Access the web application at: `http://127.0.0.1:8000/`

## Usage

To use the app, navigate to the home page and start a new counting session by indicating the stream numbers and car types. Then, on the next screen, select a stream, click on the buttons to count each type as they pass, and end the session when finished.


## Acknowledgements

Special thanks to [Jana Busse](https://www.frankfurt-university.de/?id=12694), Ph.D. candidate from ReLUT, Frankfurt University of Applied Sciences who kindly shared her knowledge about manual traffic counting and made comments. 

---

This project is very much a work in progress. Feedback and contributions are highly appreciated.
