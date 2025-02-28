In this project, I built an API that combines two XGBoost machine learning models. The API accepts input in JSON format and returns output in JSON format.

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

The input is first processed and encoded , then it passed to the severity prediction  model.
The input is then encoded and decoded internally to generate a suitable format for the treatment prediction model.
The final output is generated.

Output:
{
  "Severity": "High",
  "Treatment": "Mepolizumab"
}

The model was trained on a limited dataset, so it provides treatment recommendations for only four diseases.
The input text must be formatted correctly to generate a valid output. (Refer to encoders.py for details.)
Future Improvements: The model can be trained on a larger dataset to improve predictions and support more diseases and symptoms.
Note - Read temp file for more detail in each folder.
