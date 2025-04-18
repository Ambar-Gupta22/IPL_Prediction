import os
from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
from flask_cors import CORS  # Enable CORS for cross-origin requests

app = Flask(__name__)
CORS(app)  # Allow access from other origins (like React Native app)

# Load the pre-trained pipeline
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Define team and city options
teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
]

# Route for form-based interaction (browser)
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        # Extract form data
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        selected_city = request.form['city']
        target = int(request.form['target'])
        score = int(request.form['score'])
        overs = float(request.form['overs'])
        wickets = int(request.form['wickets'])

        # Calculate features
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        remaining_wickets = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [remaining_wickets],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Make prediction
        prediction = pipe.predict_proba(input_df)
        loss = prediction[0][0]
        win = prediction[0][1]

        result = {
            'batting_team': batting_team,
            'bowling_team': bowling_team,
            'win': round(win * 100),
            'loss': round(loss * 100)
        }

    return render_template('index.html', teams=sorted(teams), cities=sorted(cities), result=result)


# Route for API interaction with React Native app
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    batting_team = data['batting_team']
    bowling_team = data['bowling_team']
    selected_city = data['city']
    target = int(data['target'])
    score = int(data['score'])
    overs = float(data['overs'])
    wickets = int(data['wickets'])

    # Calculate features
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    remaining_wickets = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    # Create dataframe for prediction
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [remaining_wickets],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    # Predict
    prediction = pipe.predict_proba(input_df)
    loss = prediction[0][0]
    win = prediction[0][1]

    return jsonify({
        'win': round(win * 100),
        'loss': round(loss * 100)
    })


if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)