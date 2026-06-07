from interaction_engine import InteractionEngine

engine = InteractionEngine("../data/raw/drug_interactions.csv")

drug_list = ["Warfarin", "Ibuprofen", "Paracetamol"]

interactions = engine.check_all_interactions(drug_list)

for interaction in interactions:
    print(interaction)