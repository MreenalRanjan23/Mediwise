class PatientProfile:

    def __init__(
        self,
        age,
        sex=None,
        weight=None,
        height=None,

        # Core conditions
        liver_disease=False,
        kidney_disease=False,

        # Biological state
        pregnant=False,
        lactating=False,

        # Clinical context
        allergies=None,
        conditions=None,

        # Lifestyle
        smoker=False,
        alcohol_use=False,
        occupation=None,

        # Labs (for future phases)
        creatinine=None,
        alt=None,
        ast=None,
        inr=None,

        # Genetics (future)
        cyp2d6=None
    ):
        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height

        self.liver_disease = liver_disease
        self.kidney_disease = kidney_disease

        self.pregnant = pregnant
        self.lactating = lactating

        self.allergies = allergies or []
        self.conditions = conditions or []

        self.smoker = smoker
        self.alcohol_use = alcohol_use
        self.occupation = occupation

        self.creatinine = creatinine
        self.alt = alt
        self.ast = ast
        self.inr = inr

        self.cyp2d6 = cyp2d6

    # -----------------------------
    # Risk multiplier (UPDATED)
    # -----------------------------
    def get_risk_multiplier(self):

        multiplier = 1.0

        # Age
        if self.age > 65:
            multiplier *= 1.2

        # Organ conditions
        if self.liver_disease:
            multiplier *= 1.3

        if self.kidney_disease:
            multiplier *= 1.3

        # Lifestyle
        if self.smoker:
            multiplier *= 1.05

        if self.alcohol_use:
            multiplier *= 1.1

        # Low weight risk
        if self.weight and self.weight < 50:
            multiplier *= 1.1

        return multiplier

    # -----------------------------
    # Summary (for API/UI)
    # -----------------------------
    def summary(self):
        return {
            "age": self.age,
            "sex": self.sex,
            "weight": self.weight,
            "liver_disease": self.liver_disease,
            "kidney_disease": self.kidney_disease,
            "pregnant": self.pregnant,
            "allergies": self.allergies,
            "conditions": self.conditions,
            "smoker": self.smoker,
            "alcohol_use": self.alcohol_use
        }