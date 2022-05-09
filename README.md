# BGPVisualization

### Creating Static Visualizations
In order to create static visualizations from the live BGP message data, we must run the ```main.py``` script.
This script takes in the following command line arguments:
```
argv[0] is python filename
argv[1] is live or upload use: "-l" or "-u"
argv[2] is whether or not they want the data output to a file as well (check live_mode.py) use : "-f" or "-nf"
argv[3] is the desired update time in seconds
argv[4] no use yet, was supposed to be desires prefix but I changed stuff
argv[5] is the desired prefix?
argv[6] is the desired peer/AS
if argv 1 indicates live programming, open up a socket, make argv 3 the desired path?
Example: main([0,"-l","-nf",2,0,'208.65.152.0/22','3356'])
Running from command line: -l -nf 2 0 208.65.152.0/22 3356
If no specific path or AS is desired, list both as 0
Ex: -l -nf 2 0 0 0
```

### Starting up the Webpage Locally:

Make sure [Node.js](https://nodejs.org/en/) is installed!

```
 cd .\cytoscape_graph\bgpvizapp\
 npm install
 node .\index.js
```
App url: http://localhost:3000/ 

### App Screenshot:
![image](https://user-images.githubusercontent.com/59209071/167343246-c9dd013f-3aef-46ee-adeb-7d13b15df90d.png)
