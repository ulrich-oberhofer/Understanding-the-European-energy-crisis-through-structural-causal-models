import os
from dowhy import gcm
from dowhy.graph import is_root_node, get_ordered_predecessors
from dowhy.gcm.falsify import falsify_graph

from scripts.utils import save_file


def create_causal_model(graph, data):
    """
    This function initializes a Structural Causal Model (SCM) based on the provided
    causal graph and fits it to the given data. Root nodes in the graph are assigned
    empirical distributions, while non-root nodes are modeled using an additive noise
    model with a linear regressor.

    Parameters:
    graph (networkx.DiGraph):  A directed acyclic graph representing the causal structure.
    data (pandas.DataFrame): A DataFrame containing the normalized data to fit the model.

    Returns:
    gcm.StructuralCausalModel: The fitted Structural Causal Model.
    """
    causal_model = gcm.StructuralCausalModel(graph)

    for n in causal_model.graph.nodes:
        if is_root_node(causal_model.graph, n):
            causal_model.set_causal_mechanism(n, gcm.EmpiricalDistribution())
        else:
            causal_model.set_causal_mechanism(
                n, gcm.AdditiveNoiseModel(gcm.ml.create_linear_regressor())
            )
    print(gcm.fit(causal_model, data))
    return causal_model


def get_linear_coefficients(causal_model, data_original):
    """
    Get the structural coefficients of a linear Structural Causal Model (SCM).
    This function extracts the structural coefficients (including intercepts) from a fitted
    linear SCM and adjusts them to account for the original (non-normalized) data scale.

    Parameters:
    causal_model (gcm.StructuralCausalModel): The fitted causal model from which the structural coefficients are extracted.
    data_original (pandas.DataFrame): The original (non-normalized) dataset used to fit the causal model.

    Returns:
    dict: A dictionary where keys are the nodes of the causal graph, and values are dictionaries
        containing the structural coefficients for each parent node and the intercept.
        The coefficients are adjusted to match the scale of the original data.
    """
    coefficients = {}
    for node in causal_model.graph.nodes:
        if is_root_node(causal_model.graph, node):
            continue
        # coefficients
        coef_ = causal_model.causal_mechanism(node).prediction_model.sklearn_model.coef_
        ordered_parents = get_ordered_predecessors(causal_model.graph, node)
        intercept_ = causal_model.causal_mechanism(
            node
        ).prediction_model.sklearn_model.intercept_
        # denormalize intercept
        intercept_ = intercept_ * data_original[node].std() + data_original[node].mean()
        for i in range(len(ordered_parents)):
            # denormalize coefficients
            coef_[i] = (
                coef_[i]
                * data_original[node].std()
                / data_original[ordered_parents[i]].std()
            )
            intercept_ = (
                intercept_ - coef_[i] * data_original[ordered_parents[i]].mean()
            )
            labeled_coef = {
                ordered_parents[i]: coef_[i] for i in range(len(ordered_parents))
            }
        # intercept
        labeled_coef["intercept"] = intercept_
        # save in dict
        coefficients[node] = labeled_coef
    return coefficients


def create_eval_scm(
    graph_dict,
    df_data,
    df_data_original,
    with_coefficients=False,
    with_evaluation=False,
    with_falsification=False,
):
    """
    This function constructs a causal model based on the provided graph structure and data,
    and optionally performs structural coefficient calculation, model evaluation, and falsification tests.

    Parameters:
    graph_dict (dict): A dictionary containing the causal graph structure, including nodes, edges, and a name.
    df_data (pandas.DataFrame): The normalized data used to fit the causal model.
    df_data_original (pandas.DataFrame): The original (non-normalized) data used for coefficient calculations.
    with_coefficients (bool, optional): If True, calculates and saves the structural coefficients. Default is False.
    with_evaluation (bool, optional): If True, evaluates the causal model and saves the results. Default is False.
    with_falsification (bool, optional): If True, performs falsification tests on the causal model. Default is False.

    Returns:
    None
    """
    selected_graph = graph_dict
    nodes = selected_graph["nodes"]
    causal_graph = selected_graph["graph"]
    name = selected_graph["name"]

    df_data = df_data.loc[:, nodes].dropna()
    df_data_original = df_data_original.loc[:, nodes].dropna()
    years = f"{df_data.index[0].year}-{df_data.index[-1].year}"
    dir = f"../models/{name}/"
    try:
        os.mkdir(dir)
    except OSError as error:
        print(error)

    print("creating causal model")
    causal_model = create_causal_model(graph=causal_graph, data=df_data)
    # structural coefficients
    if with_coefficients:
        print("get coefficients")
        coefficients = get_linear_coefficients(
            causal_model=causal_model, data_original=df_data_original
        )
        dir_new = dir + "coefficients/"
        save_file(coefficients, dir=dir_new, filename=f"{name}_{years}_coefficients")

    # main overview evaluation.
    if with_evaluation:
        print("evaluate")
        evaluate_causal_model = gcm.evaluate_causal_model(causal_model, df_data)
        print(evaluate_causal_model)
        dir_new = dir + "evaluation/"
        save_file(
            evaluate_causal_model, dir=dir_new, filename=f"{name}_{years}_evaluation"
        )

    # more precise falsification than that of the evaluation function, but takes longer
    # it employs a larger max_num_samples_run in the kernel_based function used to perform CI-tests
    if with_falsification:
        print("falsification")
        falsification_result = falsify_graph(
            causal_graph=causal_graph,
            data=df_data,
            plot_histogram=True,
            suggestions=False,
            n_permutations=50,
            allow_data_subset=False,
            significance_level=0.05,
        )
        dir_new = dir + "falsification/"
        save_file(
            falsification_result, dir=dir_new, filename=f"{name}_{years}_falsification"
        )
