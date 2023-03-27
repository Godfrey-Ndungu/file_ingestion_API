#!/bin/bash

# Check if OS is Unix or Windows and run appropriate code
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # Install required packages
  sudo apt update
  sudo apt install python3 python3-pip python3-venv python3-setuptools bionic

  # Install and start Postgres
  sudo apt install postgresql
  sudo systemctl start postgresql

  # Install and start Redis
  sudo apt install redis-server
  sudo systemctl start redis-server
elif [[ "$OSTYPE" == "win"* ]]; then
  # Windows code goes here
  echo "Windows is not supported yet."
  exit 1
else
  echo "Unsupported OS."
  exit 1
fi

# Create virtual environment
python3 -m venv env

# Add .env file
echo "SECRET_KEY=\"\"" >> .env
echo "ALLOWED_HOSTS=\"\"" >> .env
echo "DEBUG=" >> .env
echo "DB_NAME=\"\"" >> .env
echo "DB_USER=\"\"" >> .env
echo "DB_PASSWORD=\"\"" >> .env
echo "DB_HOST=\"\"" >> .env
echo "DB_PORT=\"\"" >> .env

# Install requirements
source env/bin/activate
pip install -r requirements.txt

# Ask user to set up DB
echo "Please set up the database and update the .env file with the necessary information. Once you have done this, type 'y' to continue."
read answer

if [ "$answer" != "y" ]; then
  echo "Aborting."
  exit 1
fi

# Run Django migrations and server
python manage.py migrate --settings=fileUpload.development
python manage.py runserver --settings=fileUpload.development
