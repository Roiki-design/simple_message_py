
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

from twisted.internet import task, protocol, defer

import simple_message as sm
import construct as c2


class IncompleteMessageException(Exception):
    """
    There is currently not enough data for a complete message to be consumed.
    """


# TODO: use python logging infrastructure
def logdebug(msg, *args):
    print(msg % (args))
def loginfo(msg, *args):
    print(msg % (args))
def logerr(msg, *args):
    print(msg % (args))
def logwarn(msg, *args):
    print(msg % (args))


class SimpleMessageProtocol(protocol.Protocol):

    _S_INIT         = 0
    _S_PKT_LEN_RCVD = 1
    _S_MSG_RCVD     = 2

    def __init__(self):
        self._state = self._S_INIT
        self._remainingData = ""
        self._num_msgs_seen = 0
        self._expected_pkt_len = 0
        self._callbacks = {}

    def connectionMade(self):
        logdebug("Connected")
        if self.factory.disable_nagle:
            self.transport.setTcpNoDelay(enabled=True)

    def connectionLost(self, reason):
        logdebug("Connection lost: %s", reason)
        # handle disconnects properly:
        #  https://jml.io/pages/how-to-disconnect-in-twisted-really.html

    def sendMsg(self, msg):
        """
        Send a message in binary form to remote.
        This method takes care of all protocol specific aspects of sending
        a message (such as the prefix).
        """
        data = sm.SimpleMessage.build(msg)
        data_len = sm.PktLen(None).build(len(data))
        self.transport.write(data_len + data)

    def registerCallback(self, msg_type, cb, single_shot=False):
        """
        Register a callback to be executed whenever a message of type 'msg_type'
        is received. The callback will receive the entire message when invoked.
        """
        logdebug("registerCallback: registering '%s' for body type 0x%X",
            cb.__name__, msg_type)
        self._callbacks.setdefault(msg_type, []).append((cb, single_shot))

    def purgeCallbacks(self, msg_type):
        """
        Remove all callbacks registered for the given 'msg_type'.
        """
        self._callbacks.pop(msg_type, None)

    def purgeAllCallbacks(self):
        """
        Remove all registered callbacks for all pkt types.
        """
        self._body_type_callbacks.clear()

    def dataReceived(self, data):
        self._remainingData += data
        while self._remainingData:
            try:
                self._consumeData()
            except IncompleteMessageException:
                # try again later (when we get more data)
                break

    def _consumeData(self):
        if self._state == self._S_INIT:
            self._consumePktLen()
        if self._state == self._S_PKT_LEN_RCVD:
            self._consumeMsg()
        if self._state == self._S_MSG_RCVD:
            self._dispatchMsg()

    _LEN_PKT_LEN = sm.PktLen.sizeof()

    def _consumePktLen(self):
        if (len(self._remainingData) < self._LEN_PKT_LEN):
            raise IncompleteMessageException()
        self._processPktLen()

    def _processPktLen(self):
        # get field data from buffer
        data = self._remainingData[:self._LEN_PKT_LEN]
        self._remainingData = self._remainingData[self._LEN_PKT_LEN:]

        # deserialise
        self._expected_pkt_len = sm.PktLen(None).parse(data)

        # transition
        self._state = self._S_PKT_LEN_RCVD

    def _consumeMsg(self):
        if (len(self._remainingData) < self._expected_pkt_len):
            raise IncompleteMessageException()
        self._processMsg()

    def _processMsg(self):
        # get data from buffer
        data = self._remainingData[:self._expected_pkt_len]
        self._remainingData = self._remainingData[self._expected_pkt_len:]

        # deserialise
        self._msg = sm.SimpleMessage.parse(data)

        # transition
        self._num_msgs_seen += 1
        self._expected_pkt_len = 0
        self._state = self._S_MSG_RCVD

    def _dispatchMsg(self):
        # call registered callbacks based on msg type
        cbs = self._callbacks.get(self._msg.header.msg_type, [])
        for (cb, single_shot) in cbs:
            try:
                # remove it first, then execute
                if single_shot:
                    cbs.remove((cb, single_shot))
                cb(self._msg)
            except Exception as e:
                logwarn("Exception caught executing callback '%s': %s",
                    cb.__name__, e)

        # transition
        self._state = self._S_INIT


class SimpleMessageFactory(protocol.Factory):
    protocol = SimpleMessageProtocol

    def __init__(self, disable_nagle=False):
        self.disable_nagle = disable_nagle
