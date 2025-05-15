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


