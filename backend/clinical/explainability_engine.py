class ExplainabilityEngine:

    def generate(self, risk_analysis):

        clinical = []
        drug_specific = []
        interactions_list = []

        lab = risk_analysis.get("lab_analysis", {})

        # -----------------------------
        # Clinical Factors
        # -----------------------------
        egfr = lab.get("egfr")
        if egfr and egfr < 60:
            clinical.append(
                f"Reduced kidney function (eGFR {egfr}) may cause drug accumulation"
            )

        alt = lab.get("alt")
        if alt and alt > 60:
            clinical.append(
                f"Elevated liver enzymes (ALT {alt}) increase hepatotoxicity risk"
            )

        # -----------------------------
        # Drug-specific reasons
        # -----------------------------
        for t in risk_analysis.get("toxicity_results", []):

            drug = t["drug"]

            for r in t.get("comorbidity_reasons", []):
                drug_specific.append(f"{drug}: {r}")

            for r in t.get("lifestyle_reasons", []):
                drug_specific.append(f"{drug}: {r}")

            for r in t.get("liver_reasons", []):
                drug_specific.append(f"{drug}: {r}")

        # -----------------------------
        # Interactions
        # -----------------------------
        for i in risk_analysis.get("interactions", []):
            interactions_list.append(
                f"{i['drug_pair']} → {i['interaction_type']}"
            )

        # -----------------------------
        # Build structured output
        # -----------------------------
        output = []

        if clinical:
            output.append("🧠 Clinical Factors:")
            output.extend([f"- {c}" for c in clinical])
            output.append("")

        if drug_specific:
            output.append("💊 Drug-Specific Risks:")
            output.extend([f"- {d}" for d in drug_specific])
            output.append("")

        if interactions_list:
            output.append("⚠️ Interactions:")
            output.extend([f"- {i}" for i in interactions_list])

        if not output:
            return ["No major risk factors detected"]

        return output