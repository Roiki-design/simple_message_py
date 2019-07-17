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

from twisted.internet import reactor, error
from twisted.internet.endpoints import TCP4ServerEndpoint

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


def onStateEpConnectErr(err, port):
    sys.stderr.write("Unable to connect to tcp {}  {}".format( port, err))
    err.trap(error.ConnectError)
    reactor.callLater(1, reactor.stop)


def main():
    DEFAULT_TIMEOUT=2.0

    # parse command line opts
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
        dest='verbose',help='Be verbose')
    parser.add_argument('--port', type=int, default=StandardSocketPorts.MOTION,
        help='TCP port to connect to (default: %(default)s)')


    args = parser.parse_args()

    # create endpoint
    state_ep = TCP4ServerEndpoint(reactor=reactor,
                port=)


    # Simple Message client instance for this endpoint
    client = SimpleMessageClient()



    factory = protocol.SimpleMessageFactory(disable_nagle=True)
    d = state_ep.listen(protocolFactory=factory)
    print("listening..")
    # setup callbacks to init client instance on succesfull connection
    d.addCallback(onStateEpConnect, client)
    d.addErrback(onStateEpConnectErr, args.port)

    reactor.run()


if __name__ == "__main__":
    main()
