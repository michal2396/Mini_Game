from flask import Flask, render_template, jsonify
from flask_cors import CORS
import random
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)

# The initial user and goal locations
user_location = {'lat': 0, 'lon': 0}
goal_location = {'lat': 0, 'lon': 0}


def generate_goal():
    """Generate a random goal location within a 1 km radius from the user"""
    goal_location['lat'] = user_location['lat'] + random.uniform(-0.01, 0.01)
    goal_location['lon'] = user_location['lon'] + random.uniform(-0.01, 0.01)
    return goal_location


@app.route('/')
def index():
    return render_template('index.html', user_location=user_location, goal_location=goal_location)


@app.route('/generate_goal')
def generate():
    return generate_goal()


@app.route('/update_location/<float:lat>/<float:lon>')
def update_location(lat, lon):
    global user_location
    user_location = {'lat': lat, 'lon': lon}

    # Check if the user is within 10m of the goal using geopy's geodesic
    distance_to_goal = geodesic((user_location['lat'], user_location['lon']),
                                (goal_location['lat'], goal_location['lon'])).meters

    if distance_to_goal < 10:
        # generate_goal()
        return jsonify({'message': 'Goal!'})

    return jsonify({'message': ''})


if __name__ == '__main__':
    generate_goal()
    app.run(debug=True)
