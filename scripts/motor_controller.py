#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Simple Message feedback publisher. The server waits for connection and then starts publishing roboto feedback information.
"""
from sys import stdout
import time
from twisted.python.log import startLogging
from twisted.internet import interfaces, reactor, task, defer, protocol
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
import queue
import construct as c2
import simple_message as sm
from simple_message import protocol as p2
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall
#from PoKeys import *


class Motorcontroller(LineReceiver):

    remote_connected = False
    motors_powered = False
    Error = False

    def __init__(self):
        self.factory = factory
        self.loop = LoopingCall(self.send_to_motors)

    def connectionMade(self):
        print('Connection made from {}'.format(self.transport.getPeer()))
        if self.factory.motors.get(self.transport.getPeer()) != None:
            self.factory.motors[self.transport.getpeer()] = True
            self.loop.start(0.01)
        else:
            print("Connection not in database")

    def connectionLost(self, reason):
        print('Connection lost from {}'.format(self.transport.getPeer()))
        self.factory.motors[self.transport.getPeer()] = False
        self.loop.stop()

    def lineReceived(self):
        print("got message")

    def send_to_motors(self):
        if self.transport.getPeer() == "10.0.0.11" and self.Error==False:
            motor_functions.motor1()
        elif self.transport.getPeer() == "10.0.0.12" and self.Error==False:
            motor_functions.motor_2a()
        elif self.transport.getPeer() == "10.0.0.13" and self.Error==False:
            motor_functions.motor_2b()
        elif self.transport.getPeer() == "10.0.0.14" and self.Error==False:
            motor_functions.motor_3()
        elif self.transport.getPeer() == "10.0.0.15" and self.Error==False:
            motor_functions.motor_4()
        elif self.transport.getPeer() == "10.0.0.16" and self.Error==False:
            motor_functions.motor_5()
        elif self.transport.getPeer() == "10.0.0.17" and self.Error==False:
            motor_functions.motor_6()
        else:
            pass

class motor_functions(object):

    def motor_1(self):
        while monitoring.joint1_queue.empty() == False and p2.SimpleMessageProtocol.e_stopped != 0 :
            angle=monitoring.joint1_queue.get()
            self.transport.sendline(angle)
        else:
            pass
    def motor_2a(self):
        while monitoring.joint2_queue.empty() == False and p2.SimpleMessageProtocol.e_stopped != 0 :
            angle=monitoring.joint1_queue.get()
            self.transport.sendline(angle)
        else:
            pass
    def motor_2b(self):
        while monitoring.joint2_queue.empty() == False and p2.SimpleMessageProtocol.e_stopped != 0 :
            angle=monitoring.joint1_queue.get()
            self.transport.sendline(angle)
        else:
            pass
    def motor_3(self):
     while monitoring.joint3_queue.empty() == False and p2.SimpleMessageProtocol.e_stopped != 0 :
         angle=monitoring.joint1_queue.get()
         self.transport.sendline(angle)
     else:
        pass

    def motor_4(self):
        while monitoring.joint4_queue.empty() == False and p2.SimpleMessageProtocol.e_stopped != 0 :
            angle=monitoring.joint1_queue.get()
            self.transport.sendline(angle)
        else:
            pass

    def motor_5(self):
     while monitoring.joint5_queue.empty() == False and p2.SimpleMessageProtocol.e_stopped != 0 :
         angle=monitoring.joint1_queue.get()
         self.transport.sendline(angle)
     else:
        pass
    def motor_6(self):
     while monitoring.joint6_queue.empty() == False and p2.SimpleMessageProtocol.e_stopped != 0 :
         angle=monitoring.joint1_queue.get()
         self.transport.sendline(angle)
     else:
        pass

class monitoring():

    def __init__(self):
        self.joint1_queue = queue.Queue()
        self.joint2_queue = queue.Queue()
        self.joint3_queue = queue.Queue()
        self.joint4_queue = queue.Queue()
        self.joint5_queue = queue.Queue()
        self.joint6_queue = queue.Queue()

    def assign_to_queue():
        if any(p2.SimpleMessageProtocol.trajectoryPoint_store) != False:
            for key in p2.SimpleMessageProtocol.trajectoryPoint_store.items():
                self.joint1_queue.put(val[0])
                self.joint2_queue.put(val[1])
                self.joint3_queue.put(val[2])
                self.joint4_queue.put(val[3])
                self.joint5_queue.put(val[4])
                self.joint6_queue.put(val[5])



    while True:
        assign_to_queue()


class feedbackfactory(Factory):
    protocol = Motorcontroller
    def __init__(self):
        self.motors =	{
        "10.0.0.10": False, #Remote
        "10.0.0.11": False, #Motor1
        "10.0.0.12": False, #Motor2a
        "10.0.0.13": False, #Motor2b
        "10.0.0.14": False, #Motor3
        "10.0.0.15": False, #Motor4
        "10.0.0.16": False, #Motor5
        "10.0.0.17": False #Motor6
        #10.0.0.18: False #Track
       }

factory=feedbackfactory()


endpoint=TCP4ServerEndpoint(reactor, 15000)
endpoint.listen(feedbackfactory())
reactor.callInThread(monitoring())
reactor.run()
