from django.shortcuts import render
from aqi_calculator import calculate_current_aqi
from ml_model import predict_solar_irradiance
from datetime import datetime

# Create your views here.
import requests


lat=28.7041
lon= 77.1025

# 1. Get coordinates from city name using OpenStreetMap
def get_coordinates(city):
    url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    response = requests.get(url).json()
    if response:
        lat = float(response[0]["lat"])
        lon = float(response[0]["lon"])
        return lat, lon
    return None, None

# 2. Get weather using coordinates
def get_weather(lat, lon):
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    data = requests.get(url).json()
    try:
        temp = data["main"]["temp"] 
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        precipitation = data.get("rain", {}).get("1h", 0.0)
    except KeyError:
        return None
    return {"temperature": temp, "humidity": humidity, "pressure": pressure, "wind_speed": wind_speed,"temp_min":temp_min,"temp_max":temp_max,"precipitation": precipitation}

# 3. Get AQI using coordinates
def get_aqi(lat, lon):
    
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    data = requests.get(url).json()
    try:
        aqi = data["list"][0]["main"]["aqi"]  # AQI index
        PM2_5 =data["list"][0]["components"]["pm2_5"]
        PM10 =data["list"][0]["components"]["pm10"]
        NO2 =data["list"][0]["components"]["no2"]
        SO2 =data["list"][0]["components"]["so2"]
        CO =data["list"][0]["components"]["co"]
        Ozone =data["list"][0]["components"]["o3"]
    except (KeyError, IndexError):
        return None
    return {"aqi": aqi,"PM2_5":PM2_5,"PM10":PM10,"NO2":NO2,"SO2":SO2,"CO":CO,"Ozone":Ozone}

def calulate_aqi(lat,lon):
    api_data = get_aqi(lat, lon)
    
    if api_data:
        print("Raw API Response:", api_data)
        
        # Step 2: Pass pollutant values to our custom AQI calculator
        result = calculate_current_aqi(api_data)
        
        print("Calculated AQI:", result["AQI"])
        print("Category:", result["Category"])
    else:
        print("Error: Could not fetch AQI data from API")


def collect_environment_data(lat, lon):
    weather = get_weather(lat, lon)
    air = get_aqi(lat, lon)

    if not weather or not air:
        return None

    # Calculate AQI
    aqi_result = calculate_current_aqi(air)

    # Current date
    now = datetime.now()
    year, month, day = now.year, now.month, now.day

    record = {
        "Year": year,
        "Month": month,
        "Day": day,
        "Humidity": weather["humidity"],
        "Precipitation": weather["precipitation"],
        "Temprature": round(weather["temperature"], 2),
        "MAX_Temp": round(weather["temp_max"], 2),
        "MIN_Temp": round(weather["temp_min"], 2),
        "Pressure": weather["pressure"],
        "Wind_Speed": weather["wind_speed"],
        "AQI": aqi_result["AQI"]
    }
    if record:
        result = predict_solar_irradiance(record)
        print("Predicted Solar Irradiance:", result)

    return result


calulate_aqi(lat,lon)
collect_environment_data(lat, lon)