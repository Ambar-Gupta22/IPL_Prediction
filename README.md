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

