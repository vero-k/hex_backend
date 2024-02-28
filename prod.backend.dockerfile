
########################
# Production NOTE NEEDS FIXING

FROM python:3.11-slim

## Set the working directory in the container 
WORKDIR /backend_app

## Copy the dependencies file to the working directory.
COPY requirements.txt /backend_app

## Install any dependencies.
RUN pip install --no-cache-dir -r requirements.txt

## Copy the current directory contents into the container at /backend
COPY . .

## Expose port 8000 to access the Flask app. port that gunicorns uses
EXPOSE 8000

# if app is only accessible from within the container
#ENV FLASK_RUN_HOST 0.0.0.0 

## Define environment variable
##  PYTHONDONTWRITEBYTECODE: prevents Python from writing pyc files to disc (equivalent to python -B option)
## PYTHONUNBUFFERED: prevents Python from buffering stdout and stderr (equivalent to python -u option)
#ENV FLASK_APP run
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## for production
## 4 worker processes started
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "hex_be:create_app()"]





