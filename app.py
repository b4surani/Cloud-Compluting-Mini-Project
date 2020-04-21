from flask import Flask, Blueprint, url_for
from flask import flash, redirect, render_template, request, session, abort, jsonify, json
from flask_login import login_required, current_user, LoginManager, login_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
import os

# Definition of required variables
app = Flask(__name__)
main = Blueprint('main', __name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tutorial.db'
cc = 'GB'

# Initialization of Database and Login Manager
db = SQLAlchemy(app)
ma = Marshmallow(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):    # User database definition for tabular data
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))


    def display(self):  # User database definition for raw data
        return {"id": self.id,
                "username": self.username,
                "email": self.email}


class UserSchema(ma.ModelSchema):   # UserSchema database initialization
    class Meta:
        model = User


@login_manager.user_loader  # Load user from database
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/allusers', methods=['GET'])    # Display all users to admin
def alluser():
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email == "admin@admin.com"):  # Check if user is admin and logged in
        data = User.query.all()     # Get all user data
        users = []
        for d in data:
            users.append(d.display())   # Append all data in d to users
        return jsonify({'users': users}), 200   # Display all user as json
        # users = User.query.all()
        # # drop_column(users, users.password)
        # user_schema = UserSchema(many=True)
        # output = user_schema.dump(users)
        # with open('./tutorial.json', 'w') as json_file:
        #     json.dump(output, json_file)
        # return jsonify({'users': output})
    else:
        flash('Please login with admin credentials! 401')   # Flash message
        return redirect(url_for('login'))   # Redirect to a page


def index():    # Generate json from database
    users = User.query.all()
    user_schema = UserSchema(many=True)  # Set multi entry in user_schema
    output = user_schema.dump(users)  # Dump all users to output
    with open('./tutorial.json', 'w') as json_file:  # Write on json file
        json.dump(output, json_file)  # Load all data to json file
    # return jsonify({'users': output})


@app.route('/allusers/<name>', methods=['GET'])     # Filter by name from all users
def alluser_name(name):
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email == "admin@admin.com"):
        data = User.query.filter_by(username=name).all()    # Look for particular user
        users = []
        for d in data:
            users.append(d.display())
        return jsonify({'users': users}), 200
    else:
        flash('Please login with admin credentials! 401')
        return redirect(url_for('login'))


@app.route('/', methods=['GET'])    # home page
def home():
    user1check = current_user.is_authenticated
    if user1check:     # Check if user is logged in
        return render_template('home.html', name=current_user.username)     # Revert with username to template
    else:
        return render_template('home.html', name='User')


@app.route('/profile', methods=['GET'])     # Profile page
def profile():
    user1check = current_user.is_authenticated
    if user1check:
        return render_template('profile.html', name=current_user.username)
    else:
        flash('Please login first! 401')
        return redirect(url_for('login'))


@app.route('/profile', methods=['POST'])    # Profile page to update password
def profile_post():
    email = current_user.email      # Get current user
    password = request.form.get('password1')    # Old password
    newpassword = request.form.get('password2')     # New password
    query = User.query.filter(User.email.in_([email])).first()  # Query current user in database
    if query:
        check = check_password_hash(query.password, password)   # Check old password in database
        if check:
            password = generate_password_hash(newpassword, method='sha256')     # Encrypt new password
            query.password = password   # Update new password
            db.session.commit()     # Commit changes in database
            index()     # Regenerate json file
            flash('Password updated successfully. 201')
            return redirect(url_for('profile'))
        else:
            flash('Please check your current password and try again. 404')
            return redirect(url_for('profile'))
    else:
        flash('Please check your login details and try again. 401')
        return redirect(url_for('login'))


@app.route('/profile/delete', methods=['POST', 'GET'])      # Profile page to delete user
def profile_delete():
    user1check = current_user.is_authenticated
    if user1check:
        email = current_user.email
        query = User.query.filter(User.email.in_([email])).first()
        db.session.delete(query)    # Delete user from database
        db.session.commit()
        index()
        # with open('./tutorial.json', 'r') as data_file:
        #     data = json.load(data_file)
        # for element in data:
        #     del element[current_user.id]
        #     del element[current_user.email]
        #     del element[current_user.username]
        #     del element[current_user.password]
        flash('User deleted successfully. 201')
        return redirect(url_for('login'))
    else:
        flash('Please login first! 401')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET'])   # Login page
