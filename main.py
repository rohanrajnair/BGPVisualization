import create_graph,filtering,graph_diff,animation,live_mode

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