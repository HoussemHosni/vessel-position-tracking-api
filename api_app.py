import logging
import os
import requests
from db import db
from flask import Flask
from flask import render_template, request, session, redirect, url_for
from flask_restful import Api
from resources.vessel_position import VesselPosition, VesselsList
from update_trips import generate_map


app = Flask(__name__)

uri = os.environ.get("DATABASE_URL", 'sqlite:///data.db')

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "secret_key"

api = Api(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# define /add_position endpoint
@app.route('/add_position', methods=['GET', 'POST'])
def add_position():

    # When Submiting form
    if request.method == 'POST':
        for k, v in request.form.items():
            session[k] = v
        
        # retrieve json fields entered in the "add position" form
        data = {
                "vessel_id": session["vessel_id"],
                "latitude": session["latitude"],
                "longitude": session["longitude"],
                "position_time": session["position_time"]
        }
        try:
            response = requests.post(f"http://127.0.0.1:5000/vessel/{data['vessel_id']}", data = data)
        except:
            logging.error('Failed to insert vessel position into the database')
            pass
        return redirect(url_for('show_trips'))

    return render_template('add_position.html')

# define /trips/ endpoint 
@app.route('/trips/', methods=['GET'])
def show_trips():
    # fetch database vessels positions and update Trips Graph
    generate_map()
    # return trips.html containing the updated chart
    return render_template('trips.html')

# add api resources
api.add_resource(VesselPosition, '/vessel/<int:vessel_id>')
api.add_resource(VesselsList, '/vessels')

if __name__ == '__main__':
    app.run(debug=True)