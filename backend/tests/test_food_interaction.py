import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clinical.food_interaction_engine import FoodInteractionEngine


engine = FoodInteractionEngine(
    "data/raw/food_interactions.csv"
)

drugs = ["Ciprofloxacin", "Warfarin", "Paracetamol"]

results = engine.check_food_interactions(drugs)

print(results)