def normalize_risk_score(raw_score):

    """
    Convert raw aggregated score
    into a user-friendly 0–100 scale.
    """

    # =====================================
    # Clamp very high scores
    # =====================================

    capped = min(raw_score, 300)

    # =====================================
    # Normalize to percentage
    # =====================================

    normalized = int((capped / 300) * 100)

    # =====================================
    # Risk category
    # =====================================

    if normalized < 20:
        level = "Minimal"

    elif normalized < 40:
        level = "Low"

    elif normalized < 60:
        level = "Moderate"

    elif normalized < 80:
        level = "High"

    else:
        level = "Critical"

    # =====================================
    # UI color mapping
    # =====================================

    color_map = {
        "Minimal": "#22c55e",
        "Low": "#84cc16",
        "Moderate": "#facc15",
        "High": "#f97316",
        "Critical": "#ef4444",
    }

    return {
        "raw_score": round(raw_score, 2),
        "normalized_score": normalized,
        "risk_level": level,
        "color": color_map[level]
    }