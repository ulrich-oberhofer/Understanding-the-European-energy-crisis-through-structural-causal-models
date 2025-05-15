import networkx as nx

"""
This script defines several causal graph models using NetworkX directed graphs (DiGraph).
Each model represents a specific causal structure with nodes and edges, where:
- Nodes represent variables in the causal model.
- Edges represent causal relationships between variables.
The models are saved as dictionaries containing:
    - `name`: The name of the graph.
    - `nodes`: A list of nodes (variables) in the graph.
    - `edges`: A list of directed edges (causal relationships) in the graph.
    - `graph`: A NetworkX DiGraph object representing the causal graph.
Models:
1. `GRAPH18`: 
    - Target: `price_da`.
    - Excludes: `oil_price`, `rl_CH`, `rl_GB`.
    - Used in the final analysis.
2. `GRAPH22`: 
    - Target: `agg_net_export`.
    - Excludes: `oil_price`, `rl_CH`, `rl_GB`.
    - Used in the final analysis.
3. `GRAPH24`: 
    - Target: `price_da_DE_LU<FR`.
    - Excludes: `oil_price`, `rl_CH`, `rl_GB`.
4. `GRAPH23`: 
    - Target: `price_da_diff_IT_NORD_FR`.
    - Excludes: `oil_price`, `rl_CH`, `rl_GB`.
5. `GRAPH19`: 
    - Target: `price_da`.
    - Excludes: `oil_price`, `rl_CH`, `rl_GB`, `rl_FR_ramp`.
6. `GRAPH20`: 
    - Target: `total_export`.
    - Excludes: `oil_price`, `rl_CH`, `rl_GB`.
7. `GRAPH21`: 
    - Target: `FR->IT_NORD`.
    - Excludes: `oil_price`, `rl_CH`, `rl_GB`.
Note:
- Models `GRAPH18` and `GRAPH22` are the only ones used in the final analysis.
- The script uses NetworkX to create and manipulate directed graphs.
"""

# causal graphs saved as dictionaries
# model 18 and 22 are the only ones used in the final analysis
# model 18 is for price_da as target, model 22 is for agg_net_export as target


# model 18: price_da as target. no oil_price, rl_CH, rl_GB
nodes = [
    "price_da",
    "carbon_price",
    "gas_price",
    "na",
    "run_off_gen",
    "solar_da",
    "load_da",
    "wind_da",
    "rl_FR_ramp",
    "rl_BE",
    "rl_DE_LU",
    "rl_ES",
    "rl_IT_NORD",
    "river_flow_mean",
    "temp_mean",
    "river_temp",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
    "isworkingday",
]

confounders = [
    "isworkingday",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
prices = [
    "carbon_price",
    "gas_price",
]
river = [
    "river_temp",
    "river_flow_mean",
]
renew = ["solar_da", "wind_da"]
load = ["load_da", "rl_FR_ramp", "rl_BE", "rl_DE_LU", "rl_ES", "rl_IT_NORD"]
na_hydro = ["na", "run_off_gen"]

confounders_prices = [
    (a, "gas_price") for a in ["isworkingday", "day_of_year_sin", "day_of_year_cos"]
]
confounders_mid_layer = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in renew
] + [(a, b) for a in confounders for b in load + na_hydro]
confounders_temp = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in ["temp_mean"] + river
] + [("temp_mean", b) for b in river]
temp_mid_layer = [("temp_mean", b) for b in load + renew] + [
    (a, b) for a in river for b in na_hydro
]
mid_layer_price_da = [(a, b) for a in load + renew + na_hydro for b in ["price_da"]]
prices_price_da = [(a, b) for a in prices for b in ["price_da"]]
edges = (
    confounders_prices
    + confounders_temp
    + confounders_mid_layer
    + temp_mid_layer
    + mid_layer_price_da
    + prices_price_da
)
# remove edges
edges = [
    e
    for e in edges
    if e not in [("isworkingday", "gas_price"), ("temp_mean", "rl_FR_ramp")]
]

