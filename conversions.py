# Fatores de conversão de distância
DISTANCE_FACTORS = {"km": 1.0, "mi": 1.60934}  # 1 mi = 1.60934 km

# Consumos convertidos para L/100km
def to_l_per_100km(value, metric):
    if metric == "L/100km":
        return value
    elif metric == "km/L":
        return 100 / value if value != 0 else 0
    elif metric == "mpg":  # mpg (US)
        return 235.215 / value if value != 0 else 0
    else:
        return value
