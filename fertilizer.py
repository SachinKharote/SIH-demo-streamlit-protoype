# fertilizer.py

# Ideal nutrient levels for crops (example values)
ideal_nutrients = {
    "Wheat": {"N": 100, "P": 50, "K": 50},
    "Maize": {"N": 120, "P": 60, "K": 60},
    "Banana": {"N": 120, "P": 60, "K": 60},
    "Groundnut": {"N": 50, "P": 40, "K": 40},
    "Cowpea": {"N": 40, "P": 30, "K": 30}
}

# Fertilizer mapping for nutrient deficiencies
fertilizer_map = {
    "N": "Urea",
    "P": "DAP",
    "K": "MOP"
}

# Sowing & harvesting seasons
crop_seasons = {
    "Wheat": {"sowing": "Oct-Dec", "harvesting": "Mar-Apr"},
    "Maize": {"sowing": "Jun-Jul", "harvesting": "Sep-Oct"},
    "Banana": {"sowing": "Feb-Mar", "harvesting": "Nov-Dec"},
    "Groundnut": {"sowing": "Jun-Jul", "harvesting": "Oct-Nov"},
    "Cowpea": {"sowing": "Jun-Jul", "harvesting": "Sep-Oct"}
}

def recommend_fertilizers(crop, user_n, user_p, user_k):
    """Returns list of recommended fertilizers based on nutrient deficiency"""
    fertilizers = []
    ideal = ideal_nutrients.get(crop)
    if ideal:
        if user_n < ideal["N"]:
            fertilizers.append(fertilizer_map["N"])
        if user_p < ideal["P"]:
            fertilizers.append(fertilizer_map["P"])
        if user_k < ideal["K"]:
            fertilizers.append(fertilizer_map["K"])
    return fertilizers

def get_crop_season(crop):
    """Returns sowing and harvesting season for a crop"""
    return crop_seasons.get(crop, {"sowing": "Unknown", "harvesting": "Unknown"})
