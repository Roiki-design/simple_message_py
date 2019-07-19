#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Simple Message feedback publisher. The server waits for connection and then starts publishing roboto feedback information.
"""

from __future__ import print_function

from sys import stdout
from twisted.python.log import startLogging
from twisted.internet import interfaces, reactor, task, defer, protocol
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint
import construct as c2
import simple_message as sm
from twisted.protocols.basic import LineReceiver



class feedbackPublisher(Protocol):
    def __init__(self):
        self.lc = task.LoopingCall(self.StatusMessage)


    def connectionMade(self):
        print('Connection made from {}'.format(self.transport.getPeer()))
        self.lc.start(5.0)

    def connectionLost(self, reason):
        print('Connection lost from {}'.format(self.transport.getPeer()))
        self.lc.stop()



    def dataReceived(self, data):
        print("connect")
        print(data)

    def StatusMessage(self):

            StatusMessage = c2.Struct(
                'Header' / c2.Struct(
                    'msg_type' / c2.Int32sl,
                    'comm_type' / c2.Int32sl,
                    'reply_type' / c2.Int32sl,
                ),
                'body' / c2.Struct(
                    'drives_powered' / c2.Int32sl,
                    'e_stopped' / c2.Int32sl,
                    'error_code' / c2.Int32sl,
                    'in_error' / c2.Int32sl,
                    'in_motion' / c2.Int32sl,
                    'mode' / c2.Int32sl,
                    'motion_possible' / c2.Int32sl
                ),
                c2.Terminated
            )

            msg = dict(
            Header=dict(msg_type=13, comm_type=1, reply_type=0),
            body=dict(drives_powered=1,e_stopped=0,error_code=0, in_error=0,in_motion=0,mode=2, motion_possible=1))
            status_data = StatusMessage.build(msg)
            print(status_data)
            data_len = c2.Int32sl.build(len(status_data))
            print('sending status')
            self.transport.write(data_len + status_data)

class feedbackfactory(Factory):
    protocol = feedbackPublisher



startLogging(stdout)
endpoint=TCP4ClientEndpoint(reactor, 'localhost', 11000)
endpoint.connect(feedbackfactory())
reactor.run()
