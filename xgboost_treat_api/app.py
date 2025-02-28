from flask import Flask, request, jsonify
import xgboost as xgb
import numpy as np
import pandas as pd
import logging
import os
from encoders.encoders import encode_input, decode_severity, decode_treatment
import pickle

app = Flask(__name__)

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(filename="logs/api.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load models
with open("models/xgboost_model_severity_pred2.pkl", "rb") as file:
    severity_model = pickle.load(file)

with open("models/xgboost_model_treat_pred.pkl", "rb") as file:
    treatment_model = pickle.load(file)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data
        data = request.json
        if not data:
            return jsonify({"error": "No input provided"}), 400

        # Encode input for severity prediction
        encoded_input = encode_input(data)
        if "error" in encoded_input:
            return jsonify(encoded_input), 400

        # Correct the feature order for severity model
        severity_features = ['Age', 'Gender_encoded', 'Smoking_Status_encoded', 'Asthma_Diagnosis_encoded', 'Symptoms_encoded', 'Peak_Flow']
        df_severity = pd.DataFrame([encoded_input])[severity_features]

        
        severity_pred = int(severity_model.predict(pd.DataFrame([encoded_input]))[0])

        # Decode severity prediction
        severity_label = decode_severity(severity_pred)

        # Create input for treatment model (internally transformed)
        treatment_input = {
            "Symptoms_encoded": encoded_input["Symptoms_encoded"],
            "Sex_encoded": encoded_input["Gender_encoded"],  # Gender -> Sex_encoded
            "Age": encoded_input["Age"],
            "Disease_encoded": 3,  # Asthma -> Disease_encoded (always 3)
            "Nature_encoded": severity_pred  # Severity output -> Nature_encoded
        }

        # Correct feature order for treatment model
        treatment_features = ['Symptoms_encoded', 'Sex_encoded', 'Age', 'Disease_encoded', 'Nature_encoded']
        df_treatment = pd.DataFrame([treatment_input])[treatment_features]

        treatment_pred = int(treatment_model.predict(pd.DataFrame([treatment_input]))[0])

        # Decode treatment prediction
        treatment_label = decode_treatment(treatment_pred)

        # Prepare final response
        response = {
            "Severity": severity_label,
            "Treatment": treatment_label
        }

        logging.info(f"Input: {data}, Response: {response}")
        return jsonify(response)

    except Exception as e:
        logging.error(f"Error processing input {data}: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
