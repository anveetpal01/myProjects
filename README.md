This are the project made by me under the guidence of my mentor Mr. Yash Gupta sir Senior Lead Engineer of Alveofit.
I this project I made an api which takes an input of json format and give output in the json format.
For Example:
Input - 
{
"Age" : 43,
"Gender" : "Male",
"Smoking" : "Ex-Smoker",
"Asthma" : "Yes",
"Symptoms" : "coughing",
"Peak_Flow" : 221
}

Output - 
{
"Severity" : "high",
"Treatment" : "Mepolizumab"
}
Since this model is a trained on limited data so it gives treatment for limited disease only (only 4 disease).
Also the text of input is has to corrected for getting the output. (Check in encoders.py) 
Further this model is updated.
