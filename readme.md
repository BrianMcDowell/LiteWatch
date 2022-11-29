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

## Running Locally
Running locally can vary by IDE/OS. If using PyCharm Professional, simply pressing run in the toolbar will start the server. The user may have to select the Python interpreter and edit the run configuration to run a Django server from the browser when using PyCharm. 
Otherwise, the steps are as follows:
1. python ./manage.py runserver

## Heroku
https://litewatch.herokuapp.com/
