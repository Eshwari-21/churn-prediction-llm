def get_risk(prob):
    if prob > 0.8:
        return "High"
    elif prob > 0.5:
        return "Medium"
    return "Low"