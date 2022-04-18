import pickle
import networkx as nx
import matplotlib.pyplot as plt
from create_graph import filter_data, is_subprefix, parse_update_line, des_prefix

def calc_diff(graph1, graph2):
    edge_diff = list(set(graph2.edges) - set(graph1.edges))
    node_diff = list(set(graph2.nodes) - set(graph1.nodes))
    return edge_diff, node_diff

def report_stats(edge_diff, node_diff):
    num_route_changes = len(edge_diff)
    num_new_nodes = len(node_diff)

    f = open('asn_to_owner.txt', 'r')
    file_content = f.read()
    asn_to_owner_list = file_content.split('\n')
    f.close()

    f = open('statistics.txt', 'w')
    f.write('Route Changes: ' + str(num_route_changes) + '\n')
    f.write('New Nodes: ' + str(num_new_nodes) + '\n')
    for i in node_diff:
        f.write(asn_to_owner_list[int(i)-1] + '\n')
    f.close()

# diff between two rib files
def make_diff_graph(pkl1, pkl2, img_file):
    with open(pkl1, 'rb') as handle:
        rib1_graph = pickle.load(handle)

    with open(pkl2, 'rb') as handle:
        rib2_graph = pickle.load(handle)

    edge_diff, node_diff = calc_diff(rib1_graph, rib2_graph)

    # reporting statistics
    report_stats(edge_diff, node_diff)

    edge_weights = []
    node_colors = []
    #edge_styles = []

    for e in rib2_graph.edges:
        if e in edge_diff:
            edge_weights.append(3.0)
            #edge_styles.append("dashed")
        else:
            edge_weights.append(1.0)
            #edge_styles.append("solid")

    for n in rib2_graph.nodes:
        if n in node_diff:
            node_colors.append("#FDAD5C")
        else:
            node_colors.append("#A0CBE2")


    base_options = dict(with_labels=True, edgecolors="black", node_size=2000)

    graph_diff = nx.Graph()
    graph_diff.add_nodes_from(rib2_graph.nodes)
    graph_diff.add_edges_from(rib2_graph.edges)

    plt.figure(figsize=(40, 40))
    plt.tight_layout()

    nx.draw_networkx(graph_diff, node_color=node_colors, width=edge_weights, **base_options)
    plt.savefig(img_file)
    return graph_diff

graph_diff = make_diff_graph('graph_rib1.pickle', 'graph_rib2.pickle', 'graph_diff_test.png')

