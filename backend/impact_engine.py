def estimate_effect(data, prob):

    watch_hours = data.get("watch_hours", 0)
    last_login = data.get("last_login_days", 0)

    if watch_hours < 5:
        reduction = 0.35
    elif last_login > 10:
        reduction = 0.25
    else:
        reduction = 0.15

    new_prob = prob * (1 - reduction)

    return {
        "new_probability": round(new_prob, 3),
        "improvement": reduction
    }