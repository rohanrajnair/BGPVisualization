import ipaddress

des_prefix = "208.65.152.0/22"

def is_subprefix(prefix1, prefix2):
    addr1 = ipaddress.ip_interface(prefix1)
    addr2 = ipaddress.ip_interface(prefix2)
    host_list1 = addr1.network.hosts()
    host_list2 = addr2.network.hosts()
    if (set(host_list1).issubset(set(host_list2))):
        return True
    return False


def filter_update_file(update_file, output_file):
    f = open(update_file)
    f2 = open(output_file, 'a')
    for line in f:
        line_arr = line.split("|")
        curr_prefix = line_arr[5].strip()
        print(curr_prefix)
        if (is_subprefix(curr_prefix, des_prefix)):
            print("found!")
            f2.write(line)
    f.close()
    f2.close()
        
filter_update_file('updates_20080224_1839.txt', 'filtered_update_data1.txt')