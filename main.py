import sys
import rislive2
#create workflow for all files
#add command line arg that does live monitoring or takes files based on what user wants


#have user specify where to get stream from

# we read that stream into an array
#store as buffer
#read from buffer every X seconds where X is specified by user
#user also specifies IP's and AS's of interest via extra command line args
#user specifies whether live or upload
#essentially 2 paths to follow based on user desire
#specify filtering for peers


#if the user specifies a certain prefix, use filtering.py, else just go straight to the live_mode stuff
#RIS and pyBGPstream may do the prefix filtering for us, make that clear to user by making them
#say peer and prefix in exact syntax for filtering for pyBGPStream

#-l flag for live mode, -u for upload
#0 is filename
#1 is live or upload
def main(argv):
    print("hello")
    #if user chooses liveMode, run liveMode script
    if((argv[1]=="-l")or(argv[1]=="-L")):
        rislive2.goLive(argv)
    if((argv[1]=="-u")or(argv[1]=="-U")):  #if this happens, we let the user upload a file, maybe implement later
        pass
#main([0, "-l", "-nf", 2, 0, '208.65.152.0/22', '3356'])
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
Running from command line: -l -nf 2 0 208.65.152.0/22 3356
"""
if __name__ == "__main__":
    main(sys.argv[0:])