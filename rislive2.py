import json
import websocket,live_mode,time
from datetime import date

def main(argv):
    ws = websocket.WebSocket()
    websocket.WebSocket()
    fileName = date.today() + time.time() + argv[4]+".txt"
    tidyData =[]
    # TO DO
    """ filter to only include announcements?
    argv[0] is python filename
    argv[1] is live or upload use: "-l" or "-u"
    argv[2] is whether or not they want the data output to a file as well use : "-f" or "-nf"
    argv[3] is the desired update time in seconds
    argv[4] is the desired peer/AS?
   if argv 1 indicates live programming, open up a socket, make argv 3 the desired path?
    """
    makeFile = False
    if(argv[1]=="-l"or"-L"):
        if(argv[2]=="-f"or"-F"):
            makeFile = True
        ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-manual-example")
        ws.send(json.dumps({"type": "ris_subscribe", "data": {"host": "rrc21", "path": 3356}}))
        res = []
        updateFrequency = argv[2]
        #updateFrequency is in seconds, if more than an hour, default to 1 minute
        if (updateFrequency > 3600):
            updateFrequency = 60
        #num_messages = 200
        firstCall = time.time()
        for data in ws:
            parsed = json.loads(data)
            res.append(parsed)
            #num_messages -=1
            curTime = time.time()
            if (curTime-firstCall >= updateFrequency):#after X length of time, send the data to be parsed, then continue reading.
                if(makeFile is True):
                    live_mode.getDataAndParse(res, makeFile, fileName)

                tidyData = live_mode.getDataAndConvert(res,makeFile,"noFile") #convert the data
                firstCall = curTime #update the time interval
                break
    #After breaking, call getDataAndParse
main([0,"-l","-nf",2,0])
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