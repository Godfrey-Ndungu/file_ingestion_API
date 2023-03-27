
![Logo](https://www.lifewire.com/thmb/tHjH9M19MsA9gFY-qcZvKYv5oG4=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/cloud-upload-a30f385a928e44e199a62210d578375a.jpg)


## Run Locally

Clone the project

```bash
git@github.com:Godfrey-Ndungu/file_ingestion_API.git
```

Setup GitHooks:

1:Open the terminal and navigate to the root directory of your cloned project.  
2:Create a .git/hooks directory if it does not already exist
3:Copy the conf/hooks/pre-commit file to the .git/hooks directory  
4:Make the pre-commit file executable by running the command:chmod +x .git/hooks/pre-commit  
5:Verify that the pre-commit hook is set up correctly by running the command:pre-commit run --all-files
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



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

`ALLOWED_HOSTS`

`DEBUG`


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
```http
```
```http
```



## Installation

Setting background workers using redis and celery

```bash
    sudo apt-get install redis-server
    sudo service redis-server start
```
activate python virtual environment and run celery using:
```bash
celery -A fileUpload worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo

```
    