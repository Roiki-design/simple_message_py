#!/usr/bin/env python

from twisted.internet import reactor
from twisted.application import internet, service
from twisted.names import server, dns, hosts
from simple_message import protocol, StandardSocketPorts
port = 53


# Create a MultiService, and hook up a TCPServer and a UDPServer to it as
# children.
factory = protocol.SimpleMessageFactory()
simplemessageService = service.MultiService()

trajectory_service = internet.TCPServer(protocol.StandardSocketPorts.MOTION, factory).setServiceParent(simplemessageService)
feedback_service = internet.TCPClient("192.168.3.240", protocol.StandardSocketPorts.STATE, factory).setServiceParent(simplemessageService)



# Create an application as normal
application = service.Application("SimpleMessage")

# Connect our MultiService to the application, just like a normal service.
simplemessageService.setServiceParent(application)
