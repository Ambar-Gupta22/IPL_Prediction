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
This is the backend Flask application for the IPL Match Win Prediction System. It serves both a browser-based frontend and a React Native mobile app via REST API.

📦 Features:
Predicts the winning probability of an IPL team based on live match data.

Supports form-based input (via HTML UI).

Provides a JSON-based API endpoint for integration with mobile apps (like React Native).

🔧 How it works:
1. Imports and Setup
python
Copy
Edit
from flask import Flask, request, render_template, jsonify
import pickle, pandas as pd
from flask_cors import CORS
Uses Flask for serving routes and handling HTTP requests.

Loads a pre-trained machine learning pipeline from pipe.pkl.

Enables Cross-Origin Resource Sharing (CORS) to allow frontend apps to interact during development.

2. Static Team and City Lists
python
Copy
Edit
teams = [ ... ]
cities = [ ... ]
Predefined IPL team and city names are used as valid options for prediction.

3. / Route – Web Interface
python
Copy
Edit
@app.route('/', methods=['GET', 'POST'])
Renders an HTML form (index.html) for user input.

On form submission (POST), it:

Extracts match parameters (team, city, target, score, etc.)

Computes match features like runs_left, balls_left, crr (Current Run Rate), rrr (Required Run Rate).

Creates a pandas.DataFrame to pass input into the model.

Gets win/loss probabilities using pipe.predict_proba(...).

Displays the result back to the browser.

4. /predict Route – API for Mobile App
python
Copy
Edit
@app.route('/predict', methods=['POST'])
Accepts JSON input from mobile apps.

Performs the same feature calculation and prediction steps as the web interface.

Returns a JSON response with win and loss percentages.

5. Model Prediction
python
Copy
Edit
prediction = pipe.predict_proba(input_df)
The ML model outputs probabilities for both win and loss classes.

Output is rounded and formatted for readability.

📡 Example JSON API Request
json
Copy
Edit
POST /predict
Content-Type: application/json

{
  "batting_team": "Chennai Super Kings",
  "bowling_team": "Mumbai Indians",
  "city": "Mumbai",
  "target": 180,
  "score": 100,
  "overs": 12.0,
  "wickets": 4
}
🧠 Output
json
Copy
Edit
{
  "win": 64,
  "loss": 36
}



