# Cloud Computing Project

This mini project provides Sunset and Sunrise Times using pubic API from sunrise-sunset.org and corona virus statistics from thevirsutracker.com's Coronavirus Data API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Firstly you need to install Python3, to do so open terminal window and run following commands:

```
apt install python
apt install python3
```

### Installing

Now install required libraries and modules to support project execution and for that run following commands in terminal window:

```
pip install flask
pip install flask-login
pip install flask-sqlalchemy
pip install flask-marshmallow
pip install werkzeug
pip install requests
```

### Run Project

Once everthing is done, download project data to project directory. Now open terminal window -> navigate to project directory and run application file as follows:

```
python3 app.py
```

## Running the tests

Once you will run the project, it will be hosted on your local server or cloud server. You need to go to your browser and open local IP or cloud IP with port address 5000.

```
http://localhost:5000/ #home page
```

### Break down into end to end URLs

You will be able to access home screen of web application, where you can sign up and reigster a user, it will store user data in SQlite database in the root directory of the project.

```
http://localhost:5000/ #home page
http://localhost:5000/signup #signup page
http://localhost:5000/signup #to enter signup details 
```

Once you signed up, you can login to access your profile, it will jump to home screen with greeting. You can navigate to Profile section, here you can change your password by entering current password and new password, it reverts on changrs made. Here you can also delete your accout and it will return to login screen. 

```
http://localhost:5000/login #login page
http://localhost:5000/login #to enter log in credentials
http://localhost:5000/profile #profile page
http://localhost:5000/profile #to get new password
http://localhost:5000/profile #to delete account
```

Following to that is Explore section, where you can access sunrise and sunset API, this creates a GET request to public API to get sunrise time, sunset time and day length of your location. You need to enter longitude and latitude of your location's geographical coordinates to get timing of the that day. You can also enter a perticular date to check values. If date field is left blank, then API will consider current date.

```
http://localhost:5000/explore #explore page
http://localhost:5000/explore #to enter coordinates and request API
```

Next section is Covid-19, which is open for all the users including unauthrizes users on this web application. Here we have three API calling, first one is to get global statistics of the world, it will retunr total cases, total recovered and so on. 

```
http://localhost:5000/covid #covid page
http://localhost:5000/covid/stat #to request world stats API
```

Second API is to get timeline data of the corona virus cases, it is a corona virus tracker on day to day bases for each attected country. Here you can filter these data for a perticular date, where you will get staticstics for a perticular day for each attected country around the world.

```
http://localhost:5000/covid/time #to request world timeline API
http://localhost:5000/covid/time/date=4-19-20 #to filter world timeline by date
```

Last API is to track corona virus statistics of individual country. Here you need to enter country code to get timeline of corona virus cases of given country. Here you can request case count for a perticular date on given country.

```
http://localhost:5000/covid/count #to request country's timeline API
http://localhost:5000/covid/count/date=4-19-20 #to filter country's timeline by date
```

Finally you can click on Logout in navigation and user will be logged out from the session to home screen. The last section in navigation is About, which presents basic information about project and developer. 

```
http://localhost:5000/logout #to logout
http://localhost:5000/about #about page
```

### Some important URLs

You can create a user with email as admin@admin.com which acts as admin and it is set by developer. Admin can access details of all the registered user's email id and username in All Users section, it responses in json format and it can be filtered by name to quick search. Admin can also delete a user from delete tab in navigation bar.

```
http://localhost:5000/allusers #to list all users #admin access
http://localhost:5000/allusers/<name> #to filter a user from all users #admin access
http://localhost:5000/delete #delete page #admin access
http://localhost:5000/delete #to enter email and delete user #admin access
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
