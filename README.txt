

Flask Backend for Image Processing

This backend app is designed specifically to process images and data to meet the needs of our corresponding frontend application. This backend service is built to handle a variety of tasks including image manipulation, data formatting, and efficient data transfer.
Features

    Image Processing: Customized image processing functionalities tailored for the frontend needs.
    Data Handling: Efficient processing and formatting of data for frontend utilization.
    Databases: Storage of data from frontend in database for the duration of the game
    API Endpoints: RESTful API endpoints for easy integration with the frontend.


Getting Started

These instructions will get you a copy of the project up and running on your local machine 

git clone []
cd []

# Activate Virtual Environment
source myenv/bin/activate

# set ENV variable
export FLASK_APP=run.py

# run the application
flask run

There is a dockerfile in the respitory as well, if one wants to deploy the app in a docker container