GRAPH18 = {
    "name": "graph18",
    "nodes": nodes,
    "edges": edges,
    "graph": nx.DiGraph(edges),
}


# model 22: agg_net_export as target.
nodes = [
    "agg_net_export",
    "carbon_price",
    "gas_price",
    "na",
    "run_off_gen",
    "solar_da",
    "load_da",
    "wind_da",
    "rl_FR_ramp",
    "rl_BE",
    "rl_DE_LU",
    "rl_ES",
    "rl_IT_NORD",
    "river_flow_mean",
    "temp_mean",
    "river_temp",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
    "isworkingday",
]

confounders = [
    "isworkingday",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
prices = [
    "carbon_price",
    "gas_price",
]
river = [
    "river_temp",
    "river_flow_mean",
]
renew = ["solar_da", "wind_da"]
load = ["load_da", "rl_FR_ramp", "rl_BE", "rl_DE_LU", "rl_ES", "rl_IT_NORD"]
na_hydro = ["na", "run_off_gen"]

confounders_prices = [
    (a, "gas_price") for a in ["isworkingday", "day_of_year_sin", "day_of_year_cos"]
]
confounders_mid_layer = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in renew
] + [(a, b) for a in confounders for b in load + na_hydro]
confounders_temp = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in ["temp_mean"] + river
] + [("temp_mean", b) for b in river]
temp_mid_layer = [("temp_mean", b) for b in load + renew] + [
    (a, b) for a in river for b in na_hydro
]
mid_layer_price_da = [
    (a, b) for a in load + renew + na_hydro for b in ["agg_net_export"]
]
prices_price_da = [(a, b) for a in prices for b in ["agg_net_export"]]
edges = (
    confounders_prices
    + confounders_temp
    + confounders_mid_layer
    + temp_mid_layer
    + mid_layer_price_da
    + prices_price_da
)
# remove edges
edges = [
    e
    for e in edges
    if e not in [("isworkingday", "gas_price"), ("temp_mean", "rl_FR_ramp")]
]

GRAPH22 = {
    "name": "graph22",
    "nodes": nodes,
    "edges": edges,
    "graph": nx.DiGraph(edges),
}
### below only old, not used causal graphs ###

# model 24: with price_da_DE_LU<FR as target. no oil_price, rl_CH, rl_GB
nodes = [
    "price_da_DE_LU<FR",
    "carbon_price",
    "gas_price",
    "na",
    "run_off_gen",
    "solar_da",
    "load_da",
    "wind_da",
    "rl_FR_ramp",
    "rl_BE",
    "rl_DE_LU",
    "rl_ES",
    "rl_IT_NORD",
    "river_flow_mean",
    "temp_mean",
    "river_temp",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
    "isworkingday",
]

confounders = [
    "isworkingday",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
prices = [
    "carbon_price",
    "gas_price",
]
river = [
    "river_temp",
    "river_flow_mean",
]
renew = ["solar_da", "wind_da"]
load = ["load_da", "rl_FR_ramp", "rl_BE", "rl_DE_LU", "rl_ES", "rl_IT_NORD"]
na_hydro = ["na", "run_off_gen"]

confounders_prices = [
    (a, "gas_price") for a in ["isworkingday", "day_of_year_sin", "day_of_year_cos"]
]
confounders_mid_layer = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in renew
] + [(a, b) for a in confounders for b in load + na_hydro]
confounders_temp = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in ["temp_mean"] + river
] + [("temp_mean", b) for b in river]
temp_mid_layer = [("temp_mean", b) for b in load + renew] + [
    (a, b) for a in river for b in na_hydro
]
mid_layer_price_da = [
    (a, b) for a in load + renew + na_hydro for b in ["price_da_DE_LU<FR"]
]
prices_price_da = [(a, b) for a in prices for b in ["price_da_DE_LU<FR"]]
edges = (
    confounders_prices
    + confounders_temp
    + confounders_mid_layer
    + temp_mid_layer
    + mid_layer_price_da
    + prices_price_da
)
# remove edges
edges = [
    e
    for e in edges
    if e not in [("isworkingday", "gas_price"), ("temp_mean", "rl_FR_ramp")]
]

