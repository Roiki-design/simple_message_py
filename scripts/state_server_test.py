#!/usr/bin/env python

# Copyright (c) 2016, G.A. vd. Hoorn
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import time
import math
import sys
import array as ar
sys.path.append('/Users/joonasadm/Github/simple_message_py/')
from twisted.internet import reactor, error
from twisted.internet.endpoints import TCP4ClientEndpoint, TCP4ServerEndpoint
from twisted.python import log
from simple_message import protocol, StandardSocketPorts, StandardMsgTypes


class SimpleMessageClient(object):
    def __init__(self):
        self._prot = None

    def onRobotStatus(self, msg):
        if (msg.body.in_error):
            print ("Robot error: {}".format(msg.body.error_code))

    def onJointPosition(self, msg):
        print ("joint0: {:6.3f} rad ({:6.3f} deg)".format(
            msg.body.joint_data[0],
            math.degrees(msg.body.joint_data[0])))

    def onJointPosition_ss(self, msg):
        print ("SINGLE_SHOT: joint0: {:6.3f} rad ({:6.3f} deg)".format(
            msg.body.joint_data[0],
            math.degrees(msg.body.joint_data[0])))



def onStateEpConnect(prot, client):
    prot.registerCallback(StandardMsgTypes.STATUS, client.onRobotStatus)
    prot.registerCallback(StandardMsgTypes.JOINT_POSITION, client.onJointPosition)
    prot.registerCallback(StandardMsgTypes.JOINT_POSITION, client.onJointPosition_ss, single_shot=True)
    client._prot = prot


def onStateEpConnectErr(err):
    sys.stderr.write("Unable to connect to host, {} ".format( err))
    err.trap(error.ConnectError)
    reactor.callLater(1, reactor.stop)

def main():
    DEFAULT_TIMEOUT=2.0
    log.startLogging(sys.stdout)
    log.msg('starting')
    SimProto = protocol.SimpleMessageProtocol
    # parse command line opts
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
        dest='verbose',help='Be verbose')
    args = parser.parse_args()

    # create endpoint
    trajData= TCP4ServerEndpoint(reactor=reactor, port=StandardSocketPorts.MOTION, backlog=50)
    feedback= TCP4ServerEndpoint(reactor=reactor, port=StandardSocketPorts.STATE)
    print("init")
    # Simple Message client instance for this endpoint
    client= SimpleMessageClient

    factory = protocol.SimpleMessageFactory(disable_nagle=True)
    f = feedback.listen(protocolFactory=factory)
    d = trajData.listen(protocolFactory=factory)
    print("listening motion data")
    # setup callbacks to init client instance on succesfull connection
    #d.addCallback(onStateEpConnect, client)
    #d.addErrback(onStateEpConnectErr, args.host, 11000)""
    #f.addErrback(onStateEpConnectErr)
    a = ar.array('d', [0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0])
    #nulldata =
    SimProto.sendMsg(StandardMsgTypes.JOINT_FEEDBACK, 1)
    reactor.run() #@UndefinedVariable


if __name__ == "__main__":
    main()
