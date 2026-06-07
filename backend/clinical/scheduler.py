import pandas as pd


class MedicationScheduler:

    def __init__(self, metadata_path, interaction_path):

        self.drug_data = pd.read_csv(metadata_path)
        self.interactions = pd.read_csv(interaction_path)

        self.drug_data["drug_name"] = self.drug_data["drug_name"].str.lower()

        # Default daily schedule
        self.wake_time = 7
        self.sleep_time = 23

        # Meal times
        self.meals = {
            "breakfast": 9,
            "lunch": 13,
            "dinner": 19
        }

    # Convert 24h time → AM/PM
    def format_time(self, hour):

        if hour == 0:
            return "12 AM"

        if hour == 12:
            return "12 PM"

        if hour > 12:
            return f"{hour-12} PM"

        return f"{hour} AM"

    # Fetch drug information
    def get_drug_info(self, drug_name):

        drug_name = drug_name.lower()

        drug = self.drug_data[self.drug_data["drug_name"] == drug_name]

        if drug.empty:
            raise ValueError(f"{drug_name} not found")

        return drug.iloc[0]

    # Generate medication schedule
    def generate_schedule(self, drugs):

        schedule = []
        current_time = self.wake_time + 1

        for drug in drugs:

            drug_info = self.get_drug_info(drug)

            if drug_info["empty_stomach_required"] == 1:

                time = self.meals["breakfast"] - 1
                instruction = "Take on empty stomach before breakfast"

            elif drug_info["requires_food"] == 1:

                time = self.meals["breakfast"]
                instruction = "Take with breakfast"

            else:

                time = current_time
                instruction = "Take normally"
                current_time += 2

            schedule.append({
                "drug": drug,
                "time": time,
                "formatted_time": self.format_time(time),
                "instruction": instruction
            })

        schedule = self.apply_spacing_rules(schedule)

        return schedule

    # Apply interaction spacing rules
    def apply_spacing_rules(self, schedule):

        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):

                drug_a = schedule[i]["drug"]
                drug_b = schedule[j]["drug"]

                interaction = self.interactions[
                    (self.interactions["drug_a"].str.lower() == drug_a.lower()) &
                    (self.interactions["drug_b"].str.lower() == drug_b.lower())
                ]

                if not interaction.empty:

                    spacing = int(interaction.iloc[0]["recommended_spacing_hours"])

                    if spacing > 0:

                        if abs(schedule[i]["time"] - schedule[j]["time"]) < spacing:

                            schedule[j]["time"] = schedule[i]["time"] + spacing
                            schedule[j]["formatted_time"] = self.format_time(schedule[j]["time"])

                            schedule[j]["instruction"] += (
                                f" (Adjusted for {spacing}h spacing from {drug_a})"
                            )

        return schedule

    # Create full daily report
    def generate_daily_report(self, drugs):

        schedule = self.generate_schedule(drugs)

        report = []
        report.append("\n===============================")
        report.append("        MEDICATION SCHEDULE")
        report.append("===============================\n")

        report.append(f"Wake Time : {self.format_time(self.wake_time)}")
        report.append(f"Sleep Time: {self.format_time(self.sleep_time)}\n")

        report.append("Meals")
        report.append("-----")
        report.append(f"Breakfast : {self.format_time(self.meals['breakfast'])}")
        report.append(f"Lunch     : {self.format_time(self.meals['lunch'])}")
        report.append(f"Dinner    : {self.format_time(self.meals['dinner'])}\n")

        report.append("Medication Timeline")
        report.append("-------------------")

        for item in schedule:

            report.append(
                f"{item['formatted_time']} - {item['drug']}"
            )

            report.append(
                f"    {item['instruction']}"
            )

        return "\n".join(report)