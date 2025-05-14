# Parking System API

## Description

This is a backend API for managing a parking system. It provides functionalities for managing parking lots, floors, rows, slots, users, and vehicles.  The API is built using the Flask framework and uses MySQL for the database.

## Features

* **Parking Management:**
    * Add, retrieve, update, and delete parking lots.
    * Manage parking floors, rows, and slots.
* **User Management:**
    * Register and log in users.
    * Retrieve user details.
* **Vehicle Management:**
    * Add, retrieve, update, and delete vehicles.
* **Parking Operations:**
    * Allocate and free parking slots.
    * Record vehicle entry and exit times.
* **Database:** MySQL
* **API Testing:** pytest
* **CI/CD:** GitHub Actions, Docker

## Table of Contents
* [Installation](#installation)
* [Database Setup](#database-setup)
* [Running the Application](#running-the-application)
* [Testing](#testing)
* [CI/CD](#cicd)
* [Dependencies](#dependencies)

## 📁 Project Structure
```
📁 Parking_system/ 
│-- 📂 .git/           # Git version control directory
│-- 📂 .github/
│ └── 📂 workflows/
│ └── 📄 cicd.yaml     # GitHub Actions workflow for CI/CD
│-- 📄 .gitignore      # Git ignore file for excluding files from repo
│-- 📄 app.py          # Main Flask app with routes and models
│-- 📄 Dockerfile      # Instructions to build Docker image
│-- 📄 requirements.txt # Python dependencies
│-- 📄 run.py          # Script to run the Flask app
│-- 📄 test_app.py     # Pytest test suite for the application

```

### 📄 File & Folder Descriptions

| File/Folder             | Description |
|------------------------|-------------|
| `.git/`                | Auto-generated Git directory for version control. |
| `.github/workflows/`   | Contains GitHub Actions workflows. |
| `cicd.yaml`            | Defines CI/CD automation steps (build, test, push Docker). |
| `app.py`               | Main application file containing route definitions and model logic. |
| `Dockerfile`           | Used to containerize the app using Docker. |
| `requirements.txt`     | Lists Python dependencies (`Flask`, `PyMySQL`, etc.). |
| `run.py`               | Entry point that calls `create_app()` and runs the server. |
| `test_app.py`          | Contains unit tests using `pytest` for API endpoints. |



## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Preethika1801/Park_Vision_Backend.git
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    * On Windows:

        ```bash
        venv\Scripts\activate
        ```

    * On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Database Setup

1.  **Set up MySQL:**
    * Make sure you have MySQL installed and running.
    * Create a database named  `parking_system`.
    * Import the database schema and initial data from the  `Parking-system dump.sql`  file. You can use a MySQL client or the command line:

        ```bash
        mysql -u root -p parking_system < Parking-system dump.sql
        ```

2.  **Configure the database connection:**
    * In the  `app.py`  file, update the  `username`  and  `password`  variables in the  `create_app`  function with your MySQL credentials:

        ```python
        username = "your_mysql_username"  # Replace with your MySQL username
        password = "your_mysql_password"  # Replace with your MySQL password
        ```

## Running the Application

1.  **Start the application:**

    ```bash
    python run.py
    ```

2.  The application will be running at  `http://0.0.0.0:5000`.

## Testing

1.  **Run the tests:**

    ```bash
    pytest
    ```

## CI/CD

The project is set up with a CI/CD pipeline using GitHub Actions.

* The  `cicd.yaml`  file defines the workflow.
* On every push and pull request to the  `main`  and  `master`  branches, the workflow will:
    * Build a Docker image of the application.
    * Log in to Docker Hub.
    * Push the Docker image to Docker Hub.

## Dependencies

* Flask
* Flask-SQLAlchemy
* mysqlclient/PyMySQL
* pytest

## 📄 Additional Documentation

To understand this project in more detail, please refer to the **File** uploaded in the repository.


