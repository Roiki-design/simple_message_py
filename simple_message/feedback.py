#!/usr/bin/env python

from __future__ import print_function

from sys import stdout
from twisted.python.log import startLogging
from twisted.internet import interfaces, reactor, task, defer, protocol
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
import construct as c2
import simple_message as sm
from twisted.protocols.basic import LineReceiver



class feedbackPublisher(Protocol):
    def __init__(self):
        self.lc = task.LoopingCall(self.FeedbackMessage)
        self.data = {}

    def connectionMade(self):
        print('Connection made from {}'.format(self.transport.getPeer()))
        self.lc.start(2.0)

    def connectionLost(self, reason):
        print('Connection lost from {}'.format(self.transport.getPeer()))
        self.lc.stop()

    def dataReceived(self, data):
        print("connect")
        print(data)

    def FeedbackMessage(self):
        joint_1 = 0.0
        joint_2 = 0.0
        joint_3 = 0.0
        joint_4 = 0.0
        joint_5 = 0.0
        joint_6 = 0.0

        SimpleMessage = c2.Struct(
            'Header' / c2.Struct(
                'msg_type' / c2.Int32sl,
                'comm_type' / c2.Int32sl,
                'reply_type' / c2.Int32sl,
            ),
            'body' / c2.Struct(
                'robot_id' / c2.Int32sl,
                'valid_fields'/ c2.Int32sl,
                'time' / c2.Float32b,
                'positions' / c2.Float32b[10],
                'velocities' / c2.Float32b[10],
                'accelerations' / c2.Float32b[10],
            ),
            c2.Terminated
        )
        msg = dict(
        Header=dict(msg_type=15, comm_type=1, reply_type=0),
        body=dict(robot_id=0,valid_fields=0x02,time=0,
        positions=[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6,0.0,0.0,0.0,0.0],
        velocities=[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6,0.0,0.0,0.0,0.0],
        accelerations=[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6,0.0,0.0,0.0,0.0]),
        )
        feedback_data = SimpleMessage.build(msg)
        #print(feedback_data)
        data_len = c2.Int32sl.build(len(feedback_data))
        print('sending feedback')
        self.transport.write(data_len + feedback_data)


    def jointMessage(self):


        JointMessage = c2.Struct(
            'Header' / c2.Struct(
                'msg_type' / c2.Int32sl,
                'comm_type' / c2.Int32sl,
                'reply_type' / c2.Int32sl,
            ),
            'body' / c2.Struct(
                'SequenceNumber' / c2.Int32sl,
                'Joint_data'/c2.Float32b[10],
                'velocity' / c2.Int32sl,
                'duration' / c2.Int32sl,
            ),
            c2.Terminated
        )

class feedbackfactory(Factory):
    protocol = feedbackPublisher
