FROM python:3

# copy the requirements file
COPY requirements.txt /app/requirements.txt

# install the necessary dependencies
RUN pip install -r /app/requirements.txt

# copy all files and directories in the current directory into the image
COPY . /app

# set the working directory to the app directory
WORKDIR /app

# run the app when the container is started
#CMD ["python", "app.py"]
CMD ["gunicorn","app:server"]
