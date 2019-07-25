# simple_message_py
A Python (Twisted) implementation of the Simple Message protocol


A working server implementation of ROS simple message protocol. The current server interfaces with ROS and moveit through industrial robot client and exposes joint positions in a simple dictionary for further use. Also included are simple server/client programs for testing and developing applications. 

Currently working on a server that handles sending individual motion commands to indidividual motor drivers through ethernet/UART adapters.

TODO:
interfaceing with motor drivers
more testing
Recording and playback
remote with gui and its interface
whatever else i come up with
