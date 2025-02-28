This project was developed under the guidance of my mentor, Mr. Yash Gupta, Senior Lead Engineer at Alveofit.

In this project, I built an API that accepts input in JSON format and returns output in JSON format.

Example:
Input - 
{
  "Age": 43,
  "Gender": "Male",
  "Smoking": "Ex-Smoker",
  "Asthma": "Yes",
  "Symptoms": "Coughing",
  "Peak_Flow": 221
}

Output:
{
  "Severity": "High",
  "Treatment": "Mepolizumab"
}

The model was trained on a limited dataset, so it provides treatment recommendations for only four diseases.
The input text must be formatted correctly to generate a valid output. (Refer to encoders.py for details.)
Future Improvements: The model can be trained on a larger dataset to improve predictions and support more diseases and symptoms.
