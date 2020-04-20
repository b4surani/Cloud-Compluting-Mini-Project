from flask import Flask, Blueprint, url_for
from flask import flash, redirect, render_template, request, session, abort, jsonify, json
from flask_login import login_required, current_user, LoginManager, login_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
import os

app = Flask(__name__)

main = Blueprint('main', __name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tutorial.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def display(self):
        return {"id": self.id,
                "username": self.username,
                "email": self.email}


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/allusers', methods=['GET'])
def alluser():
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email == "admin@admin.com"):
        data = User.query.all()
        users = []
        for d in data:
            users.append(d.display())
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        with open('./tutorial.json', 'w') as json_file:
            json.dump(output, json_file)
        return jsonify({'users': users})
        # users = User.query.all()
        # # drop_column(users, users.password)
        # user_schema = UserSchema(many=True)
        # output = user_schema.dump(users)
        # with open('./tutorial.json', 'w') as json_file:
        #     json.dump(output, json_file)
        # return jsonify({'users': output})
    else:
        flash('Please login with admin credentials!')
        return redirect(url_for('login'))


def index():
    users = User.query.all()
    # drop_column(users, users.password)
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users)
    with open('./tutorial.json', 'w') as json_file:
        json.dump(output, json_file)
    # return jsonify({'users': output})


@app.route('/allusers/<name>', methods=['GET'])
def alluser_name(name):
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email == "admin@admin.com"):
        data = User.query.filter_by(username=name).all()
        users = []
        for d in data:
            users.append(d.display())
        return jsonify({'users': users})
    else:
        flash('Please login with admin credentials!')
        return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def home():
    user1check = current_user.is_authenticated
    if user1check:
        return render_template('home.html', name=current_user.username)
    else:
        return render_template('home.html', name='User')


@app.route('/profile', methods=['GET'])
def profile():
    user1check = current_user.is_authenticated
    if user1check:
        return render_template('profile.html', name=current_user.username)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))


@app.route('/profile', methods=['POST'])
def profile_post():
    email = current_user.email
    password = request.form.get('password1')
    newpassword = request.form.get('password2')
    query = User.query.filter(User.email.in_([email])).first()
    if query:
        check = check_password_hash(query.password, password)
        if check:
            password = generate_password_hash(newpassword, method='sha256')
            query.password = password
            db.session.commit()
            index()
            flash('Password updated successfully.')
            return redirect(url_for('profile'))
        else:
            flash('Please check your current password and try again.')
            return redirect(url_for('profile'))
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))


@app.route('/profile/delete', methods=['POST', 'GET'])
def profile_delete():
    user1check = current_user.is_authenticated
    if user1check:
        email = current_user.email
        query = User.query.filter(User.email.in_([email])).first()
        db.session.delete(query)
        db.session.commit()
        index()
        # with open('./tutorial.json', 'r') as data_file:
        #     data = json.load(data_file)
        # for element in data:
        #     del element[current_user.id]
        #     del element[current_user.email]
        #     del element[current_user.username]
        #     del element[current_user.password]
        flash('User deleted successfully.')
        return redirect(url_for('login'))
    else:
        flash('Please login first!')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    user1check = current_user.is_authenticated
    if user1check:
        logout_user()
        flash('You have successfully logged out.')
    else:
        pass
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    query = User.query.filter(User.email.in_([email])).first()
    if query:
        check = check_password_hash(query.password, password)
        if check:
            user = User.query.filter(User.email.in_([email])).first()
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Please check your password and try again.')
            return redirect(url_for('login'))
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET'])
def signup():
    user1check = current_user.is_authenticated
    if user1check:
        logout_user()
        flash('You have successfully logged out.')
    else:
        pass
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password = generate_password_hash(password, method='sha256')
    query = User.query.filter(User.email.in_([email])).first()
    if query:
        flash('Email address already exists')
        return redirect(url_for('signup'))
    else:
        new_user = User(email=email, username=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        index()
        # user_schema = UserSchema()
        # output = user_schema.dump(new_user)
        # with open('./tutorial.json', 'a') as json_file:
        #     json.dump(output, json_file)
        flash('Signup successful, please login!')
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    user1check = current_user.is_authenticated
    if user1check:
        logout_user()
        flash('You have successfully logged out.')
        return redirect(url_for('home'))
    else:
        flash('Please login first!')
        return redirect(url_for('login'))


@app.route('/explore', methods=['GET'])
def explore():
    user1check = current_user.is_authenticated
    if user1check:
        return render_template('explore.html')
    else:
        flash('Please enter your login details.')
        return redirect(url_for('login'))


@app.route('/explore', methods=['POST', 'GET'])
def explore_post():
    # https: // api.sunrise - sunset.org / json?lat = 36.7201600 & lng = -4.4203400 & date = 2020 - 04 - 19
    api_url_temp = "https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}"
    lat = request.form.get('latitude')  # 36.7201600
    lng = request.form.get('longitude')  # -4.4203400
    date = request.form.get('date')  # 2020-04-19
    if not all([lat, lng]):
        flash('Latitude and Longitude are mandatory.')
        return redirect(url_for('explore'))
    elif lat == '0' or lng == '0':
        flash('Latitude and Longitude are non zero value.')
        return redirect(url_for('explore'))
    else:
        api_url = api_url_temp.format(lat=lat, lng=lng, date=date)
        print(api_url)
        response = requests.get(api_url)
        try:
            if response.ok:
                return jsonify(response.json())
            else:
                print(response.reason)
        except Exception:
            error = str(response.status_code) + " " + response.reason
            flash(error)
        # return redirect(url_for('explore'))


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/delete', methods=['GET'])
def delete():
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email=="admin@admin.com"):
        return render_template('delete.html')
    else:
        flash('Please login with admin credentials!')
        return redirect(url_for('login'))


@app.route('/delete', methods=['GET', 'POST'])
def delete_post():
    user1check = current_user.is_authenticated
    if (user1check) and (current_user.email=="admin@admin.com"):
        email = request.form.get('email')
        query = User.query.filter(User.email.in_([email])).first()
        db.session.delete(query)
        db.session.commit()
        index()
        # with open('./tutorial.json', 'r') as data_file:
        #     data = json.load(data_file)
        # for element in data:
        #     del element[current_user.id]
        #     del element[current_user.email]
        #     del element[current_user.username]
        #     del element[current_user.password]
        flash('User deleted successfully.')
        return redirect(url_for('delete'))
    else:
        flash('Please login with admin credentials!')
        return redirect(url_for('login'))


@app.route('/covid', methods=['GET'])
def covid():
    return render_template('covid.html')


@app.route('/covid/stat', methods=['POST', 'GET'])
def covid_stat():
    # https://thevirustracker.com/free-api?global=stats
    api_url = "https://thevirustracker.com/free-api?global=stats"
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


@app.route('/covid/time', methods=['POST', 'GET'])
def covid_time():
    # https://thevirustracker.com/timeline/map-data.json
    api_url = "https://thevirustracker.com/timeline/map-data.json"
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


@app.route('/covid/count', methods=['POST', 'GET'])
def covid_count():
    # https://thevirustracker.com/free-api?countryTimeline=US
    api_url_temp = "https://thevirustracker.com/free-api?countryTimeline={code}"
    code = request.form.get('code')  # UK, IN
    if not all([code]):
        flash('Country Code is mandatory.')
        return redirect(url_for('covid'))
    else:
        api_url = api_url_temp.format(code=code)
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


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0')
