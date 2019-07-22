#!/usr/bin/env python

from __future__ import print_function

from sys import stdout
from twisted.internet import interfaces, reactor, task, defer, protocol
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
import construct as c2
import simple_message as sm
from twisted.protocols.basic import LineReceiver



class feedbackPublisher(Protocol):
    def __init__(self):
        self.lc = task.LoopingCall(self.FeedbackMessage)
        self.lc1 = task.LoopingCall(self.StatusMessage)
        self.data = {}

    def connectionMade(self):
        print('Connection made from {}'.format(self.transport.getPeer()))
        self.lc.start(0.5)
        self.lc1.start(3.0)
        print("starting feedback")

    def connectionLost(self, reason):
        print('Connection lost from {}'.format(self.transport.getPeer()))
        self.lc.stop()
        self.lc1.stop()
        print("Stopping feedback")

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
        Header=dict(msg_type=10, comm_type=1, reply_type=0),
        body=dict(robot_id=0,valid_fields=0x02,time=0,
        positions=[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6,0.0,0.0,0.0,0.0],
        velocities=[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6,0.0,0.0,0.0,0.0],
        accelerations=[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6,0.0,0.0,0.0,0.0]),
        )
        feedback_data = SimpleMessage.build(msg)
        #print(feedback_data)
        data_len = c2.Int32sl.build(len(feedback_data))
        #print('sending feedback')
        self.transport.write(data_len + feedback_data)

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
                #print(status_data)
                data_len = c2.Int32sl.build(len(status_data))
                #print('sending status')
                self.transport.write(data_len + status_data)

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
