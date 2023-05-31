import pickle
from pathlib import Path

import bw2data
import networkx as nx
from bw2data.backends import ActivityDataset, ExchangeDataset
from tqdm import tqdm
from playhouse.shortcuts import model_to_dict

# Create an empty graph
G = nx.DiGraph()

bw2data.projects.set_current("ecoi_dbs")
activities = ActivityDataset.select()

# g_node_data = []
for act in tqdm(activities):
    # data = model_to_dict(act)
    # data["location_name"] = geo_code2_name.get(act.location, "")
    # G.add_nodes_from([(act.code, data)]
    # g_node_data.append((act.code, {"name": act.name}))
    G.add_node(act.code)
# G.add_nodes_from(g_node_data)

for exc in tqdm(ExchangeDataset.select()):
    # print(exc)
    # G.add_edges_from((exc.input_code, exc.output_code, {"weight": exc.data["amount"]}))
    G.add_edge(exc.input_code, exc.output_code)

# Add edges (links)
# edges_data = [
#     ('Node1', 'Node2', {'weight': 3.1415}),
#     # add more edges here
# ]
# G.add_edges_from(edges_data)


def serialize(graph: nx.Graph, path: Path):
    # Save to a pickle file
    pickle.dump(graph, path.open("wb"))


def deserialize(path: Path) -> nx.Graph:
    return pickle.load(path.open("rb"))