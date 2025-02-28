def encode_input(data):
    """Encodes the input fields to numerical values for prediction."""
    try:
        symptoms_mapping = {'Wheezing': 5, 'coughing': 0, 'shortness of Breath': 4}
        gender_mapping = {'Female': 0, 'Male': 1}
        smoking_mapping = {'Non-Smoker': 0, 'Ex-Smoker': 1, 'Current Smoker': 2}
        severity_mapping = {'high': 0, 'medium': 2, 'low': 1}

        encoded_data = {
            "Age": data["Age"],
            "Gender_encoded": gender_mapping.get(data["Gender"], None),
            "Smoking_Status_encoded": smoking_mapping.get(data["Smoking"], None),
            "Asthma_Diagnosis_encoded": 3 if data["Asthma"] == "Yes" else 0,
            "Symptoms_encoded": symptoms_mapping.get(data["Symptoms"], None),
            "Peak_Flow": data["Peak_Flow"]
        }

        # Check if any value is None (invalid category)
        if None in encoded_data.values():
            return {"error": "Invalid categorical values in input"}

        return encoded_data
    except KeyError as e:
        return {"error": f"Missing required field: {str(e)}"}

def decode_severity(severity_code):
    """Decodes severity levels."""
    severity_mapping = {0: "high", 2: "medium", 1: "low"}
    return severity_mapping.get(severity_code, "Unknown")

def decode_treatment(treatment_code):
    """Decodes treatment names based on encoded values."""
    treatment_mapping = {
    10: "Omalizumab", 9: "Mepolizumab", 23: "itraconazole", 20: "inhaler",
    14: "antibiotics", 19: "hypertonic saline", 7: "Intrapulmonary Percussive Ventilation",
    17: "consult doctor", 28: "saline nose drops", 30: "steroids to reduce inflammation",
    32: "x-ray", 21: "inhealer", 25: "oxygen", 16: "consult a doctor",
    12: "Pulmonary rehabilitation", 13: "Surgery", 4: "Chemotherapy",
    2: "Antibiotics", 3: "Antibiotics.", 15: "aspirin", 5: "Cough medicine",
    1: "Antibiotic", 22: "isotonic sodium chloride solution", 11: "Oseltamivir",
    6: "Diuretics", 0: "Adaptive servo-ventilation", 8: "Intravenous fluids",
    27: "rifampin", 26: "pyrazinamide", 18: "ethambutol", 24: "oxygen",
    29: "stay away from cold places", 31: "surgery"
}
    return treatment_mapping.get(treatment_code, "Unknown")
