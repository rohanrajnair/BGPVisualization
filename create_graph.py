import networkx as nx
import ipaddress
import pickle
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import sys
import subprocess

# prefix of interest for 2008 BGP hijacking attack
des_prefix = "208.65.152.0/22"
#des_prefix = str(rislive2.getDestPrefix())

class table_entry:
  def __init__(self, asn, ip, path):
    self.asn = asn
    self.ip = ip
    self.path = path

# check if one prefix is a sub-prefix of another
def is_subprefix(prefix1, prefix2):
    addr1 = ipaddress.ip_interface(prefix1)
    addr2 = ipaddress.ip_interface(prefix2)
    host_list1 = addr1.network.hosts()
    host_list2 = addr2.network.hosts()
    if (set(host_list1).issubset(set(host_list2))):
        return True
    return False

def parse_rib_line(line): #maybe set a flag if the user specifies a particular prefix?
    path = []
    line_arr = line.split("|")
    curr_prefix = line_arr[5]
    if is_subprefix(curr_prefix, des_prefix): #if flag true do this? otherwise just get the path and prefix
        path = line_arr[6].split()
    return path, curr_prefix

def parse_live_rib_line(line):
    path = []
    line_arr = line.split("|")
    curr_prefix = line_arr[5]
    # if is_subprefix(curr_prefix, des_prefix):
    path = line_arr[6].split()
    return path, curr_prefix

def filter_data(dump_file, output_file):
    # dumping contents of rib/update file
    # bashCommand = "python3 mrt2bgpdump.py " + src_file + " -m > " + dump_file
    # output = subprocess.check_output(['bash', '-c', bashCommand])

    # further filtering by ASNs (YouTube and Pakistan Telecom)
    bashCommand = "grep \"36561\|17557\" " + dump_file + " > " + output_file
    output = subprocess.check_output(['bash', '-c', bashCommand])



def make_graph(src_file, pkl_file, img_file, output_to_file=False):
    edges = []
    nodes = []

    f = open(src_file)

    f2 = open('prefix_to_asn.txt', 'a')

    f3 = open('path_list.txt', 'a')

    for line in f:
        path, prefix = parse_rib_line(line)
        if path:
            if output_to_file:
                f2.write(prefix + '\t' + path[-1] + '\n')
                for j in range(len(path)):
                    f3.write(path[j])
                    if j != len(path) - 1:
                        f3.write(' ')
                    else:
                        f3.write('\n')

            for i in range(len(path) - 1):
                n1 = path[i]
                n2 = path[i+1]
                edges.append((n1, n2))
                if n1 not in nodes:
                    nodes.append(n1)
                if n2 not in nodes:
                    nodes.append(n2)

    f.close()
    f2.close()
    f3.close()
    my_graph = nx.Graph()
    my_graph.add_nodes_from(n for n in nodes)
    my_graph.add_edges_from((u, v) for u, v in edges)
    with open(pkl_file, 'wb') as handle:
        pickle.dump(my_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
    base_options = dict(with_labels=True, edgecolors="black", node_size=2000)
    plt.figure(figsize=(40, 40))
    plt.tight_layout()

    node_colors = ["#A0CBE2" for i in range(len(nodes))]

    # target ASN
    for i in range(len(nodes)):
        if nodes[i] == '36561':
            node_colors[i] = '#FFFF00'

    nx.draw_networkx(my_graph, node_color=node_colors, **base_options)
    plt.savefig(img_file)
    #plt.show()
    #make this return the list of graph names

#this is a copy of make_graph that uses arrays for a potential live implementation
def make_live_graph(prefixToASNArray,pkl_file, img_file, output_to_file=False):
    edges = []
    nodes = []

    f = prefixToASNArray

    f2 = open('prefix_to_asn.txt', 'a')

    f3 = open('path_list.txt', 'a')

    for line in f:
        path, prefix = parse_live_rib_line(line) #doesnt account for specific prefixes rn
        if path:
            if output_to_file:
                f2.write(prefix + '\t' + path[-1] + '\n')
                for j in range(len(path)):
                    f3.write(path[j])
                    if j != len(path) - 1:
                        f3.write(' ')
                    else:
                        f3.write('\n')

            for i in range(len(path) - 1):
                n1 = path[i]
                n2 = path[i+1]
                edges.append((n1, n2))
                if n1 not in nodes:
                    nodes.append(n1)
                if n2 not in nodes:
                    nodes.append(n2)

    #f.close()
    f2.close()
    f3.close()
    my_graph = nx.Graph()
    my_graph.add_nodes_from(n for n in nodes)
    my_graph.add_edges_from((u, v) for u, v in edges)
    with open(pkl_file, 'wb') as handle:
        pickle.dump(my_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
    base_options = dict(with_labels=True, edgecolors="black", node_size=2000)
    plt.figure(figsize=(40, 40))
    plt.tight_layout()

    node_colors = ["#A0CBE2" for i in range(len(nodes))]

    # target ASN
    for i in range(len(nodes)):
        if nodes[i] == '36561':
            node_colors[i] = '#FFFF00'

    nx.draw_networkx(my_graph, node_color=node_colors, **base_options)
    plt.savefig(img_file)

#always make graph_rib1 and 2 pickle and graph 1 and 2 png. keep array though
#make_graph('filteredOutput/filtered_rib_data.txt', 'graph_rib1.pickle', 'graphsAndVisuals/graph_rib1.png', output_to_file=True)

#make_graph('filteredOutput/filtered_rib_data2.txt', 'graph_rib2.pickle', 'graphsAndVisuals/graph_rib2.png')