from flask import Flask, render_template, request, session
from location import *
from database import login, insert_contacts
import os

app = Flask(__name__)
app.secret_key = os.getenv('app_secret_key')
app.config['SESSION_TYPE'] = 'memcache'


@app.route('/')
def index():
    lat, lon, ip = get_user_location()
    session['ip'] = ip
    session['lat'] = lat
    session['lon'] = lon
    login_data = login(ip)
    if login_data == 'user created' or login_data[0][1] is None:
        return render_template('index.html')
    else:
        session['contacts'] = login_data
        return render_template('sos.html')
    # return render_template('sos.html')


@app.route('/sos')
def sos():
    return render_template('sos.html')


@app.route('/location')
def location():
    return render_template('location.html')


@app.route('/sos_message', methods=["POST"])
def sos_message():
    print("SOS Message Received")
    user_location = (session['lat'], session['lon'])
    distances, police_data = nearest_police_stations(user_location)
    a, b, c = map_plotting(user_location, distances, police_data)
    a.save('map.html', close_file=False)
    cwd = os.getcwd()
    os.replace(cwd + '/map.html', cwd + '/templates/map.html')
    return "SOS Message Received"


@app.route('/add_contacts', methods=["POST"])
def add_contacts():
    if request.method == "POST":
        contacts = []
        for contact in request.form:
            contacts.append(request.form[contact])
        insert_contacts(session['ip'], contacts)
        return 'request received'


@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == '__main__':
    app.run()
