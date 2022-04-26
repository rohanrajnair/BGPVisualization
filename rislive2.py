import json
import os

import websocket,live_mode,time,create_graph,graph_diff
from datetime import date

def main(argv): #this will have to be a function that takes in params passed from main when the whole thing is put together
    ws = websocket.WebSocket() #Added by adriel, create websocket to connect to RISlive
    websocket.WebSocket()
    fileName = str(date.today()) + str(time.time()) + str(argv[4])+".txt" #trying to do dynamic file creation if user wants
    #stuff output to file
    tidyData =[]
    #setting names of files to write to and save images to
    liveGraphPickleOne = 'firstgraph.pickle'
    liveGraphPickleTwo = 'secondgraph.pickle'
    liveGraphImgOne = 'firstgraph.png'
    liveGraphImgTwo = 'secondgraph.png'
    # TO DO
    #erase old versions of the files
    try:
        os.remove(liveGraphPickleOne)
        os.remove(liveGraphImgOne)
        os.remove(liveGraphImgTwo)
        os.remove(liveGraphPickleTwo)
        os.remove('rib_graph_diff.png')
    except:#if it cant find the files to remove just continue bc itll make them
        pass
    #get command line params and set booleans
    """
    argv[0] is python filename
    argv[1] is live or upload use: "-l" or "-u"
    argv[2] is whether or not they want the data output to a file as well (check live_mode.py) use : "-f" or "-nf"
    argv[3] is the desired update time in seconds
    argv[4] no use yet, was supposed to be desires prefix but I changed stuff
    argv[5] is the desired prefix?
    argv[6] is the desired peer/AS
   if argv 1 indicates live programming, open up a socket, make argv 3 the desired path?
    Example: main([0,"-l","-nf",2,0,'208.65.152.0/22','3356'])
    """
    fileOption = argv[2]
    userPath = str(argv[6])
    global globalDest
    globalDest = setDestPrefix(argv[4])
    calledOnce = False
    graphInitialized = False

    #0 to size, oldsize=size, oldsize to size
    execNumber = 0 #if exec num is zero, file names are some val, if exec num is one file names are other val
    makeintoFile = False
    if(argv[1]=="-l"or"-L"): #if live mode
        if((fileOption == "-f")or(fileOption=="-F")): #check if output to file is desired
            makeintoFile = True #set flag if yest
        ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-manual-example")
        ws.send(json.dumps({"type": "ris_subscribe", "data": {"host": "rrc21", "path": userPath}}))
        res = []
        updateFrequency = argv[3] #give the update freq

        #updateFrequency is in seconds, if more than an hour, default to 1 minute
        if (updateFrequency > 3600):
            updateFrequency = 60
        #num_messages = 200
        firstCall = time.time() #set time marker
        oldIndex = 0 #to help implement "sliding window", I need to add a clear function to make sure the array
        #doesn't get too large since the data we're getting is constantly flowing
        for data in ws: #added by Adriel, connects stuff and adds to an array
            parsed = json.loads(data)
            res.append(parsed)
            #num_messages -=1
            #take note of the array size
            newIndex = len(res)-oldIndex
            if ((graphInitialized == False) and (firstCall>0)):  # make the first graph to display to the user, will
                #probably only be one node ?
                create_graph.make_live_graph(live_mode.getDataAndConvert(res, makeintoFile, fileName), liveGraphPickleOne,
                                             liveGraphImgOne,
                                             output_to_file=True)  # use makelivegraph bc functions are using arrays now
                graphInitialized = True
            curTime = time.time()
            if(curTime-firstCall >= updateFrequency): #if the desired update time has passed, start update process
                if(calledOnce==False): #if first update, do this
                    newres = res[oldIndex:newIndex]
                    calledOnce = True
                #don't pass in res, pass in a range of res
                else: #if any other update, do this
                    newres = res[oldIndex:len(res)]
                execNumber = updateGraph(graphInitialized,execNumber,makeintoFile,newres,fileName) #call update graph
                firstCall = curTime #reset time window
                oldIndex = newIndex #need to make a clear function
