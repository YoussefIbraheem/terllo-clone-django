# Use the official Python runtime image
FROM python:3.12-slim  

# Create the accounts directory
RUN mkdir /accounts

# Set the working directory inside the container
WORKDIR /accounts

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Upgrade pip
RUN pip install --upgrade pip 

# Copy the Django project  and install dependencies
COPY requirements.txt  /accounts/

# run this command to install all dependencies 
RUN pip install -r requirements.txt

# Copy the Django project to the container
COPY . /accounts/

# Expose the Django port
EXPOSE 8000

# Run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]