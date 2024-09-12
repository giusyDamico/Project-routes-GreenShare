# Project-GreenShare
# Django Routes Management App

## Overview

This Django application allows users to upload or import route data either through a direct file upload or by providing a URL to a file. The routes data is processed and stored in a PostgreSQL database.

## Settings of PostgrSQL Database in local
I have created a DB with the following parameters:

        'default': {
                 'ENGINE': 'django.db.backends.postgresql',
                 'NAME': 'postgres',
                 'USER': 'postgres',
                 'PASSWORD': 'giusy',
                 'HOST': 'localhost',
                 'PORT': '5432',
         }
### How to set Database PostgreSQL in local:

Go to the shell and start comunication with PSQL (if you want access as superuser the username is "postgres")

        sudo -u postgres psql

If you want reset password of superuser, write on shell:

        ALTER USER postgres WITH PASSWORD 'password';
I have used as password= giusy

Then you can write command of PSQL:
- \du : in order to visualize all users
- \l: in order to visualize all databases
- \c name_db: in order to connect to database

If you want create a new database:

        CREATE DATABASE nome_db;
I have used as nome_db=postgres

If you want verify the port and if it is correct the connection with a specific Database:

        \conninfo
In this way you can see also the used port. 
In my case i have used port : 5432
# Advantage of use DOCKER
Using Docker-compose.yml , it is not necessary to set in local the PostgreSQL.

## Steps in order to compose up:
- **Step 1**: go in the directory where there is *docker-compose.yml* and run on terminal:  'docker-compose up --build'
- **Step 2**: go in the shell of Django container and do migrations run command: 
          ' python manage.py makemigrations app '
          ' python manage.py migrate '   

### Features

- **View Routes:** Displays all routes stored in the database.
- **Upload Routes:** Allows users to upload route files directly.
- **Import Routes from URL:** Allows users to import route files from a specified URL.

# DATA IMPORT   
I have implemented three functions in views.py : 
## View Routes

    Endpoint: /app/view-routes/
    Method: GET
    Description: Displays all routes stored in the database along with a success message from previous operations.

## Upload Routes

    Endpoint: /app/upload-routes/
    Method: POST
    Description: Upload a file directly to the server. The file can be a .zip file containing routes.txt or a routes.txt file directly.
    File Requirements:
        .zip file must contain routes.txt.
        .txt file should be named routes.txt.
    Response: Redirects to the /app/view_routes/ page with a success message if the upload and processing are successful.

## Import Routes from URL

    Endpoint: /app/import-file/
    Method: POST
    Description: Import route data from a URL. The URL must point to a .zip file containing routes.txt or a .txt file directly.
    Request Body:
        file_url (string): URL of the file to be imported.
    Response: Redirects to the /app/view_routes/ page with a success message if the import and processing are successful.
### Usage
In order to test these views, I have used *insomnia*, I have uploaded the JSON file in order to test these requests. (test_request_routes.JSON).

# DJANGO ADMIN

### Admin Interface Configuration
In the admin.py file, we have configured the admin interface for the Route model with the following settings:

### Accessing the Admin Interface
  - **Create admin user**: Type on terminal: *python manage.py createsuperuser* (you need to choose username, email and password)
  - **Start the Django Server**: Type on terminal: *python manage.py runserver*
  - **Navigate to the Admin Page**: Open your browser and go to the Django admin URL: http://127.0.0.1:8000/admin/
  - **Log in with Admin Credentials** : Enter the username and password for the admin user.

I have created an user (that have permission only to view, but not modified the routes username='User1' password='Utenteanonimo1!').

### Manage Route Data:
Once logged in, you will see a section called "Routes" in the admin panel. Click on it to view, search, filter, and modify route data.

# REST API
I have used serializer.py in order to allow a client to browse the data imported from the routes.txt file. 
## Usage
- **Authentication**: It is necessary authenticate before to browse the data. If you are not authenticated it gives error.
- **Navigate**: The endpoint is : /app/routes/
- **List of all routes**: you can see all routes saved in DB
- **Filter**: you can filter routes for route_long_name (and I add also filtering for route_id).

I have used *insomnia* to test the request (see JSON file test_request_routes.JSON)

# Additional:
## 1.Handling "Page Not Found" Errors
Implement error handling to provide informative messages for "Page Not Found" errors.

## 2. Adding view for delete element inside Database
    Endpoint: /app/refresh-db/
    Description: All elements inside Database is deleted.

## 3. Adding tests.py
In order to run test.py , write on shell : *python manage.py test*.

### 1. Upload Routes Functionality (`test_upload_routes`)

- **Objective**: To verify that the *upload_routes* view correctly processes file uploads and imports route data into the database.
- **Test Details**: 
  - Simulates the upload of a ZIP or text file containing route data.
  - Checks if the file is handled properly and if the routes are imported into the database correctly.
  - Verifies that the appropriate success message is displayed and the redirection occurs properly.

### 2. Import Routes from URL (`test_import_routes_from_url`)

- **Objective**: To ensure that the *import_routes_from_url* view correctly processes an import request from a given URL.
- **Test Details**: 
  - Verifies that the view can handle requests containing URLs ( I have adding *https://www.ctmcagliari.it/open_data/GTFS.zip*)  .zip or .txt files.
  - Checks if the file is downloaded, extracted (if necessary), and whether the route data is imported into the database.
  - Ensures the correct success message is displayed and that redirection occurs properly.

### 3. Refresh Database (`test_refresh_db`)

- **Objective**: To confirm that the *refresh_db* view correctly deletes all existing route data from the database.
- **Test Details**: 
  - Ensures that invoking the *refresh_db* view results in the complete removal of route data from the database.
  - Verifies if the correct success message is shown after the data is deleted.

### 4. Custom 404 Page (`test_custom_404_page`)

- **Objective**: To test the custom 404 error page functionality.
- **Test Details**: 
  - Verifies that when a non-existent page is requested, the application properly displays a custom 404 error page with the appropriate status code.

# Possible Improvements
## 1. Token Authentication
Implement token authentication to enhance security and provide a more robust authentication mechanism for API endpoints. This can be achieved using Django REST framework’s token authentication (*rest_framework.authtoken*)

## 2. Throttling
Implement throttling to limit the number of requests a user can make to the API within a specified time frame. This helps protect the application from excessive usage and ensures fair use of resources.

## 3. Improve the visualization of routes 
A potential future improvement is the implementation of pagination to limit the number of routes displayed per page.
