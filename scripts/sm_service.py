from twisted.application import service, internet
from simple_message import *

port_listen = StandardSocketPorts.MOTION
port_feedback = StandardSocketPorts.STATE

factory = protocol.SimpleMessageFactory(Disable_nagle=True)

application_listen = service.application("motion")
application_feedback = service.Application("feedback")

Simple_message_service = service.MultiService()

motionservice = internet.TCPserver(port_listen, factory)
feedbackservice = internet.TCPclient(port_feedback, factory

motionservice.setServiceParent(application_listen)
