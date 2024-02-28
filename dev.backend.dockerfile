
########################
# image name: backend_img


FROM python:3.11-slim

RUN mkdir -p /backend_app

## Set the working directory in the container to /app
WORKDIR /backend_app

## Copy the dependencies file to the working directory.
COPY hex_backend/requirements.txt requirements.txt

## Install any dependencies.
RUN pip install --no-cache-dir -r requirements.txt

## Copy the current directory contents into the container at /backend
COPY hex_backend/ .

## Expose port 5000 to access the Flask app. (default port is 8000), in development
EXPOSE 5000

## Define environment variable
## - PYTHONDONTWRITEBYTECODE: prevents Python from writing pyc files to disc (equivalent to python -B option)
## - PYTHONUNBUFFERED: prevents Python from buffering stdout and stderr (equivalent to python -u option)

ENV FLASK_ENV=development
ENV FLASK_APP="run.py"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]



