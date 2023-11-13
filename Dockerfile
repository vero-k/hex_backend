
########################
# Production 

## Use an official Python runtime as a parent image
FROM python:3.11-slim

## Set the working directory in the container to /app
WORKDIR /backend

## Copy the dependencies file to the working directory.
COPY requirements.txt .

## Install any dependencies.
RUN pip install --no-cache-dir -r requirements.txt

## Copy the current directory contents into the container at /backend
COPY . /backend

## Expose port 8000 to access the Flask app. (default port is 8000), in production. Since Gunicorn uses
EXPOSE 8000

## Define environment variable
## - PYTHONDONTWRITEBYTECODE: prevents Python from writing pyc files to disc (equivalent to python -B option)
## - PYTHONUNBUFFERED: prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP hex_be:create_app()
ENV FLASK_ENV production

## for production
## 4 worker processes started
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "hex_be:create_app()"]


