from flask import Flask, request, render_template
import pickle
import pandas as pd
from flask_cors import CORS  # Enable CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin access

# Load the pre-trained model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Define team and city options
teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None  # Default result is None
    if request.method == 'POST':
        # Extract form data
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        selected_city = request.form['city']
        target = int(request.form['target'])
        score = int(request.form['score'])
        overs = float(request.form['overs'])
        wickets = int(request.form['wickets'])

        # Calculate input features
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        remaining_wickets = 10 - wickets
        crr = score / overs if overs > 0 else 0  # Handle division by zero
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0  # Handle division by zero

        # Create input dataframe
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

        # Predict probabilities
        prediction = pipe.predict_proba(input_df)
        loss = prediction[0][0]
        win = prediction[0][1]

        result = {
            'batting_team': batting_team,
            'bowling_team': bowling_team,
            'win': round(win * 100),
            'loss': round(loss * 100)
        }

    # Render template with or without results
    return render_template('index.html', teams=sorted(teams), cities=sorted(cities), result=result)

if __name__ == '__main__':
    app.run(debug=True)
