import joblib
import numpy as np
from django.conf import settings
import os

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
def load_cancer_model():
    model_path = "E:\\Documents\\PE\\Master\\S1\\python\\Health_Project\\Health_Project\\Health_App\\ML_models\\cancer_detection_model.pkl"
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        print("Cancer Model file not found.")
        return None

def make_cancer_prediction(radius_mean, texture_mean, perimeter_mean, area_mean):
    model = load_cancer_model()
    if not model:
        return "Model loading failed", None

    # Prepare input array (ensure correct shape)
    input_features = np.array([[radius_mean, texture_mean, perimeter_mean, area_mean]], dtype=np.float64)

    print("Input Shape for Model:", input_features.shape)  # Debugging output (should be (1, 4))

    # Predict the probability
    prediction_proba = model.predict_proba(input_features)[0][1]

    # Determine prediction and probability percentage
    prediction = "Malignant" if prediction_proba > 0.5 else "Benign"
    probability_percentage = round(prediction_proba * 100, 2)

    return prediction, probability_percentage

