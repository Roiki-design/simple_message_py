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
        self.lc = task.LoopingCall(self.FeedbackMessage) #add both feedback and status as loops to a connection
        self.lc1 = task.LoopingCall(self.StatusMessage)
        self.data = {}
        self.drives_powered = 0
        self.e_stopped = 0
        self.error_code = 0
        self.in_error = 0
        self.in_motion = 0
        self.mode = 0
        self.motion_possible = 0

    def connectionMade(self):
        print('Connection made from {}'.format(self.transport.getPeer()))
        self.lc.start(0.5)                          #Start loops on intervals
        self.lc1.start(3.0)
        print("starting feedback")

    def connectionLost(self, reason):
        print('Connection lost from {}'.format(self.transport.getPeer()))
        self.lc.stop()                          #Stop loops on disconnect
        self.lc1.stop()
        print("Stopping feedback")

    def dataReceived(self, data):
        print("connect")
        print(data)

    def FeedbackMessage(self):
        #create a feedback message we populate and send
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
                'seq_nr' / c2.Int32sl ,
                'joint_data'/ c2.Float32b[10]
            ),
            c2.Terminated
        )                                           #packa a message.
        msg = dict(
        Header=dict(msg_type=10, comm_type=1, reply_type=0),
        body=dict(seq_nr=0,joint_data=[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6,0.0,0.0,0.0,0.0]
        ))
        feedback_data = SimpleMessage.build(msg)
        #print(feedback_data)
        data_len = c2.Int32sl.build(len(feedback_data))
        #print('sending feedback')
        self.transport.write(data_len + feedback_data)

    def StatusMessage(self):
                #Create a statusmessage that we populate and send
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

                self.mode = 2
                self.drives_powered = 1
                self.motion_possible = 1

                msg = dict(
                Header=dict(msg_type=13, comm_type=1, reply_type=0),
                body=dict(drives_powered= self.drives_powered,
                e_stopped=self.e_stopped,
                error_code= self.error_code,
                in_error=self.in_error,
                in_motion=self.in_motion,
                mode=self.mode,
                motion_possible=self.motion_possible
                ))
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
