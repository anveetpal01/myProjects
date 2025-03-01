from flask import Flask, request, jsonify
import xgboost as xgb
import numpy as np
import pandas as pd
import logging
import os
import pickle
from encoders.encoders import encode_input, decode_severity, decode_treatment

app = Flask(__name__)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(filename="logs/api.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load models
try:
    with open("models/xgboost_model_severity_pred2.pkl", "rb") as file:
        severity_model = pickle.load(file)

    with open("models/xgboost_model_treat_pred.pkl", "rb") as file:
        treatment_model = pickle.load(file)
except Exception as e:
    logging.error(f"Error loading models: {str(e)}")
    raise RuntimeError("Failed to load models. Please check model paths and files.") from e

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data
        data = request.json
        if not data:
            return jsonify({"error": "No input provided"}), 400

        # Ensure input is a list (to support multiple patients)
        if isinstance(data, dict):
            data = [data]  # Convert single patient input to a list

        # Encode inputs for severity prediction
        encoded_inputs = [encode_input(patient) for patient in data]

        # Check if any encoding errors occurred
        for encoded_input in encoded_inputs:
            if "error" in encoded_input:
                return jsonify(encoded_input), 400

        # Define feature order for severity model
        severity_features = ['Age', 'Gender_encoded', 'Smoking_Status_encoded', 'Asthma_Diagnosis_encoded', 'Symptoms_encoded', 'Peak_Flow']
        df_severity = pd.DataFrame(encoded_inputs)[severity_features]

        # Predict severity for all patients
        severity_preds = severity_model.predict(df_severity)
        severity_labels = [decode_severity(int(pred)) for pred in severity_preds]

        # Prepare treatment model inputs
        treatment_inputs = [
            {
                "Symptoms_encoded": encoded_inputs[i]["Symptoms_encoded"],
                "Sex_encoded": encoded_inputs[i]["Gender_encoded"],
                "Age": encoded_inputs[i]["Age"],
                "Disease_encoded": 3,  # Asthma -> Disease_encoded (always 3)
                "Nature_encoded": int(severity_preds[i])  # Severity output -> Nature_encoded
            }
            for i in range(len(data))
        ]

        # Define feature order for treatment model
        treatment_features = ['Symptoms_encoded', 'Sex_encoded', 'Age', 'Disease_encoded', 'Nature_encoded']
        df_treatment = pd.DataFrame(treatment_inputs)[treatment_features]

        # Predict treatment for all patients
        treatment_preds = treatment_model.predict(df_treatment)
        treatment_labels = [decode_treatment(int(pred)) for pred in treatment_preds]

        # Prepare and return response
        response = [
            {"Severity": severity_labels[i], "Treatment": treatment_labels[i]}
            for i in range(len(data))
        ]

        logging.info(f"Input: {data}, Response: {response}")
        return jsonify(response)

    except Exception as e:
        logging.error(f"Error processing input {data}: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
