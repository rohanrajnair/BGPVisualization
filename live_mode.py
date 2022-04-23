import pybgpstream

#if user chooses live, navigate them here
#get stream from specified RIS place
#read that stream into a file
#read from that file to create an animation

#this function forms the stream
#read into buffer of size X, once buffer is full, do stuff, remove everython but last element in buffer
#append that element first, keep reading?

streamFilter = ""
streamBuffer = []
def formStream(chosenCollector):
    if(chosenCollector!=""):
        streamFilter = "collector" + " " + chosenCollector
    else:
        #if the user doesn't give a filter, just use this as the default.
        streamFilter = "collector rrc00"

    chosenStream = pybgpstream.BGPStream(
        #Don't modify this line, this makes sure it goes to ris live
        project = "ris-live",

        filter = streamFilter,
    )


def getDataAndParse(userStream):
    #wait some length of time for buffer to get data, read from buffer, keep adding to buffer.
    #after X length of time, clear the buffer up until the last index before the clear function is called
    #continue adding and reading
    #try to implement sliding window-esque functionality
    lastIndex = 0
    beforeClear = 0
    while(userStream):

