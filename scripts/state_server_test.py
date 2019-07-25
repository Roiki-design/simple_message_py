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

from twisted.internet import reactor, error, defer
from twisted.internet.endpoints import TCP4ServerEndpoint
from simple_message import protocol, StandardSocketPorts, StandardMsgTypes
from simple_message import feedback as fb

# create servers and sart them.
def main():

    # create endpoint
    state_ep = TCP4ServerEndpoint(reactor, 11000)
    feedback = TCP4ServerEndpoint(reactor, 11002)

    # Simple Message client instance for this endpoint
    client = SimpleMessageServer()


    feedbackfactory = fb.feedbackfactory()
    factory = protocol.SimpleMessageFactory(disable_nagle=True)
    state_ep.listen(factory)
    feedback.listen(feedbackfactory)
    print("listening..")
    reactor.run()


if __name__ == "__main__":
    main()
