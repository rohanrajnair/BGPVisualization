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

def parse_rib_line(line):
    path = []
    line_arr = line.split("|")
    curr_prefix = line_arr[5]
    if is_subprefix(curr_prefix, des_prefix):
        path = line_arr[6].split()
    return path

def parse_update_line(line):
    is_withdrawal = False
    path = []
    line_arr = line.split("|")
    entry_type = line_arr[2] # announcement or withdrawal
    curr_prefix = line_arr[5]



def filter_data(dump_file, output_file):
    # dumping contents of rib/update file
    # bashCommand = "python3 mrt2bgpdump.py " + src_file + " -m > " + dump_file
    # output = subprocess.check_output(['bash', '-c', bashCommand])

    # further filtering by ASNs (YouTube and Pakistan Telecom)
    bashCommand = "grep \"36561\|17557\" " + dump_file + " > " + output_file
    output = subprocess.check_output(['bash', '-c', bashCommand])



def make_graph(src_file, pkl_file, img_file):
    edges = []
    nodes = []

    f = open(src_file)

    for line in f:
        path = parse_rib_line(line)
        if path:
            for i in range(len(path) - 1):
                n1 = path[i]
                n2 = path[i+1]
                edges.append((n1, n2))
                if n1 not in nodes:
                    nodes.append(n1)
                if n2 not in nodes:
                    nodes.append(n2)

    my_graph = nx.Graph()
    my_graph.add_nodes_from(n for n in nodes)
    my_graph.add_edges_from((u, v) for u, v in edges)
    with open(pkl_file, 'wb') as handle:
        pickle.dump(my_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
    base_options = dict(with_labels=True, edgecolors="black", node_size=2000)
    plt.figure(figsize=(40, 40))
    plt.tight_layout()

    node_colors = ["#A0CBE2" for i in range(len(nodes))]

    nx.draw_networkx(my_graph, node_color=node_colors, **base_options)
    plt.savefig(img_file)
    #plt.show()

make_graph('filtered_rib_data.txt', 'graph_rib1.pickle', 'graph_rib1.png')

make_graph('filtered_rib_data2.txt', 'graph_rib2.pickle', 'graph_rib2.png')