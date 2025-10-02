import joblib
import pandas as pd


# Load model once when Django starts
model = joblib.load("solar_app/predicting_Solar_Irradiance_model.pkl")


# Column order must match what you used in training
FEATURE_COLUMNS = [
    "Year","Month","Day","Humidity","Precipitation","Temprature","MAX_Temp","MIN_Temp","Pressure","Wind_Speed","AQI"
]

def predict_solar_irradiance(record: dict):
    # data is a Python list of 11 values
    df = pd.DataFrame([[record[col] for col in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
    prediction = model.predict(df)
    return prediction[0]
