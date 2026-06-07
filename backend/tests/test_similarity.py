from clinical.similarity_engine import SimilarityEngine

engine = SimilarityEngine("data/raw/drug_metadata.csv")

print("\nSimilarity between drugs:\n")

print("Ibuprofen vs Paracetamol:",
      engine.similarity("ibuprofen", "paracetamol"))

print("\nTop similar to Ibuprofen:\n")

print(engine.get_similar_drugs("ibuprofen"))