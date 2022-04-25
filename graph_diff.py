import pickle
import ipaddress
import networkx as nx
import matplotlib.pyplot as plt
import rislive2

# This File is calculating the difference between two graphs and drawing it
des_prefix = "208.65.152.0/22"
#make array that calls make diff graph on index 0 and index 1 in that order

# 4/21/2022 Changed filter_update_data to also take a command line parameter that looks at AS's of interest
def filter_update_data(dump_file, output_file):
    # dumping contents of rib/update file
    # bashCommand = "python3 mrt2bgpdump.py " + src_file + " -m > " + dump_file
    # output = subprocess.check_output(['bash', '-c', bashCommand])

    # further filtering by ASNs (YouTube and Pakistan Telecom)
    # TODO add functionality to check AS's of interest via command line params, if 0, then ignore?
    bashCommand = "grep \"36561\|17557\|W\" " + dump_file + " > " + output_file
    output = subprocess.check_output(['bash', '-c', bashCommand])


def is_subprefix(prefix1, prefix2):
    addr1 = ipaddress.ip_interface(prefix1)
    addr2 = ipaddress.ip_interface(prefix2)
    host_list1 = addr1.network.hosts()
    host_list2 = addr2.network.hosts()
    if (set(host_list1).issubset(set(host_list2))):
        return True
    return False


def parse_update_line(line): #may have to change this to change the des_prfix dynamically based on the prefixes in the array.
    is_withdrawal = False
    valid_flag = True
    path = []
    line_arr = line.split("|")
    entry_type = line_arr[2]  # announcement or withdrawal
    asn = line_arr[4].strip()
    curr_prefix = line_arr[5].strip()
    if is_subprefix(curr_prefix, des_prefix):
        if entry_type == 'A':
            path = line_arr[6].split()
        if entry_type == 'W':
            is_withdrawal = True
    else:
        valid_flag = False

    return valid_flag, path, asn, is_withdrawal, curr_prefix


def create_prefix_asn_mapping(filename):
    ip_asn_map = {}
    f = open(filename)
    for line in f:
        line_arr = line.split('\t')
        if line_arr[0] not in ip_asn_map:
            ip_asn_map[line_arr[0]] = [line_arr[1]]
        else:
            ip_asn_map[line_arr[0]].append(line_arr[1])
    f.close()
    return ip_asn_map


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
        f.write(asn_to_owner_list[int(i) - 1] + '\n')
    f.close()


# diff between two rib files
def make_diff_graph(pkl1, pkl2, img_file): #prefix to asn should be kept constant?
    with open(pkl1, 'rb') as handle:
        rib1_graph = pickle.load(handle)

    with open(pkl2, 'rb') as handle:
        rib2_graph = pickle.load(handle)

    edge_diff, node_diff = calc_diff(rib1_graph, rib2_graph)

    # reporting statistics
    report_stats(edge_diff, node_diff)

    edge_weights = []
    node_colors = []
    edge_styles = []
    edge_colors = []

    for e in rib2_graph.edges:
        if e in edge_diff:
            edge_weights.append(3.0)
            # edge_styles.append("dashed")
            edge_colors.append("#00FF00")
        else:
            edge_weights.append(1.0)
            # edge_styles.append("solid")
            edge_colors.append("#000000")

    for n in rib2_graph.nodes:
        if n in node_diff:
            node_colors.append("#00FF00")
        else:
            node_colors.append("#A0CBE2")

    node_list = list(rib2_graph.nodes)
    for i in range(len(node_list)):
        if node_list[i] == '36561' or node_list[i] == '17557':
            node_colors[i] = '#FFFF00'

    base_options = dict(with_labels=True, edgecolors='black', node_size=2000)

    graph_diff = nx.Graph()
    graph_diff.add_nodes_from(rib2_graph.nodes)
    graph_diff.add_edges_from(rib2_graph.edges)

    plt.figure(figsize=(40, 40))
    plt.tight_layout()

    nx.draw_networkx(graph_diff, node_color=node_colors, edge_color=edge_colors, **base_options)
    plt.savefig(img_file)
    return graph_diff

