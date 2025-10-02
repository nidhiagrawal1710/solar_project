import numpy as np

# ---------- Subindex Functions ----------
def get_PM25_subindex(x):
    if x <= 30:
        return x * 50 / 30
    elif x <= 60:
        return 50 + (x - 30) * 50 / 30
    elif x <= 90:
        return 100 + (x - 60) * 100 / 30
    elif x <= 120:
        return 200 + (x - 90) * 100 / 30
    elif x <= 250:
        return 300 + (x - 120) * 100 / 130
    elif x > 250:
        return 400 + (x - 250) * 100 / 130
    else:
        return np.nan

def get_PM10_subindex(x):
    if x <= 50:
        return x
    elif x <= 100:
        return x
    elif x <= 250:
        return 100 + (x - 100) * 100 / 150
    elif x <= 350:
        return 200 + (x - 250)
    elif x <= 430:
        return 300 + (x - 350) * 100 / 80
    elif x > 430:
        return 400 + (x - 430) * 100 / 80
    else:
        return np.nan

def get_SO2_subindex(x):
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 380:
        return 100 + (x - 80) * 100 / 300
    elif x <= 800:
        return 200 + (x - 380) * 100 / 420
    elif x <= 1600:
        return 300 + (x - 800) * 100 / 800
    elif x > 1600:
        return 400 + (x - 1600) * 100 / 800
    else:
        return np.nan

def get_NOx_subindex(x):
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 180:
        return 100 + (x - 80) * 100 / 100
    elif x <= 280:
        return 200 + (x - 180) * 100 / 100
    elif x <= 400:
        return 300 + (x - 280) * 100 / 120
    elif x > 400:
        return 400 + (x - 400) * 100 / 120
    else:
        return np.nan

def get_CO_subindex(x):
    if x <= 1:
        return x * 50 / 1
    elif x <= 2:
        return 50 + (x - 1) * 50 / 1
    elif x <= 10:
        return 100 + (x - 2) * 100 / 8
    elif x <= 17:
        return 200 + (x - 10) * 100 / 7
    elif x <= 34:
        return 300 + (x - 17) * 100 / 17
    elif x > 34:
        return 400 + (x - 34) * 100 / 17
    else:
        return np.nan

def get_O3_subindex(x):
    if x <= 50:
        return x * 50 / 50
    elif x <= 100:
        return 50 + (x - 50) * 50 / 50
    elif x <= 168:
        return 100 + (x - 100) * 100 / 68
    elif x <= 208:
        return 200 + (x - 168) * 100 / 40
    elif x <= 748:
        return 300 + (x - 208) * 100 / 539
    elif x > 748:
        return 400 + (x - 748) * 100 / 539
    else:
        return np.nan

# ---------- AQI Category ----------
def get_AQI_bucket(x):
    if x <= 50:
        return "Good"
    elif x <= 100:
        return "Satisfactory"
    elif x <= 200:
        return "Moderate"
    elif x <= 300:
        return "Poor"
    elif x <= 400:
        return "Very Poor"
    elif x > 400:
        return "Severe"
    else:
        return "Unknown"

# ---------- AQI Calculation from API data ----------
def calculate_current_aqi(api_data: dict):
    # Extract pollutant values
    PM25 = api_data.get("PM2_5", np.nan)
    PM10 = api_data.get("PM10", np.nan)
    NO2  = api_data.get("NO2", np.nan)
    SO2  = api_data.get("SO2", np.nan)
    CO   = api_data.get("CO", np.nan)
    O3   = api_data.get("Ozone", np.nan)

    # ✅ Convert CO from µg/m³ to mg/m³
    if not np.isnan(CO):
        CO = CO / 1000.0

    # Calculate subindices
    subindices = [
        get_PM25_subindex(PM25) if PM25 is not None else np.nan,
        get_PM10_subindex(PM10) if PM10 is not None else np.nan,
        get_NOx_subindex(NO2) if NO2 is not None else np.nan,
        get_SO2_subindex(SO2) if SO2 is not None else np.nan,
        get_CO_subindex(CO) if CO is not None else np.nan,
        get_O3_subindex(O3) if O3 is not None else np.nan,
    ]

    # Count valid subindices
    valid_count = np.sum(~np.isnan(subindices))

    # AQI calculation (rule: need at least 3 valid pollutants)
    if valid_count < 3:
        return {"AQI": None, "Category": "Insufficient Data"}

    AQI_value = round(np.nanmax(subindices))
    AQI_category = get_AQI_bucket(AQI_value)

    return {"AQI": AQI_value, "Category": AQI_category}

# ---------- Example ----------
# if __name__ == "__main__":
    # Simulated API response
    # api_response = {"PM2_5": 49.35, "PM10": 81.01, "NO2": 75.615, "SO2": 80.18, "CO": 2.74, "Ozone": 9.33}

    # result = calculate_current_aqi(api_response)
    # print("Current AQI:", result["AQI"])
    # print("Category:", result["Category"])
