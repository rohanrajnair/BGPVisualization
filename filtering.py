import ipaddress

des_prefix = "208.65.152.0/22"
#checks if one IP is a subprefix of another IP
def is_subprefix(prefix1, prefix2):
    addr1 = ipaddress.ip_interface(prefix1)
    addr2 = ipaddress.ip_interface(prefix2)
    host_list1 = addr1.network.hosts()
    host_list2 = addr2.network.hosts()
    if (set(host_list1).issubset(set(host_list2))):
        return True
    return False

#okay, so what I'm understanding is this makes a new output file
#with only the destination of interest?
#It doesn't change the AS's in there, it can accept any AS
def filter_update_file(update_file, output_file):
    f = open(update_file)
    f2 = open(output_file, 'a') #open an update file and output file, split based on the |,
    for line in f: #for every IP address, write it to the output file if its destination
        #is a subprefix of the current prefix
        line_arr = line.split("|")
        curr_prefix = line_arr[5].strip()
        print(curr_prefix)
        if (is_subprefix(curr_prefix, des_prefix)):
            print("found!")
            f2.write(line)
    f.close()
    f2.close()

#copy of filter update for live implementation, the array indexes will have to change since the
#live data is longer and has the relevant information further ahead
#this may only be relevant if the user chooses a specific prefix

def live_filter_update_file(update_file, output_file):
    f = open(update_file)
    f2 = open(output_file, 'a')  # open an update file and output file, split based on the |,
    for line in f:  # for every IP address, write it to the output file if its destination
        # is a subprefix of the current prefix
        line_arr = line.split("|")
        curr_prefix = line_arr[5].strip()
        print(curr_prefix)
        if (is_subprefix(curr_prefix, des_prefix)):
            print("found!")
            f2.write(line)
    f.close()
    f2.close()


filter_update_file('updateFiles/updates_20080224_1839.txt', 'filteredOutput/filtered_update_data1.txt')