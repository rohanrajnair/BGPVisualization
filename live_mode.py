from datetime import date
import time


#read that stream into a file
#read from that file to create an animation?
#

#this function forms the stream
#read into buffer of size X, once buffer is full, do stuff, remove everython but last element in buffer
#append that element first, keep reading?

streamFilter = ""
streamBuffer = []
"""
Fiji: My current idea is to use this function to clean up the data to a form that can be used for create_graph in
a way that won't require us to use files.
So the purpose of this function is to take the data obtained from ris, as well as a boolean that indicates
if the user wants to output the raw data to a file for later. Then take that raw data and convert it to something like
this via the getDataAndConvert function
#protocol|timestamp|Withdrawal/announcement/routing|peerIP|peerASN|prefixes|path|originprotocol|Nexthop|local pref|MED|
Community strings|atomic aggregator|aggregator|
Then take that and use a live version of what Rohan has implemented to do the process of generating the graphs and stuff
"""
def getDataAndConvert(userStream,putInFile,fileName):
    #wait some length of time for buffer to get data, read from buffer, keep adding to buffer.
    #after X length of time, clear the buffer up until the last index before the clear function is called
    #continue adding and reading
    #try to implement sliding window-esque functionality
    #protocol|timestamp|Withdrawal/announcement/routing|peerIP|peerASN|prefixes|path|originprotocol|Nexthop|local pref|MED|Community strings|atomic aggregator|aggregator|
    #Protocol|1203878361|A|194.85.4.55|3277|202.133.47.0/24|3277 3267 2603 3549 6762 17557|INCOMPLETE|194.85.4.55|0|0|3277:3267 3277:65100 3277:65320 3277:65326|NAG||
    convertedData = []
    communityString = ""
    lastIndex = 0
    beforeClear = 0
    if (putInFile is True): # Writes raw data to file if user desires
        fileDesc = open(fileName, 'a')
        for i in range(len(userStream)):
            fileDesc.write(userStream[i])
        fileDesc.close()
    #use this to convert to something like Rohan's filtered format
    for item in userStream:
        #this checks if the "community" tag exists and converts it to the bgpduimp format
        if(item['community']):
            for link in item['community']:
                communityString = communityString + link[0]+":"+link[1] + " "
        communityString.strip()
        # added this to ignore IPv6 addresses
        if(":" in item['peer']):
            continue
        #turns announcements to BGP format
        if(item['announcements']):
            dataString = "BGP4MP|" + item['timestamp'] + "|A|" +item["peer"]+"|" + item['peer_asn']+"|"+item['announcements']['prefixes'],\
            + "|" + item['path'] + "|"+item["origin"]+"|"+item['announcements']['next_hop']+"|0|0|"+ communityString + "|NAG|"+"||"
        if(item['withdrawals']):#not complete yet
            dataString = "BGP4MP|" + item['timestamp'] + "|"
        convertedData.append(dataString)
    return convertedData
