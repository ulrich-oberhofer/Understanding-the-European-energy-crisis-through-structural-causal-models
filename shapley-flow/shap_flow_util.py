from shapflow.flow import GraphExplainer, node_dict2str_dict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import graphviz
import seaborn as sns
import re

def calculate_edge_credit(causal_graph, bg_i, fg, nruns, silent=True):
    cf_c = GraphExplainer(causal_graph, bg_i, nruns=nruns, silent=silent).shap_values(fg)
    return node_dict2str_dict(cf_c.edge_credit)

def calculate_edge_credit_alt(causal_graph, bg_i, fg_file, nruns, silent=True):
    fg = read_csv_incl_timeindex(fg_file)
    cf_c = GraphExplainer(causal_graph, bg_i, nruns=nruns, silent=silent).shap_values(fg)
    return node_dict2str_dict(cf_c.edge_credit)

def read_csv_incl_timeindex(filepath):
    # expect column 'timestamp' to exist and contain valid timestamps
    df = pd.read_csv(filepath)
    df.index = pd.to_datetime(df['timestamp'])
    df.drop('timestamp', axis=1, inplace=True)
    return df

def read_csv_between(filepath, start_date, end_date):
    # includes start_date, includes end_date
    df = read_csv_incl_timeindex(filepath)
    return df[start_date:end_date]

def get_old_feature_name(new_name):
    new_to_old_name = {v: k for k, v in paper_rename_dict.items()}
    new_to_old_name['Price FR'] = 'price_da'
    new_to_old_name['Net exports FR'] = 'agg_net_export'
    old_name = new_to_old_name[new_name]
    return old_name

def plot_dependency(name1, name2, cf, fg_values, color=True, save=False, file_name='', figsize=(8, 7), x_label='', y_label='', color_label='', scale_color=1, scale_x=1, target=None):
    # note: if name2 is target feature, do not color graph (as shapley value directy indicates prediction value)
    for node1, d in cf.edge_credit.items():
        for node2, val in d.items():
            if node1.name == name1 and node2.name == name2:
                name1_old = name1
                df = fg_values[name1_old].copy()
                df_shap = pd.DataFrame(val.flatten(), index=df.index, columns=['shapley-flow'])
                df = pd.concat([df, df_shap], axis=1)
                plt.figure(figsize=figsize)
                plt.title('Dependence plot: {} → {}'.format(name1, name2))
                name2_old = name2 #get_old_feature_name(name2)
                if name2_old in fg_values.columns and color:
                    sc = plt.scatter(x=df[name1_old]/scale_x, y=df['shapley-flow'], s=5, c=fg_values[name2_old]/scale_color, cmap='viridis')
                    colorbar = plt.colorbar(sc)
                    if color_label == '':
                        colorbar.set_label(name2)
                    else: 
                        colorbar.set_label(color_label)
                else:
                    plt.scatter(x=df[name1_old]/scale_x, y=df['shapley-flow'], s=5, color=get_color(target))

                if x_label == '':
                    plt.xlabel(name1)
                else: 
                    plt.xlabel(x_label)
                if y_label == '':
                    if target == 'price':
                        y_unit = 'EUR/MWh'
                    elif target == 'export':
                        y_unit = 'MW'
                    plt.ylabel('Shapley flow value (' + y_unit + ')')
                else:
                    plt.ylabel(y_label)
                
                plt.tight_layout()
                if save:
                    plt.savefig("./plots/dependency_plots/{}_dependency_{}_{}.pdf".format(file_name, name1, name2))
                plt.show()
                return
    raise Exception("Feature not found in graph!")

# returns a dataframe containing the mean direct credit attribution (same as the SHAP attribution, i.e. edges in causal graph from input features to target features).
def get_mean_shap_attr(cf, target):
    dict = {}
    for node1, d in cf.edge_credit.items():
        for node2, val in d.items():
            if node2.name == target:
                dict[node1.name] = abs(val.flatten()).mean()
    return pd.DataFrame.from_dict(dict, orient='index', columns=['credit'])
              
def plot_beeswarm(cf, name1, name2, fg_values, color=False, save=False, file_name='', figsize=(8, 7)):
    for node1, d in cf.edge_credit.items():
        for node2, val in d.items():
            if node1.name == name1 and node2.name == name2:
                if color:
                    df = fg_values[name1].copy()
                    df_shap = pd.DataFrame(val.flatten(), index=df.index, columns=['shapley-flow'])
                    df = pd.concat([df, df_shap], axis=1)
                else:
                    df = pd.DataFrame(val.flatten(), index=fg_values.index, columns=['shapley-flow'])
                plt.figure(figsize=figsize)
                plt.title('Beeswarm plot: {} -> {}'.format(name1, name2))
                if name2 in fg_values.columns and color:
                    sc = plt.scatter(x=df[name1], y=df['shapley-flow'], s=5, c=fg_values[name2], cmap='viridis')
                    colorbar = plt.colorbar(sc)
                    colorbar.set_label(name2, fontsize=12)
                else:
                    sns.swarmplot(x=df['shapley-flow'])
                plt.xlabel(name1, fontsize=14)
                plt.ylabel('shapley-flow', fontsize=14)
                if save:
                    plt.savefig("./img/dependency_plots/{}_dependency_{}_{}.pdf".format(file_name, name1, name2))
                plt.show()
                return   

