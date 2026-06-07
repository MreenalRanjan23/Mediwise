from clinical.risk_aggregator import RiskAggregator
from clinical.patient_profile import PatientProfile
from clinical.risk_normalizer import normalize_risk_score

# =================================================
# INITIALIZE MASTER AGGREGATOR
# =================================================

aggregator = RiskAggregator(
    metadata_path="data/raw/drug_metadata.csv",
    interaction_path="data/raw/drug_interactions.csv"
)

# =================================================
# MASTER CLINICAL PIPELINE
# =================================================

def analyze_case(payload):

    """
    Unified clinical AI orchestration pipeline
    """

    # =================================================
    # BUILD PATIENT PROFILE
    # =================================================

    patient = PatientProfile(

        age=payload.get("age", 30),

        sex=payload.get("sex", "M"),

        liver_disease=payload.get(
            "liver_disease",
            False
        ),

        kidney_disease=payload.get(
            "kidney_disease",
            False
        ),

        smoker=payload.get(
            "smoker",
            False
        ),

        alcohol_use=payload.get(
            "alcohol_use",
            False
        ),

        conditions=payload.get(
            "conditions",
            []
        ),

        creatinine=payload.get(
            "creatinine",
            1.0
        ),

        alt=payload.get(
            "alt",
            30
        ),

        ast=payload.get(
            "ast",
            30
        )
    )

    # =================================================
    # EMPTY MEDICATION SAFETY
    # =================================================

    drugs = payload.get("drugs", [])

    if len(drugs) == 0:

        return {

            "risk_analysis": {
                "score": 0,
                "normalized": {
                    "normalized_score": 0,
                    "risk_level": "Low Risk"
                },
                "interactions": []
            },

            "toxicity_results": [],

            "food_interactions": [],

            "alternatives": [],

            "lab_analysis": {
                "alt": patient.alt,
                "ast": patient.ast,
                "egfr": 90
            },

            "risk_breakdown": {},

            "explanations": [
                "No medications added."
            ],

            "insights": [
                "Add medications to begin AI analysis."
            ],

            "patient_profile": payload,

            "analytics": {

                "risk_distribution": {
                    "safe": 100,
                    "moderate": 0,
                    "high": 0
                },

                "organ_toxicity": {
                    "liver": 0,
                    "kidney": 0,
                    "cardiac": 0,
                    "cns": 0
                },

                "weekly_trend": [
                    {"day": "Mon", "risk": 0},
                    {"day": "Tue", "risk": 0},
                    {"day": "Wed", "risk": 0},
                    {"day": "Thu", "risk": 0},
                    {"day": "Fri", "risk": 0},
                    {"day": "Sat", "risk": 0},
                    {"day": "Sun", "risk": 0},
                ]
            }
        }

    # =================================================
    # RUN MASTER AGGREGATOR
    # =================================================

    results = aggregator.analyze_medication_plan(
        drugs,
        patient
    )

    # =================================================
    # EXTRACT IMPORTANT DATA
    # =================================================

    risk_score = results["final_risk_score"]

    interactions = results["interactions"]

    toxicity_results = results["toxicity_results"]

    lab_analysis = results["lab_analysis"]

    # =================================================
    # NORMALIZE RISK
    # =================================================

    normalized_risk = normalize_risk_score(
        risk_score
    )

    normalized_score = normalized_risk.get(
        "normalized_score",
        0
    )

    # =================================================
    # GENERATE AI INSIGHTS
    # =================================================

    insights = []

    if normalized_score < 25:

        insights.append(
            "Medication profile appears clinically safe."
        )

    elif normalized_score < 60:

        insights.append(
            "Moderate clinical monitoring recommended."
        )

    else:

        insights.append(
            "High cumulative medication risk detected."
        )

    if len(interactions) == 0:

        insights.append(
            "No severe drug interactions detected."
        )

    else:

        insights.append(
            f"{len(interactions)} interaction(s) detected."
        )

    # =================================================
    # ANALYTICS ENGINE
    # =================================================

    interaction_count = len(interactions)

    medication_count = len(drugs)

    # =================================================
    # DYNAMIC RISK DISTRIBUTION
    # =================================================

    safe_zone = max(
        5,
        100 - int(normalized_score)
    )

    moderate_zone = min(
        60,
        int(normalized_score * 0.55)
    )

    high_zone = min(
        100,
        int(normalized_score * 0.45)
    )

    # =================================================
    # ORGAN TOXICITY
    # =================================================

    alt_value = lab_analysis.get(
        "alt",
        30
    )

    ast_value = lab_analysis.get(
        "ast",
        30
    )

    egfr_value = lab_analysis.get(
        "egfr",
        90
    )

    liver_load = min(
        100,
        max(
            5,
            (
                (alt_value + ast_value) / 2
            ) * 0.9
            + medication_count * 8
        )
    )

    kidney_load = min(
        100,
        max(
            5,
            (120 - egfr_value)
            + medication_count * 6
        )
    )

    cardiac_load = min(
        100,
        max(
            5,
            interaction_count * 18
            + normalized_score * 0.35
        )
    )

    cns_load = min(
        100,
        max(
            5,
            medication_count * 12
            + normalized_score * 0.28
        )
    )

    # =================================================
    # WEEKLY TREND
    # =================================================

    weekly_trend = [

        {
            "day": "Mon",
            "risk": round(
                normalized_score * 0.55
            )
        },

        {
            "day": "Tue",
            "risk": round(
                normalized_score * 0.72
            )
        },

        {
            "day": "Wed",
            "risk": round(
                normalized_score * 0.84
            )
        },

        {
            "day": "Thu",
            "risk": round(
                normalized_score
            )
        },

        {
            "day": "Fri",
            "risk": round(
                normalized_score * 0.82
            )
        },

        {
            "day": "Sat",
            "risk": round(
                normalized_score * 0.68
            )
        },

        {
            "day": "Sun",
            "risk": round(
                normalized_score * 0.50
            )
        },
    ]

    # =================================================
    # ANALYTICS PAYLOAD
    # =================================================

    analytics = {

        "risk_distribution": {

            "safe": safe_zone,

            "moderate": moderate_zone,

            "high": high_zone,
        },

        "organ_toxicity": {

            "liver": round(
                liver_load
            ),

            "kidney": round(
                kidney_load
            ),

            "cardiac": round(
                cardiac_load
            ),

            "cns": round(
                cns_load
            ),
        },

        "weekly_trend": weekly_trend
    }

    # =================================================
    # FINAL RESPONSE
    # =================================================

    return {

        "risk_analysis": {

            "score": risk_score,

            "normalized": normalized_risk,

            "interactions": interactions,
        },

        "toxicity_results": toxicity_results,

        "food_interactions": results[
            "food_interactions"
        ],

        "alternatives": results[
            "alternatives"
        ],

        "lab_analysis": lab_analysis,

        "risk_breakdown": results[
            "risk_breakdown"
        ],

        "explanations": results[
            "explanations"
        ],

        "insights": insights,

        "patient_profile": results[
            "patient_profile"
        ],

        "analytics": analytics
    }


# =================================================
# LOCAL TESTING
# =================================================

if __name__ == "__main__":

    sample_payload = {

        "drugs": [
            "paracetamol",
            "ibuprofen"
        ],

        "age": 45,

        "sex": "M",

        "liver_disease": False,

        "kidney_disease": False,

        "smoker": True,

        "alcohol_use": True,

        "conditions": [
            "hypertension"
        ],

        "creatinine": 1.2,

        "alt": 70,

        "ast": 55
    }

    result = analyze_case(
        sample_payload
    )

    print(result)