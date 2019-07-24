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
from twisted.internet.endpoints import TCP4ServerEndpoint
import construct as c2
import simple_message as sm
from twisted.protocols.basic import LineReceiver

Motor1 =
Motor2a =
Motor2b =
Motor3 =
Motor4
Motor5
Motor6

class Motorcontroller(LineReceiver):
    def __init__(self):
        self.remote_connected = False
        self.motors_powered = False
        self.Error = False
        self.factory = factory

    def connectionMade(self):
        print('Connection made from {}'.format(self.transport.getPeer()))
        if self.factory.motors.get(self.transport.getPeer()) != None:
            self.factory.motors[self.transport.getpeer()] = True
        else:
            print("Connection not in database")

    def connectionLost(self, reason):
        print('Connection lost from {}'.format(self.transport.getPeer()))
        self.factory.motors.[self.transport.getPeer()] = False

    def lineReceived(self):
        print("got message")

    def sendMsg(self , joint):
        if monitoring.msg_recv == True:
            self.factory.motors[].transport.sendLine()

class monitoring(thread):

    def __init__(self):
        self.old_message = None
        self.joint_1 = 0.0
        self.joint_2 = 0.0
        self.joint_3 = 0.0
        self.joint_4 = 0.0
        self.joint_5 = 0.0
        self.joint_6 = 0.0
        self.msg_recv = False

    def message_monitor(self):
        message = SimpleMessageProtocol.jointMessage
        if message != self.old_message:
            self.joint_1 = message(['body']['Joint Data']['J0'])
            self.joint_2 = message(['body']['Joint Data']['J1'])
            self.joint_3 = message(['body']['Joint Data']['J2'])
            self.joint_4 = message(['body']['Joint Data']['J3'])
            self.joint_5 = message(['body']['Joint Data']['J4'])
            self.joint_6 = message(['body']['Joint Data']['J5'])
            self.old_message = message
            self.msg_recv = True
        else:
            break


class to_motors(thread):

    def send_to_motors(self):
        if msg_recv=True:
            sendLine(monitoring.joint_1)


class feedbackfactory(Factory):
    protocol = feedbackPublisher
    def __init__(self):
        self.motors =	{
        10.0.0.10: False, #Remote
        10.0.0.11: False, #Motor1
        10.0.0.12: False, #Motor2a
        10.0.0.13: False, #Motor2b
        10.0.0.14: False, #Motor3
        10.0.0.15: False, #Motor4
        10.0.0.16: False, #Motor5
        10.0.0.17: False #Motor6
       }

factory=feedbackfactory()


endpoint=TCP4ServerEndpoint(reactor, 15000)
endpoint.listen(feedbackfactory())
reactor.callInThread(monitoring())
reactor.run()
