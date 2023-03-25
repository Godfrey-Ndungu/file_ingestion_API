FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the Django project
COPY . .

# Expose port 8000 for the Django web server
EXPOSE 8000

# Define environment variables for Django settings
ENV DJANGO_SETTINGS_MODULE=fileUpload.development
ENV PYTHONUNBUFFERED=1

# Start the Django web server with auto-reloading
CMD ["./manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
