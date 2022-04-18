import json
import websocket

ws = websocket.WebSocket()

# TO DO
# filter to only include announcements
# 
ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-manual-example")
ws.send(json.dumps({"type": "ris_subscribe", "data": {"host": "rrc21", "path": 3356}}))
res = []
num_messages = 200
for data in ws:
    parsed = json.loads(data)
    res.append(parsed)
    num_messages -=1
    if num_messages <=0:
        break

with open("sample_data.json", 'w') as json_file:
    json.dump(res, json_file, 
                        indent=4,  
                        separators=(',',': '))
    # print(parsed["type"], parsed["data"])