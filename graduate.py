from flask import Flask, request
import pickle
import numpy as np

# master variable - controls entire application
app = Flask(__name__)

# model loading
model_file = open("best_model_lr.pkl", "rb")
data = pickle.load(model_file)
model = data["model"]
scaler = data["scaler"]


# API endpoints
@app.route("/")
def home():
    return "<h1>🎓 Graduate Admission Predictor is Running!</h1>"


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return "Send a POST request with student details to get predictions."
    else:
        # post request with student data
        req_data = request.get_json()

        # Extract input fields
        gre = req_data.get("gre", 0)
        toefl = req_data.get("toefl", 0)
        rating = req_data.get("rating", 0)
        sop = req_data.get("sop", 0.0)
        lor = req_data.get("lor", 0.0)
        cgpa = req_data.get("cgpa", 0.0)
        research = req_data.get("research", 0)

        # Arrange features in training order
        input_data = np.array([[gre, toefl, rating, sop, lor, cgpa, research]])
        input_scaled = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_percent = np.clip(prediction * 100, 0, 100)

        # Interpret result
        if prediction_percent >= 70:
            status = "Excellent chances! 🎯"
        elif prediction_percent >= 50:
            status = "Good prospects! ✨"
        else:
            status = "Needs improvement 💪"

        return {
            "chance_of_admit": f"{prediction_percent:.1f}%",
            "numeric_score": round(prediction_percent, 2),
            "status": status,
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
