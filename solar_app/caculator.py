# --- AQI Calculation using CPCB (India) breakpoints ---

# Breakpoints for each pollutant (Cp in µg/m³, CO in mg/m³)
bp_pm25 = [(0,30,0,50),(31,60,51,100),(61,90,101,200),(91,120,201,300),(121,250,301,400),(251,350,401,500)]
bp_pm10 = [(0,50,0,50),(51,100,51,100),(101,250,101,200),(251,350,201,300),(351,430,301,400),(431,1000,401,500)]
bp_no2  = [(0,40,0,50),(41,80,51,100),(81,180,101,200),(181,280,201,300),(281,400,301,400),(401,1000,401,500)]
bp_so2  = [(0,40,0,50),(41,80,51,100),(81,380,101,200),(381,800,201,300),(801,1600,301,400),(1601,2100,401,500)]
bp_co   = [(0,1,0,50),(1.1,2,51,100),(2.1,10,101,200),(10.1,17,201,300),(17.1,34,301,400),(34.1,50,401,500)]
bp_ozone= [(0,50,0,50),(51,100,51,100),(101,168,101,200),(169,208,201,300),(209,748,301,400),(749,1000,401,500)]

def sub_index(Cp, breakpoints):
    """
    Calculate sub-index for pollutant Cp using breakpoint table.
    Cp = concentration, breakpoints = [(BP_LO, BP_HI, I_LO, I_HI), ...]
    """
    for (lo, hi, ilo, ihi) in breakpoints:
        if lo <= Cp <= hi:
            if hi == lo:  # avoid divide by zero
                return ilo
            return ((ihi - ilo) / (hi - lo)) * (Cp - lo) + ilo
    # If below lowest range → lowest AQI
    if Cp < breakpoints[0][0]:
        return breakpoints[0][2]
    # If above highest → cap at highest AQI
    return breakpoints[-1][3]

def calculate_aqi(pm25, pm10, no2, so2, co, ozone):
    """
    Compute overall AQI = max(sub-indices of pollutants)
    """
    indices = {
        "PM2.5": sub_index(pm25, bp_pm25),
        "PM10":  sub_index(pm10, bp_pm10),
        "NO2":   sub_index(no2,  bp_no2),
        "SO2":   sub_index(so2,  bp_so2),
        "CO":    sub_index(co,   bp_co),
        "Ozone": sub_index(ozone,bp_ozone)
    }
    # Overall AQI is maximum of all sub-indices
    return max(indices.values()), indices

# --- Example usage ---
rows = [
    (35.15,113.09,34.65,116.41,1.48,3.11),
    (65.44,149.8,34.64,8.59,0.87,11.24),
    (120.79,180.36,46.86,79.53,0.8,11.97),
    (80.34,117.08,37.29,5.05,0.96,9.5)
]

for row in rows:
    aqi, subs = calculate_aqi(*row)
    print(f"Data={row} → AQI={round(aqi,2)} | Sub-Indices={subs}")
