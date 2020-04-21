# Cloud Computing Project

This mini project provides Sunset and Sunrise Times using pubic API from sunrise-sunset.org and corona virus statistics from thevirsutracker.com's Coronavirus Data API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Firstly you need to install Python3, to do so open terminal window and run following commands:

```
apt install python
apt install python3
apt install curl
```

### Installing

* Now install required libraries and modules to support project execution and for that run following commands in the terminal window:

```
pip install flask
pip install flask-login
pip install flask-sqlalchemy
pip install flask-marshmallow
pip install werkzeug
pip install requests
```

### Run Project

* Once everything is done, download project data to project directory. Now open terminal window -> navigate to project directory and run application file as follows:

```
python3 app.py
```

## Displaying

One start app will show the following options in the navigation bar

```
Home    Login    Signup    Covid-19    About
```

For an authorised user navigation bar will be as follows,

```
Home    Profile    Explore    Logout    Covid-19    About
```

For an admin navigation bar will look like as below with more options,

```
Home    Profile    Explore    All Users    Delete User    Logout    Covid-19    About
```

## Running the tests

Once you will run the project, it will be hosted on your local server or cloud server. 

* You need to go to your browser and open local IP or cloud IP with port address 5000.

```
http://localhost:5000/ #home page
```

### Break down into end to end URLs

* You will be able to access home screen of the web application, where you can sign up and register a user, it will store user data in SQLite database in the root directory of the project.

```
http://localhost:5000/ #home page
http://localhost:5000/signup #signup page #to enter signup details 
```

* Once you signed up, you can log in to access your profile, it will jump to the home screen with a greeting. You can navigate to Profile section, here you can change your password by entering the current password and new password, it reverts on changes made. Here you can also delete your account and it will return to the login screen. 

```
http://localhost:5000/login #login page #to enter log in credentials
http://localhost:5000/profile #profile page #to get new password #to delete account
```

* Following to that is Explore section, where you can access sunrise and sunset API, this creates a GET request to public API to get sunrise time, sunset time and day length of your location. You need to enter longitude and latitude of your location's geographical coordinates to get the timing of that day. You can also enter a particular date to check values. If the date field is left blank, then API will consider the current date.

```
http://localhost:5000/explore #explore page #to enter coordinates and request API
```

* Next section is Covid-19, which is open for all the users including unauthorized users on this web application. Here we have three API calls, the first one is to get global statistics of the world, it will return total cases, total recovered and so on. 

```
http://localhost:5000/covid #covid page
http://localhost:5000/covid/stat #to request world stats API
```

* Second API is to get timeline data of the corona virus cases, it is a corona virus tracker on a day to day bases for each affected country. Here you can filter these data for a particular date, where you will get statistics for a particular day for each affected country around the world.

```
http://localhost:5000/covid/time #to request world timeline API
http://localhost:5000/covid/time/date=4-19-20 #date=m-dd-yy #to filter world timeline by date
```

* the Last API is to track corona virus statistics of an individual country. Here you need to enter country code to get a timeline of corona virus cases of the given country. Here you can request case count for a particular date on the given country.

```
http://localhost:5000/covid/count #to request country's timeline API
http://localhost:5000/covid/count/date=4-19-20 #date=m-dd-yy #to filter country's timeline by date
```

* Finally you can click on Logout in navigation and user will be logged out from the session to the home screen. The last section in navigation is About, which presents basic information about the project and developer. 

```
http://localhost:5000/logout #to logout
http://localhost:5000/about #about page
```

### Some important URLs

* You can create a user with email as admin@admin.com which acts as admin and it is set by the developer. Admin can access details of all the registered user's email id and username in All Users section, it responses in JSON format and it can be filtered by name to quick search. Admin can also delete a user from delete tab in the navigation bar.

```
http://localhost:5000/allusers #to list all users #admin access
http://localhost:5000/allusers/<name> #to filter a user from all users #admin access
http://localhost:5000/delete #delete page #admin access #to enter email and delete user #admin access
```

## Curl Request

* User can update its username by following curl request from the terminal. But the user has to provide correct email address to do so, this is not a secure way of updating username though.

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"email": "enter user email"}' http://localhost:5000/database=NewUsername
```


## Security and Authentication

* The user database is secured with a private key.
* All user's password is encrypted using sha256 encryption method using werkzeug.security class of python library.
* All web pages have customized access to a feature of the web application as per user's authority level.

## Building Resources

* Linux Operating System 18.04
* Python Programming Language
* Pycharm IDE
* DB Browser
* Flask Web Development Framework
* Amazon Web Service EC2

## Authors

**BHARATKUMAR SURANI**
* MSc Student
* Intern of Things
* Queen Mary University of London
* Email: b.v.surani@se19.qmul.ac.uk

## Refrences

Following are the public API used for integration and demonstration.

* Sunrise and Sunset API: https://sunrise-sunset.org/api
* Thevirustracker Covid19: https://documenter.getpostman.com/view/8854915/SzS7R74n?version=latest#6a845d97-06b8-447b-a6dd-236bd3cb68f5
