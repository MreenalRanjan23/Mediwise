import pandas as pd
import networkx as nx


class DrugGraphBuilder:

    def __init__(self, interaction_path):

        self.df = pd.read_csv(interaction_path)

    def build_graph(self):

        G = nx.Graph()

        for _, row in self.df.iterrows():

            drug_a = row["drug_a"].lower()
            drug_b = row["drug_b"].lower()

            G.add_edge(drug_a, drug_b)

        return G