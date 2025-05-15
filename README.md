# IPL Win Predictor

This project is an IPL Win Probability Predictor powered by a machine learning model trained on IPL match data. It includes:

- A Flask backend to serve predictions via a web UI or REST API.
- A React Native frontend to interact with the model via a mobile app.
- A trained `LogisticRegression` model with approximately **90% accuracy**.


 🎯 Features

- Predicts win probabilities based on real-time match conditions.
- Considers:
  - Batting team
  - Bowling team
  - Host city
  - Target score
  - Current score
  - Overs completed
  - Wickets lost
- Web interface (`index.html` served via Flask).
- API endpoint (`/predict`) for mobile or other integrations.
- Mobile app built using React Native.

⚙️ Technologies Used

- **Backend**: Python, Flask, Pandas, Scikit-learn
- **Frontend (Mobile)**: React Native (Expo), Axios, Picker
- **Deployment**: Render.com for backend hosting


 🚀 Setup Instructions

🔧 Backend (Flask)

1. Clone the repo:
   ```bash
   git clone <repo_url>
   cd <repo_name>
2.python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3.python train.py
4.python app.py

⚙️ app.py – Backend for IPL Match Win Prediction
This is the backend Flask application for the IPL Match Win Prediction System. It supports both a browser-based interface and a mobile app interface through RESTful APIs.

🚀 Features
- Predicts IPL match outcomes using a trained machine learning model.

- Accepts input through both a web form and JSON API.

- Returns win/loss probabilities in real-time.

- Mobile and web compatible.

📁 File Overview: app.py

# 1. Setup
from flask import Flask, request, render_template, jsonify
import pickle, pandas as pd
from flask_cors import CORS

# Flask app initialization
app = Flask(__name__)
CORS(app, origins=["*"])  # Enable CORS for cross-origin requests

# Load pre-trained ML pipeline
pipe = pickle.load(open('pipe.pkl', 'rb'))

⚙️ Web Interface Route (/)
This route serves an HTML form for users to manually enter match information:

Extracts values like batting_team, bowling_team, city, target, score, overs, wickets.

 - Computes derived features:

 - runs_left = target - score

 - balls_left = 120 - overs * 6

 - wickets = 10 - fallen_wickets

 - crr = score / overs

 - rrr = (runs_left * 6) / balls_left

Passes this data to the model for prediction.

Renders the results on the same page.

@app.route('/', methods=['GET', 'POST'])
def home():
    # Form-based prediction and result rendering
    
📱 API Route (/predict)
Used by mobile apps (like React Native):

Accepts POST requests with JSON body:
{
  "batting_team": "Chennai Super Kings",
  "bowling_team": "Mumbai Indians",
  "city": "Mumbai",
  "target": 180,
  "score": 100,
  "overs": 12.0,
  "wickets": 4
}
Returns prediction:
{
  "win": 64,
  "loss": 36
}

@app.route('/predict', methods=['POST'])
def predict():
    # JSON-based prediction API

🧠 Model Training and Export – model_training.py
This script is responsible for cleaning IPL match data, engineering features, training a machine learning model, and exporting the trained model pipeline (pipe.pkl) used by the Flask app.

📚 Datasets Used
matches.csv: Contains match-level information.

deliveries.csv: Contains ball-by-ball data of IPL matches.

🔄 Workflow Overview
1. Read and Explore Data
   match = pd.read_csv('matches.csv')
   delivery = pd.read_csv('deliveries.csv')
Loads match and delivery datasets using pandas.
2. Compute First Innings Total
   total_score_df = delivery.groupby(['match_id','inning']).sum()['total_runs'].reset_index()
   total_score_df = total_score_df[total_score_df['inning'] == 1]
Filters only first innings totals to set targets for the second innings.
3. Merge with Match Data
   match_df = match.merge(total_score_df, left_on='id', right_on='match_id')
Merges first innings total into match data to be used as the match target.
4. Team Name Standardization
   match_df['team1'] = match_df['team1'].str.replace(...)
   match_df['team2'] = match_df['team2'].str.replace(...)
Replaces old team names like Deccan Chargers and Delhi Daredevils with current names to ensure consistency.
5. Filter Relevant Matches
   match_df = match_df[match_df['team1'].isin(teams) & match_df['team2'].isin(teams)]
   match_df = match_df[match_df['dl_applied'] == 0]
Removes matches not involving key teams or those affected by the Duckworth-Lewis method.
6. Build Second Innings Delivery Data
   delivery_df = match_df.merge(delivery, on='match_id')
   delivery_df = delivery_df[delivery_df['inning'] == 2]
Keeps only second innings data for run chase prediction.

📈 Feature Engineering
Current Score: delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs_y'].cumsum()

Runs Left, Balls Left: 
 delivery_df['runs_left'] = total_runs_x - current_score 
 delivery_df['balls_left'] = 126 - (over * 6 + ball)

Wickets Left:
 delivery_df['player_dismissed'] = ...
 delivery_df['wickets'] = 10 - cumsum(player_dismissed)

 CRR and RRR:
  delivery_df['crr'] = (current_score * 6) / balls_used
  delivery_df['rrr'] = (runs_left * 6) / balls_left

 Match Result Label:
  delivery_df['result'] = 1 if batting_team == winner else 0

🧪 Model Training
 1. Final Dataset
    final_df = delivery_df[['batting_team','bowling_team','city','runs_left','balls_left','wickets','total_runs_x','crr','rrr','result']]
This is the final input dataset (X) and target (y).
2. Train/Test Split
   X_train, X_test, y_train, y_test = train_test_split(...)
3. Preprocessing Pipeline
    ColumnTransformer + OneHotEncoder for categorical features
4. Model Used
   Logistic Regression with liblinear solver
5. Model Evaluation
    accuracy_score(y_test, y_pred)

💾 Model Export
 pickle.dump(pipe, open('pipe.pkl', 'wb'))
Saves the trained pipeline (preprocessing + model) as a .pkl file for later use in the Flask API.

