#calledOnce goes with graphInitialized,execNum goes with execNumber, makeFile and makeInto file, resourceArr with res, mycleanData = tidyData
def updateGraph(calledOnce,execNum,makeFile,resourceArr,myfileName):#add params for before and after index
#subsequent graphs are done when user wants update
# #after X length of time, send the data to be parsed, then continue reading.
    tidyData = []
    liveGraphPickleOne = 'firstgraph.pickle'
    liveGraphPickleTwo = 'secondgraph.pickle'
    liveGraphImgOne = 'firstgraph.png'
    liveGraphImgTwo = 'secondgraph.png'
    if(makeFile is True):
        tidyData = live_mode.getDataAndConvert(resourceArr, makeFile, myfileName) #this converts it to a bgpdump string
        #and writes it to a file
            #Need to make use of the "lastINdex" and "beforeClear" variables, sliding window isn't really implemented
            #yet.
    tidyData = live_mode.getDataAndConvert(resourceArr,makeFile,"noFile") #convert the data to bgpdump string

    #execNum being 1 or zero basically dicatates which sets of files are the oldest and should be overwritten
    if(execNum==0): #call make graph, then call make diff graph then after only call update
        #call live make diff graph, always show diff between old and new version?
        calledOnce = True
        #ignore lines 109 to 113
        #make new graph using update
            #graph made when creategraph called make llive graph(livegraphpickeone,livegraphimage one) , the array,
        #update the graph after showing the diff?
        #graph update basically says first param is old stuff, write new stuff to last param
        #so if i get info and just overwrite old data,then i can use the same 2 files


        # I overwrite the old image and pickle because they won't be used again after the system updates and.
            #shows the user a new version of the network
        #take the old data, get the most recent update, write that update to the oldest (or blank) file
        graph_diff.live_make_diff_udpate_graph(liveGraphPickleOne,
                                               live_mode.getDataAndConvert(resourceArr, makeFile, myfileName),
                                               'path_list.txt', liveGraphImgTwo, liveGraphPickleTwo)
        #show the difference/what was added
        graph_diff.live_make_diff_graph(liveGraphPickleOne, liveGraphPickleTwo, 'rib_graph_diff.png')

        execNum = 1
        return execNum
    #TODO if execnum is 1
    if(execNum==1): #this is so we can use 2 image files and the one we need doesn't get overwritten.
        # use makelivegraph bc we're using arrays now
        calledOnce = True

        #take the old data, get the most recent update, write that update to the oldest (or blank) file
        graph_diff.live_make_diff_udpate_graph(liveGraphPickleTwo,
                                               live_mode.getDataAndConvert(resourceArr, makeFile, myfileName),
                                               'path_list.txt', liveGraphImgOne, liveGraphPickleOne)
        #show the difference/what was added
        graph_diff.live_make_diff_graph(liveGraphPickleTwo, liveGraphPickleOne, 'rib_graph_diff.png')
        execNum = 0
        return execNum #return execnum to let system know what oldest files are
        #TODO ignore lines 141 to 145
        #first param is array, second and third are desired filenames, these should relate to the
        # very first call to make the graph diff
            #break
            #update execnumber
        #make program delete files used on termination

def setDestPrefix(userPrefix): #sets user specified destination prefix
    globalPre = userPrefix
    return globalPre
def getDestPrefix(): #gets user specified destination prefix
    return globalDest
main([0,"-l","-nf",2,0,'208.65.152.0/22','3356'])

#TODO you can ignore this stuff here
#argv[0] is python filename
#argv[1] is live or upload
#argv[2] is whether or not they want the data output to a file as well -f or -nf
#argv[3] is the desired update time in seconds
#argv[4] is the desired peer/AS?
# with open("sample_data.json", 'w') as json_file:
#     json.dump(res, json_file,
#                         indent=4,
#                         separators=(',',': '))
#     # print(parsed["type"], parsed["data"])