def login():
    user1check = current_user.is_authenticated
    if user1check:
        logout_user()   # Logout user from session
        flash('You have logged out from session. 200')
    else:
        pass
    return render_template('login.html')


@app.route('/login', methods=['POST'])      # Login page to enter credentials
def login_post():
    email = request.form.get('email')       # Get from page
    password = request.form.get('password')
    query = User.query.filter(User.email.in_([email])).first()
    if query:       # Check ID
        check = check_password_hash(query.password, password)
        if check:       # Check Password
            user = User.query.filter(User.email.in_([email])).first()      # Get user data
            login_user(user)    # Login to the session
            return redirect(url_for('home'))
        else:
            flash('Please check your password and try again. 404')
            return redirect(url_for('login'))
    else:
        flash('Please check your login details and try again. 401')
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET'])      # Signup page
def signup():
    user1check = current_user.is_authenticated
    if user1check:
        logout_user()
        flash('You have successfully logged out. 200')
    else:
        pass
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])     # Signup page to register new user
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password = generate_password_hash(password, method='sha256')       # Encrypt password
    query = User.query.filter(User.email.in_([email])).first()
    if query:
        flash('Email address already exist. 400')
        return redirect(url_for('signup'))
    else:
        new_user = User(email=email, username=name, password=password)      # Get new user data
        db.session.add(new_user)    # Add new user to database
        db.session.commit()
        index()
        # user_schema = UserSchema()
        # output = user_schema.dump(new_user)
        # with open('./tutorial.json', 'a') as json_file:
        #     json.dump(output, json_file)
        flash('Signup successful, please login! 201')
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])      # Logout page
def logout():
    user1check = current_user.is_authenticated
    if user1check:
        logout_user()
        flash('You have successfully logged out. 200')
        return redirect(url_for('home'))
    else:
        flash('Please login first! 401')
        return redirect(url_for('login'))


@app.route('/explore', methods=['GET'])     # Explore page
def explore():
    user1check = current_user.is_authenticated
    if user1check:
        return render_template('explore.html')
    else:
        flash('Please enter your login details. 401')
        return redirect(url_for('login'))


@app.route('/explore', methods=['POST'])     # Explore page to request API
def explore_post():
    # https: // api.sunrise - sunset.org / json?lat = 36.7201600 & lng = -4.4203400 & date = 2020 - 04 - 19
    api_url_temp = "https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}"    # API format
    lat = request.form.get('latitude')  # 36.7201600
    lng = request.form.get('longitude')  # -4.4203400
    date = request.form.get('date')  # 2020-04-19
    if not all([lat, lng]):     # Two fields are mandatory
        flash('Latitude and Longitude are mandatory. 400')
        return redirect(url_for('explore'))
    elif lat == '0' or lng == '0':      # Two fields are non zero
        flash('Latitude and Longitude are non zero value. 404')
        return redirect(url_for('explore'))
    else:
        api_url = api_url_temp.format(lat=lat, lng=lng, date=date)      # Load data to API format
        response = requests.get(api_url)    # Request to API
        try:
            if response.ok:     # Response is okay
                parsed_json = response.json()   # Parse response data
                res = [{'Sunrise Time': parsed_json['results']['sunrise'], 'Sunset Time': parsed_json['results']['sunset'], 'Day Length': parsed_json['results']['day_length']}]    # Get required variables
                return jsonify(res), 200     # Display as a json
            else:
                print(response.reason)
        except Exception:
            error = str(response.status_code) + " " + response.reason   # Show error with reason
            flash(error)
        # return redirect(url_for('explore'))


@app.route('/about', methods=['GET'])   # About page
def about():
    return render_template('about.html')


@app.route('/delete', methods=['GET'])      # Delete user page for admin
def delete():
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email == "admin@admin.com"):
        return render_template('delete.html')
    else:
        flash('Please login with admin credentials!, 401')
        return redirect(url_for('login'))


@app.route('/delete', methods=['POST'])      # Delete a user
def delete_post():
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email == "admin@admin.com"):
        email = request.form.get('email')
        query = User.query.filter(User.email.in_([email])).first()
        if query:
            db.session.delete(query)        # Delete queried user from database
            db.session.commit()
            index()
        # with open('./tutorial.json', 'r') as data_file:
        #     data = json.load(data_file)
        # for element in data:
        #     del element[current_user.id]
        #     del element[current_user.email]
        #     del element[current_user.username]
        #     del element[current_user.password]
            flash('User deleted successfully. 200')
            return redirect(url_for('delete'))
        else:
            flash('User not found. 404')
            return redirect(url_for('delete'))
    else:
        flash('Please login with admin credentials! 401')
        return redirect(url_for('login'))


