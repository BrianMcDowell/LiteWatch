# LiteWatch

## About
LiteWatch is for privacy-minded consumers who want to be notified when a website changes to match predefined keywords. 
It is a web application that detects changes and notifies the user of keyword matches via email. 
In addition, LiteWatch allows user to manage their own data, so that their experience is not pestered with automated advertisements.

LiteWatch is built using Django.

## Local Installation
1. Clone Repo
2. Install modules (located in requirements.txt)
    * django-crontab needs to be installed via pip in the litewatch environment
3. Make django migrations (python ./manage.py migrate)

## Database Setup for Running Locally
These steps assume use of PostgreSQL database. The original web app used Heroku Postgres add-on 
1. Create a config.py file in litewatch directory
2. Enter the following attributes of the postgres database in config.py:
> DATABASE_CONFIG = {
>    'NAME': "ASSOCIATED NAME",
>    'USER': "ASSOCIATED USER",
>    'PASSWORD': "ASSOCIATED PASSWORD",
>    'HOST': "HOST URL",
>    'PORT':  "PORT NUMBER",
> }

Additional steps for testing
In this project, a second heroku database was used strictly for testing. If the same setup is used, then the user must create their second database in heroku first, then:
1. In litewatch/config.py, enter teh following attributes of the postgres database:
> TEST_DATABASE_CONFIG = {
>    'NAME': 'ASSOCIATED NAME',
>    'USER': 'ASSOCIATED USER',
>    'PASSWORD': 'ASSOCIATED PASSWORD',
>    'HOST': 'HOST URL',
>    'PORT': 'PORT NUMBER',
>    'TEST': {
>        'NAME': 'ASSOCIATED NAME',
>    }
>}
2. Add a similar 'TEST' dictionary to the previously created DATABASE_CONFIG, using that databases name.



## Running Locally
Running locally can vary by IDE/OS. If using PyCharm Professional, simply pressing run in the toolbar will start the server. The user may have to select the Python interpreter and edit the run configuration to run a Django server from the browser when using PyCharm. 
Otherwise, the steps are as follows:
1. python ./manage.py migrate
    * Only necessary for first setup or after migrations were made
2. python ./manage.py runserver

## Heroku
https://litewatch.herokuapp.com/