GRAPH24 = {
    "name": "graph24",
    "nodes": nodes,
    "edges": edges,
    "graph": nx.DiGraph(edges),
}


# model 23: price_da_diff_IT_NORD_FR as target. no oil_price, rl_CH, rl_GB
nodes = [
    "price_da_diff_IT_NORD_FR",
    "carbon_price",
    "gas_price",
    "na",
    "run_off_gen",
    "solar_da",
    "load_da",
    "wind_da",
    "rl_FR_ramp",
    "rl_BE",
    "rl_DE_LU",
    "rl_ES",
    "rl_IT_NORD",
    "river_flow_mean",
    "temp_mean",
    "river_temp",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
    "isworkingday",
]

confounders = [
    "isworkingday",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
prices = [
    "carbon_price",
    "gas_price",
]
river = [
    "river_temp",
    "river_flow_mean",
]
renew = ["solar_da", "wind_da"]
load = ["load_da", "rl_FR_ramp", "rl_BE", "rl_DE_LU", "rl_ES", "rl_IT_NORD"]
na_hydro = ["na", "run_off_gen"]

confounders_prices = [
    (a, "gas_price") for a in ["isworkingday", "day_of_year_sin", "day_of_year_cos"]
]
confounders_mid_layer = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in renew
] + [(a, b) for a in confounders for b in load + na_hydro]
confounders_temp = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in ["temp_mean"] + river
] + [("temp_mean", b) for b in river]
temp_mid_layer = [("temp_mean", b) for b in load + renew] + [
    (a, b) for a in river for b in na_hydro
]
mid_layer_price_da = [
    (a, b) for a in load + renew + na_hydro for b in ["price_da_diff_IT_NORD_FR"]
]
prices_price_da = [(a, b) for a in prices for b in ["price_da_diff_IT_NORD_FR"]]
edges = (
    confounders_prices
    + confounders_temp
    + confounders_mid_layer
    + temp_mid_layer
    + mid_layer_price_da
    + prices_price_da
)
# remove edges
edges = [
    e
    for e in edges
    if e not in [("isworkingday", "gas_price"), ("temp_mean", "rl_FR_ramp")]
]

GRAPH23 = {
    "name": "graph23",
    "nodes": nodes,
    "edges": edges,
    "graph": nx.DiGraph(edges),
}


# model 19: without oil, RL_CH, RL_GB, rl_FR_ramp
nodes = [
    "price_da",
    "carbon_price",
    "gas_price",
    "na",
    "solar_da",
    "load_da",
    "wind_da",
    "rl_BE",
    "rl_DE_LU",
    "rl_ES",
    "rl_IT_NORD",
    "river_flow_mean",
    "temp_mean",
    "river_temp",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
    "isworkingday",
]

confounders = [
    "isworkingday",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
prices = [
    "carbon_price",
    "gas_price",
]
river = [
    "river_temp",
    "river_flow_mean",
]
renew = ["solar_da", "wind_da"]
load = ["load_da", "rl_BE", "rl_DE_LU", "rl_ES", "rl_IT_NORD"]

confounders_prices = [
    (a, "gas_price") for a in ["isworkingday", "day_of_year_sin", "day_of_year_cos"]
]
confounders_mid_layer = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in renew
] + [(a, b) for a in confounders for b in load + ["na"]]
confounders_temp = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in ["temp_mean"] + river
] + [("temp_mean", b) for b in river]
temp_mid_layer = [("temp_mean", b) for b in load + renew] + [(a, "na") for a in river]
mid_layer_price_da = [(a, b) for a in load + renew + ["na"] for b in ["price_da"]]
prices_price_da = [(a, b) for a in prices for b in ["price_da"]]
edges = (
    confounders_prices
    + confounders_temp
    + confounders_mid_layer
    + temp_mid_layer
    + mid_layer_price_da
    + prices_price_da
)
# remove edges
edges = [e for e in edges if e not in [("isworkingday", "gas_price")]]

GRAPH19 = {
    "name": "graph19",
    "nodes": nodes,
    "edges": edges,
    "graph": nx.DiGraph(edges),
}

