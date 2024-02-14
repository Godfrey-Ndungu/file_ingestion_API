
# FILE UPLOAD

This project aims to build a REST API using Django and Django Rest Framework (DRF) to allow users to upload a file containing billions of records. The preferred database for this project is Postgres. The file to be uploaded will have a number of headers including first name, last name, national ID, birth date, address, country, phone number, email, and fingerprint signature.


## Authors

- [@Godfrey-Ndungu]


## Tech Stack
**Server:** Django,Django Rest Framework


![Architecture](https://raw.githubusercontent.com/Godfrey-Ndungu/files/main/django_rest_backend_with_celery%2C_redis_and_postgresql.png?token=GHSAT0AAAAAACAEQUFISEXXD43KWRQ5GATCZBBOAXA)


## Run Locally

1.Clone the project

```bash
git@github.com:Godfrey-Ndungu/file_ingestion_API.git
```
2.Create venv and install requirements
```bash
cd file_ingestion_API
python -m venv venv
pip install -r requirements.txt
```
3 setup database and add .env
```bash
touch .env
 ```
and following variables:
`SECRET_KEY`

`ALLOWED_HOSTS`

`DEBUG`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_HOST`

`DB_PORT`




Setup GitHooks[Contributing]:

1:Open the terminal and navigate to the root directory of your cloned project.  
2:Create a .git/hooks directory if it does not already exist  
3:Copy the conf/hooks/pre-commit file to the .git/hooks director  
4:Make the pre-commit file executable by running the command:chmod +x .git/hooks/pre-commit           
5:Verify that the pre-commit hook is set up correctly by running the command:pre-commit run --all-files


##Setting background workers using redis and celery

```bash
    sudo apt-get install redis-server
    sudo service redis-server start
```
activate python virtual environment and run celery using:
```bash
celery -A fileUpload worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo

```
#Automate above :
```bash
chmod +x Makefile.sh
./Makefile.sh    
```

## Setting Up Docker


Docker Setup
This document describes the steps needed to setup a local development environment using Docker.

Prerequisites
-Docker installed on your local machine. Refer to the official Docker documentation for installation instructions.
1.Docker Compose plugin installed on your local machine. Refer to the official Docker Compose documentation for installation instructions.
Setup 

2.Clone the repository to your local machine.
In the root directory of the project, create a file named .env-docker with the following content:

```bash
SECRET_KEY
ALLOWED_HOSTS
DEBUG
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST="db" #this is used in compose file
DB_PORT
```

3.Build the Docker containers using the following command:
```bash
docker-compose build
```
4.Start the Docker containers using the following command:
```bash
docker-compose up
```



## Running Tests

To run tests, run the following command

```bash
  tox
```


## API Reference

#### Put csv file

```http
  PUT /v1/file-upload/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `numeric` |  |
| `file` | `string` | **Required**.  csv file |
| `status` | `string` |  |

#### Get item

```http
  GET /v1/users/
```
{
  "count": 123,
  "next": "/accounts/?page=4",
  "previous": "/?page=2",
  "results": [
    {
      "first_name": "string",
      "last_name": "string",
      "national_id": "string",
      "birth_date": "2023-03-25",
      "address": "string",
      "country": "string",
      "phone_number": "string",
      "email": "user@example.com",
      "finger_print_signature": "string"
    }
  ]
}

full  documentation can be found here:

```http
swagger:  /v1/api/schema/swagger-ui/
```
```http
redoc:    /v1/api/schema/redoc/
```



## Documentation
helper.py:  
This module defines a class named FileReader that contains methods for reading CSV and Excel files. The read_file method is used to determine the type of the input file (by checking its extension) and calls the appropriate method to read the file.

models.py:  
This module defines two classes that inherit from Django's models.Model class: Base and UserData. The Base class provides a common time_added attribute for its subclasses, and its Meta class is marked as abstract, indicating that it cannot be instantiated directly. The UserData class defines several attributes for storing personal information of users such as name, national ID, address, phone number, and email, as well as a unique fingerprint signature. It also provides a method named is_finger_print_signature_unique to check the uniqueness of the fingerprint signature across all instances of the model. The save method is overridden to ensure that the fingerprint signature of the current instance is unique before saving it to the database.

The FileUpload class is another subclass of Base and contains attributes for uploading and processing files. It also defines a state machine using the django_fsm package to manage the processing status of the file. It provides four methods that transition the status of the file: start_processing, mark_failed, mark_processed, and mark_processing_failed. The save method is overridden to save the file to the specified location before saving the instance.

serializers.py:

This module defines a UserDataSerializer and a FileUploadSerializer using Django REST Framework's serializers.ModelSerializer. These serializers convert instances of the corresponding model classes to and from JSON format for use in API views.

Views.py:  
UserDataViewSet: This endpoint provides GET method to get a list of user data based on various filters, search criteria, and sorting options. It inherits from GenericViewSet and uses ListModelMixin. It defines filter_backends, filterset_fields, search_fields, and ordering_fields to filter and order data. It also defines pagination_class for pagination. The get_queryset method is overridden to add birth_date range filter.

FileUploadViewSet: This endpoint provides POST, GET, and LIST methods for creating, retrieving, and listing file uploads. It inherits from GenericViewSet and uses mixins for each method. The POST method creates a new file upload object and saves the uploaded file. It requires the 'file' parameter to be present in the request. The GET method retrieves a specific file upload object by primary key. The LIST method retrieves a list of file upload objects.

utils.py:  
This is a Python module containing several utility classes for validating CSV files and their data. The module imports a class called UserData from a module called models. The UserData class is not defined in this module, but it is presumably defined in the models module.

The module also imports several Python modules: hashlib, re, and datetime.

There are three main classes defined in the module: FileExtensionValidator, FileHeaderValidator, and RowDataValidator.

The FileExtensionValidator class is used for validating file extensions. It takes a list of allowed extensions when it is initialized, and it has methods for validating if a file extension is CSV, if it is XLS, and if it is an allowed extension.

The FileHeaderValidator class is used for validating the headers of CSV files. It has a method for checking if the headers in a file are valid. It takes a file object as input.

The RowDataValidator class is used for validating the data in CSV rows. It has a method for checking if a row's data is valid. It takes a dictionary representing a row's data as input. The class has several methods for validating individual fields, such as validate_field, which takes a field name and a field value as input and returns True if the value is valid and False otherwise.

The is_date method is used for checking if a string represents a valid date. The is_email method is used for checking if a string represents a valid email address. The is_hashed method is used for checking if a string is in hashed form.

If the row data is not valid, the is_valid method returns False. If the row data is valid, the method checks if the finger_print_signature field is already in the UserData object. If it is, the method returns False. If it is not, the method returns True.

signals.py:  
This code is a signal receiver function that is triggered after a FileUpload model instance is saved. It uses Django's signal framework to automatically execute the process_uploaded_file task asynchronously using Celery.

The receiver decorator takes two arguments: the signal (post_save) and the sender (FileUpload). The start_file_upload_signal function is the signal handler that will be called when a FileUpload instance is saved.

The function checks if the instance is newly created (created=True) and if so, it calls the process_uploaded_file.delay() method with the instance's id as an argument. This creates a task that will be executed asynchronously using Celery.

The process_uploaded_file task will take the id of the FileUpload instance and use it to retrieve the corresponding file from the storage and process it. This separation of the file processing task from the request-response cycle is important for scalability and responsiveness of the application, especially when dealing with large files.

tasks.py:  
The process_uploaded_file function is decorated with the @shared_task decorator from the celery library. This decorator is used to define a Celery task that can be executed asynchronously.

The process_uploaded_file function takes a single parameter id, which represents the ID of a FileUpload object in the database. The function first retrieves the FileUpload object with the specified ID using the filter method and the first method. If the object does not exist, the function returns.

The start_processing method of the FileUpload object is called to update the status of the object to "processing". The save method is called to save the changes to the database.

The function then attempts to validate the headers of the CSV file using the FileHeaderValidator.is_valid method. If the headers are not valid, a ValueError is raised with the message "Invalid file headers."

If the headers are valid, the function reads the file using the FileReader.read_file method, which returns an iterator over the rows of the CSV file.

The function then iterates over each row in the CSV file and validates its data using the RowDataValidator.is_valid method. If the data is valid, a new UserData object is created with the data from the row, and the object is saved to the database using the save method.

If an exception occurs during the processing of the file, the function logs an error message with the logger.error method, marks the FileUpload object as processing failed using the mark_processing_failed method, and saves the changes to the database using the save method. The function then raises the exception with the retry method, which will retry the task up to three times.

If no exception occurs, the function logs a success message with the logger.info method, updates the status of the FileUpload object to "processed" using the mark_processed method, saves the changes to the database using the save method, and returns the string "File processed successfully!"