# replaces the edge colors and edge label colors in a dot string
def replace_dot_colors(dot_string: str, edge_color: str = None, font_color: str = None) -> str:
    if edge_color is not None:
        dot_string = re.sub(r'color="#[0-9a-fA-F]{6,8}"', f'color="{edge_color}"', dot_string)
    if font_color is not None:
        dot_string = re.sub(r'fontcolor="#[0-9a-fA-F]{6,8}"', f'fontcolor="{font_color}"', dot_string)
    return dot_string

def get_color(target: str) -> str:
    if target == None:
        color = '#008bfb'
    elif target == 'price':
        color = '#0173b2'
    elif target == 'export':
        color = '#de8f05'
    return color

def save_graph_paper(graph, path_file_name, target=None, format='pdf', view=False, font='Helvetica'):
    color = get_color(target)
    save_graph_color_font(graph, path_file_name=path_file_name, format=format, view=view, edge_color=color, font_color=color, font=font)

def add_or_replace_fontname(dot_string: str, font_name: str) -> str:
    def replace_font_block(match):
        block = match.group(0)
        if 'fontname=' in block:
            # ersetzen, wenn vorhanden
            block = re.sub(r'fontname="[^"]*"', f'fontname="{font_name}"', block)
        else:
            # einfügen vor schließendem ]
            block = block[:-1].rstrip() + f', fontname="{font_name}"]'
        return block

    return re.sub(r'\[.*?\]', replace_font_block, dot_string)

# save graph using this method to avoid overlapping edges (happens when using the save_graph method from shapley-flow)        
def save_graph_color_font(graph, path_file_name, format='pdf', view=False, edge_color=None, font_color=None, font='Helvetica'):
    # file name needs to be provided without file extension
    string = graph.string()
    string_color = replace_dot_colors(string, edge_color=edge_color, font_color=font_color)
    string_color_font = add_or_replace_fontname(string_color, font_name=font)
    G = graphviz.Source(string_color_font)
    G.render(path_file_name, format=format, view=view)

# rename a node in a shapley flow graph
def rename_node(g, old_name, new_name):
    node_names = []
    for x in g.nodes: node_names.append(x.name)
    index = node_names.index(old_name)
    g.nodes[index].name = new_name

# rename all nodes in shapley flow graph according to dictionary
def rename_all_nodes(g, dict):
    for old_name, new_name in dict.items():
        rename_node(g, old_name, new_name)

# rename nodes in creditflow object according to dict
def rename_nodes_in_graph(cf, dict):
    rename_all_nodes(cf.graph, dict)

paper_rename_dict = {
    'nuclear_avail': 'Nuclear availability',
    'carbon_price': 'Carbon price',
    'gas_price': 'Gas price',
    'solar_da': 'Solar day-ahead',
    'load_da': 'Load day-ahead FR',
    'wind_da': 'Wind day-ahead',
    'rl_BE': 'RL BE',
    'rl_DE_LU': 'RL DE-LU',
    'rl_ES': 'RL ES',
    'rl_IT_NORD': 'RL IT-North',
    'temp_mean': 'Air temperature',
    'river_temp': 'River temperature',
    'river_flow_mean': 'River flow rate',
    'rl_FR_ramp': 'RL ramp FR',
    'run_off_gen': 'ROR generation',
    'day_of_year_sin': 'Day of year (sin)',
    'day_of_year_cos': 'Day of year (cos)',
    'hour_sin': 'Hour (sin)',
    'hour_cos': 'Hour (cos)',
    'isworkingday': 'Is Working Day?'
}

def rename_nodes_in_graph_paper(cf):
    rename_nodes_in_graph(cf, paper_rename_dict)

def rename_target_node_paper(cf, target):
    if target == 'export':
        rename_nodes_in_graph(cf, {'agg_net_export': 'Net exports FR'})
    elif target == 'price':
        rename_nodes_in_graph(cf, {'price_da': 'Price FR'})
    else:
        raise Exception("Unknown target: {}".format(target))

def plot_bar_mean_abs_shap(cf, target_l, figsize=(6, 3.4), save=False, name='', xlabel='mean(|SHAP value|)', target=None):
    df = get_mean_shap_attr(cf, target_l)
    df = df.sort_values(by='credit', ascending=True)
    df.plot(kind='barh', legend=False, color=get_color(target), figsize=figsize, width=0.7)
    plt.xlabel(xlabel)
    plt.tight_layout()
    if save:
        plt.savefig('./plots/bar_plot_mean_abs_shap_{}.pdf'.format(name))
    plt.show()

def plot_bar_mean_abs_asv(cf, figsize=(6, 3.4), save=False, name='', xlabel='mean(|ASV attribution|)', target=None):
    sample_ind = -1
    cf.fold_noise = False
    # also draws graph, but easier to implement this way
    g = cf.draw_asv(idx=sample_ind, show_fg_val=True) 

    def get_name(s):
        suffix = ' noise'
        if s.endswith(suffix):
            s = s[:-len(suffix)]
        if s in paper_rename_dict:
            s = paper_rename_dict[s]
        return s

    dict = {}
    for edge in g.edges():
        node_name, b = edge
        credit = float(edge.attr['label'])
        feature_name = get_name(node_name)
        dict[feature_name] = credit
    df = pd.DataFrame.from_dict(dict, orient='index', columns=['credit'])
    df = df.sort_values(by='credit', ascending=True)
    df.plot(kind='barh', legend=False, color=get_color(target), figsize=figsize, width=0.7)
    plt.xlabel(xlabel)
    plt.tight_layout()
    if save:
        plt.savefig('./plots/bar_plot_mean_abs_ASV_{}.pdf'.format(name))
    plt.show()