# model 20: same as model18 but with total export of france instead of price_da as target
nodes = [
    "total_export",
    "carbon_price",
    "gas_price",
    "na",
    "solar_da",
    "load_da",
    "wind_da",
    "rl_FR_ramp",
    "rl_BE",
    "rl_DE_LU",
    "rl_ES",
    "rl_IT_NORD",
    "river_flow_mean",
    "temp_mean",
    "river_temp",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
    "isworkingday",
]

confounders = [
    "isworkingday",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
prices = [
    "carbon_price",
    "gas_price",
]
river = [
    "river_temp",
    "river_flow_mean",
]
renew = ["solar_da", "wind_da"]
load = ["load_da", "rl_FR_ramp", "rl_BE", "rl_DE_LU", "rl_ES", "rl_IT_NORD"]

confounders_prices = [
    (a, "gas_price") for a in ["isworkingday", "day_of_year_sin", "day_of_year_cos"]
]
confounders_mid_layer = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in renew
] + [(a, b) for a in confounders for b in load + ["na"]]
confounders_temp = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in ["temp_mean"] + river
] + [("temp_mean", b) for b in river]
temp_mid_layer = [("temp_mean", b) for b in load + renew] + [(a, "na") for a in river]
mid_layer_price_da = [(a, b) for a in load + renew + ["na"] for b in ["total_export"]]
prices_price_da = [(a, b) for a in prices for b in ["total_export"]]
edges = (
    confounders_prices
    + confounders_temp
    + confounders_mid_layer
    + temp_mid_layer
    + mid_layer_price_da
    + prices_price_da
)
# remove edges
edges = [
    e
    for e in edges
    if e not in [("isworkingday", "gas_price"), ("temp_mean", "rl_FR_ramp")]
]

GRAPH20 = {
    "name": "graph20",
    "nodes": nodes,
    "edges": edges,
    "graph": nx.DiGraph(edges),
}

# model 21: same as model18 but with export italy instead of price_da as target
nodes = [
    "FR->IT_NORD",
    "carbon_price",
    "gas_price",
    "na",
    "solar_da",
    "load_da",
    "wind_da",
    "rl_FR_ramp",
    "rl_BE",
    "rl_DE_LU",
    "rl_ES",
    "rl_IT_NORD",
    "river_flow_mean",
    "temp_mean",
    "river_temp",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
    "isworkingday",
]

confounders = [
    "isworkingday",
    "hour_sin",
    "hour_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
prices = [
    "carbon_price",
    "gas_price",
]
river = [
    "river_temp",
    "river_flow_mean",
]
renew = ["solar_da", "wind_da"]
load = ["load_da", "rl_FR_ramp", "rl_BE", "rl_DE_LU", "rl_ES", "rl_IT_NORD"]

confounders_prices = [
    (a, "gas_price") for a in ["isworkingday", "day_of_year_sin", "day_of_year_cos"]
]
confounders_mid_layer = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in renew
] + [(a, b) for a in confounders for b in load + ["na"]]
confounders_temp = [
    (a, b)
    for a in ["day_of_year_sin", "day_of_year_cos", "hour_sin", "hour_cos"]
    for b in ["temp_mean"] + river
] + [("temp_mean", b) for b in river]
temp_mid_layer = [("temp_mean", b) for b in load + renew] + [(a, "na") for a in river]
mid_layer_price_da = [(a, b) for a in load + renew + ["na"] for b in ["FR->IT_NORD"]]
prices_price_da = [(a, b) for a in prices for b in ["FR->IT_NORD"]]
edges = (
    confounders_prices
    + confounders_temp
    + confounders_mid_layer
    + temp_mid_layer
    + mid_layer_price_da
    + prices_price_da
)
# remove edges
edges = [
    e
    for e in edges
    if e not in [("isworkingday", "gas_price"), ("temp_mean", "rl_FR_ramp")]
]

GRAPH21 = {
    "name": "graph21",
    "nodes": nodes,
    "edges": edges,
    "graph": nx.DiGraph(edges),
}
