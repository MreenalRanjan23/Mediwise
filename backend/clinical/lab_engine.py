# -----------------------------
# Kidney Intelligence
# -----------------------------
def calculate_egfr(creatinine, age, sex):
    """
    Simplified MDRD formula
    """

    if creatinine is None or age is None or sex is None:
        return None

    try:
        creatinine = float(creatinine)
    except:
        return None

    # Sex factor
    sex_factor = 0.742 if str(sex).lower() == "female" else 1.0

    egfr = 175 * (creatinine ** -1.154) * (age ** -0.203) * sex_factor

    return round(egfr, 2)


def kidney_risk_multiplier(egfr):

    if egfr is None:
        return 1.0

    if egfr >= 90:
        return 1.0
    elif egfr >= 60:
        return 1.1
    elif egfr >= 30:
        return 1.3
    elif egfr >= 15:
        return 1.6
    else:
        return 2.0


# -----------------------------
# Liver Intelligence (NEW 🔥)
# -----------------------------
def liver_risk_multiplier(alt, ast):
    """
    Estimate liver stress based on ALT/AST levels
    """

    # No data → no penalty
    if alt is None and ast is None:
        return 1.0

    values = []

    try:
        if alt is not None:
            values.append(float(alt))
        if ast is not None:
            values.append(float(ast))
    except:
        return 1.0

    if not values:
        return 1.0

    avg = sum(values) / len(values)

    # Threshold-based multiplier
    if avg < 40:
        return 1.0
    elif avg < 80:
        return 1.1
    elif avg < 150:
        return 1.3
    else:
        return 1.6


# -----------------------------
# Optional Helper (for future XAI)
# -----------------------------
def liver_risk_level(alt, ast):
    """
    Human-readable interpretation (for explainability later)
    """

    if alt is None and ast is None:
        return "unknown"

    values = [v for v in [alt, ast] if v is not None]

    if not values:
        return "unknown"

    avg = sum(values) / len(values)

    if avg < 40:
        return "normal"
    elif avg < 80:
        return "mild elevation"
    elif avg < 150:
        return "moderate elevation"
    else:
        return "severe elevation"