@app.route('/covid', methods=['GET'])       # Covid page
def covid():
    return render_template('covid.html')


@app.route('/covid/stat', methods=['POST', 'GET'])  # Covid API world stats
def covid_stat():
    # https://thevirustracker.com/free-api?global=stats
    api_url = "https://thevirustracker.com/free-api?global=stats"   # API
    response = requests.get(api_url)
    try:
        if response.ok:
            return jsonify(response.json())
        else:
            print(response.reason)
    except Exception:
        error = str(response.status_code) + " " + response.reason
        flash(error)
    return redirect(url_for('covid'))


@app.route('/covid/time', methods=['POST', 'GET'])  # Covid API for timeline
def covid_time():
    # https://thevirustracker.com/timeline/map-data.json
    api_url = "https://thevirustracker.com/timeline/map-data.json"
    response = requests.get(api_url)
    try:
        if response.ok:
            return jsonify(response.json()), 200
        else:
            print(response.reason)
    except Exception:
        error = str(response.status_code) + " " + response.reason
        flash(error)
    return redirect(url_for('covid'))


@app.route('/covid/time/date=<date>', methods=['GET'])      # Covid API for filtered data of timeline
def covid_time_date(date):
    # https://thevirustracker.com/timeline/map-data.json
    api_url = "https://thevirustracker.com/timeline/map-data.json"
    response = requests.get(api_url)
    date = date.replace('-', '/')       # Change - -> /
    try:
        if response.ok:
            parsed_json = response.json()
            res = []
            for c in parsed_json['data']:   # Check for date in json response
                if c['date'] == date:
                    res.append(c)       # Append data to new variable
                else:
                    pass
            print(res)
            return jsonify(res), 200     # Display json output
        else:
            print(response.reason)
    except Exception:
        error = str(response.status_code) + " " + response.reason
        flash(error)
    return redirect(url_for('covid'))


@app.route('/covid/count', methods=['POST', 'GET'])     # Covid API for Country timeline
def covid_count():
    # https://thevirustracker.com/free-api?countryTimeline=US
    api_url_temp = "https://thevirustracker.com/free-api?countryTimeline={code}"
    code = request.form.get('code')  # UK, IN       # Get code
    global cc       # Call global variable
    cc = code   # Save country code to global variable
    if not all([code]):
        flash('Country Code is mandatory.')
        return redirect(url_for('covid'))
    else:
        api_url = api_url_temp.format(code=code)        # Enter code to API
        response = requests.get(api_url)
        try:
            if response.ok:
                return jsonify(response.json()), 200
            else:
                print(response.reason)
        except Exception:
            error = str(response.status_code) + " " + response.reason
            flash(error)
    return redirect(url_for('covid'))


@app.route('/covid/count/date=<date>', methods=['GET'])     # Covid API for filtering country timeline
def covid_count_date(date):
    # https://thevirustracker.com/free-api?countryTimeline=US
    api_url_temp = "https://thevirustracker.com/free-api?countryTimeline={code}"
    code = cc  # UK, IN         # Get data from global variable
    if not all([code]):
        flash('Country Code is mandatory.')
        return redirect(url_for('covid'))
    else:
        api_url = api_url_temp.format(code=code)
        response = requests.get(api_url)
        date = date.replace('-', '/')
        try:
            if response.ok:
                parsed_json = response.json()['timelineitems']
                res = []
                for c in parsed_json[0].keys():     # Filter data from json response
                    if c == date:
                        res.append(parsed_json[0][c])  # Save to new variable
                    else:
                        pass
                return jsonify(res), 200
            else:
                print(response.reason)
        except Exception:
            print('Except')
            error = str(response.status_code) + " " + response.reason
            flash(error)
    return redirect(url_for('covid'))


@app.route('/database=<newname>', methods=['PUT'])      # To request new username filtered by email
def database_put(newname):
    rep = request.json
    if not request.json:
        return jsonify({'Abort 404'}), 404
    else:
        email = request.json['email']
        query = User.query.filter(User.email.in_([email])).first()
        query.username = newname
        db.session.commit()
        index()
        return jsonify('Success 200'), 200


if __name__ == "__main__":      # Run the mail application
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=80)
