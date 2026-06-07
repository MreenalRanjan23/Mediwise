import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv


class DrugInteractionGNN(nn.Module):

    def __init__(self, num_nodes):

        super().__init__()

        self.conv1 = GCNConv(num_nodes, 16)
        self.conv2 = GCNConv(16, 8)

    def get_embeddings(self, x, edge_index):

        x = self.conv1(x, edge_index)
        x = torch.relu(x)

        x = self.conv2(x, edge_index)
        x = torch.relu(x)

        return x

    def forward(self, x, edge_index):

        return self.get_embeddings(x, edge_index)