#takes pickle made from graph creation
def make_diff_udpate_graph(rib_pkl, update_file, path_file, img_file, output_pkl):
    with open(rib_pkl, 'rb') as handle:
        rib_graph = pickle.load(handle)

    f = open(update_file, 'r') #this is reading from an update file, an array could be placed here to reduce file opening
    f2 = open(path_file, 'r') #this should stay as is

    deleted_edges = []
    new_edges = []
    new_nodes = []

    old_node_list = list(rib_graph.nodes)
    old_edge_list = list(rib_graph.edges)

    asn_prefix_map = create_prefix_asn_mapping('prefix_to_asn.txt')

    f3 = open('prefix_to_asn.txt', 'a') #appends to prefix_to_asn

    paths = []
    for line in f2:
        curr_path = line.split(' ')
        paths.append(curr_path)

    f2.close()
    f2 = open('path_list.txt', 'a') #appends to preexisting

    for line in f: #for each line in the array, parse the update, this would work for an array
        valid_flag, path, asn, is_withdrawal, curr_prefix = parse_update_line(line)
        if valid_flag:
            if is_withdrawal:
                print('FOUND WITHDRAWAL ANNOUNCEMENT')
                target_asn = asn_prefix_map[curr_prefix][0]
                for p in paths:
                    if p[0] == asn and p[-1] == target_asn:
                        print('FOUND PATH')
                        for i in range(len(p) - 1):
                            n1 = p[i]
                            n2 = p[i + 1]
                            deleted_edges.append((n1, n2))
                            print('APPENDED EDGE TO DELETED')
            else:
                for j in range(len(path)):
                    f2.write(path[j])
                    if j != len(path) - 1:
                        f2.write(' ')
                    else:
                        f2.write('\n')
                f3.write(curr_prefix + '\t' + path[-1] + '\n')
                for i in range(len(path) - 1):
                    n1 = path[i]
                    n2 = path[i + 1]
                    if (n1, n2) not in old_edge_list:
                        new_edges.append((n1, n2))
                    if n1 not in old_node_list and n1 not in new_nodes:
                        new_nodes.append(n1)
                    if n2 not in old_node_list and n2 not in new_nodes:
                        new_nodes.append(n2)

    node_colors = []
    edge_colors = []
    edge_styles = []

    nodes = []
    edges = []

    for i in range(len(old_node_list)):
        nodes.append(old_node_list[i])
        node_colors.append("#A0CBE2")

    for i in range(len(new_nodes)):
        nodes.append(new_nodes[i])
        node_colors.append("#00FF00")

    for i in range(len(old_edge_list)):
        edges.append(old_edge_list[i])
        if old_edge_list[i] in deleted_edges:
            edge_styles.append("dashed")
            edge_colors.append("#FF0000")
        else:
            edge_styles.append("solid")
            edge_colors.append("#000000")

    for i in range(len(new_edges)):
        edges.append(new_edges[i])
        edge_styles.append("solid")
        edge_colors.append("#00FF00")

    for i in range(len(nodes)):
        if nodes[i] == '36561' or nodes[i] == '17557':
            node_colors[i] = '#FFFF00'

    base_options = dict(with_labels=True, edgecolors='black', node_size=2000)

    graph_diff = nx.Graph()
    graph_diff.add_nodes_from(nodes)
    graph_diff.add_edges_from(edges)

    with open(output_pkl, 'wb') as handle:
        pickle.dump(graph_diff, handle, protocol=pickle.HIGHEST_PROTOCOL)

    plt.figure(figsize=(40, 40))
    plt.tight_layout()

    nx.draw_networkx(graph_diff, node_color=node_colors, edge_color=edge_colors, style=edge_styles, **base_options)
    plt.savefig(img_file)
    f.close() #make sure to remove this for the array version
    f2.close()
    f3.close()
    return graph_diff

#make temp picke 1 and temp pickle 2. based on even or odd declaration, call temp_pickle and temp_pickle2
#or call temp_pickle2 and temp_pickle1
#path_list.txt is always used
#make a tmp.png and a tmp2.png always
#make a filtered_updatedata1 and filtered update data 2?
# graph_diff = make_diff_graph('graph_rib1.pickle', 'graph_rib2.pickle', 'rib_graph_diff.png')
                                                            #store arrays from 2 iterations, current and previous.
# graph_diff = make_diff_udpate_graph('graph_rib1.pickle', 'filtered_update_data1.txt', 'path_list.txt', 'tmp.png', 'temp.pickle')
# graph_diff = make_diff_udpate_graph('temp.pickle', 'filtered_update_data2.txt', 'path_list.txt', 'tmp2.png', 'temp2.pickle')
# graph_diff = make_diff_udpate_graph('temp2.pickle', 'filtered_update_data3.txt', 'path_list.txt', 'tmp4.png', 'temp3.pickle')
# graph_diff = make_diff_udpate_graph('temp3.pickle', 'filtered_update_data4.txt', 'path_list.txt', 'tmp4.png', 'temp4.pickle')
# graph_diff = make_diff_udpate_graph('temp4.pickle', 'filtered_update_data5.txt', 'path_list.txt', 'tmp5.png', 'temp5.pickle')
