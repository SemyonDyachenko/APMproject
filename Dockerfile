# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Django
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Expose the port that Django runs on
EXPOSE 8000

# Start the Django development server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]