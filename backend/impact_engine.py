def calculate_impact(prob, strategies):
    improvement = 0.05 * len(strategies)

    new_prob = max(prob - improvement, 0)

    impact = f"Churn reduced by {round(improvement * 100, 2)}%"

    return new_prob, impact