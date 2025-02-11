import joblib
import numpy as np
from django.conf import settings
import os
import pandas as pd

def load_model():
    model_path = "E:\Documents\PE\Master\S1\python\projet\Health_App\ML_models\knn_model.pkl"
    try:
        knn_loaded = joblib.load(model_path)
        return knn_loaded
    except FileNotFoundError:
        print("Model file not found.")
        return None

def make_diabetes_prediction(glucose, insulin, bmi, age):
    knn_loaded = load_model()
    if not knn_loaded:
        return "Model loading failed", None

    input_features = np.array([glucose, insulin, bmi, age], dtype=np.float64).reshape(1, -1)

    print("Input Shape for Model:", input_features.shape)  # Debugging output (should be (1, 4))

    prediction_proba = knn_loaded.predict_proba(input_features)[0][1]

    prediction = True if prediction_proba > 0.5 else False
    probability_percentage = round(prediction_proba * 100, 2)

    return prediction, probability_percentage




# Load the trained model
def load_maladie_classification_model():
    model_path = "E:\Documents\PE\Master\S1\python\projet\Health_App\ML_models\model_maladies.pkl"
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        print("Cancer Model file not found.")
        return None

classes = [ "Grippe", "Rougeole","COVID-19"] 

def maladie_classification(data):
    model=load_maladie_classification_model()
    df = pd.DataFrame([data])  # Convertir en DataFrame
    prediction = model.predict(df)[0]  # Faire la prédiction
    print(prediction)
    probabilities = model.predict_proba(df)[0]  # Obtenir les probabilités des classes
    
    # Associer chaque maladie à sa probabilité
    probability_dict = {classes[i]: round(probabilities[i] * 100, 2) for i in range(len(classes))}
    max_class = max(probability_dict, key=probability_dict.get)
    return max_class, probability_dict
