
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

# from
#  simple_message/include/simple_message/socket/simple_socket.h
MAX_BUFFER_SIZE = 1024


# from
#  simple_message/include/simple_message/socket/simple_socket.h
class StandardSocketPorts():
    MOTION = 11000
    SYSTEM = 11001
    STATE  = 11002
    IO     = 11003


# from
#  simple_message/include/simple_message/simple_message.h
class StandardMsgTypes():
    INVALID            = 0
    PING               = 1
    JOINT_POSITION     = 10
    JOINT              = 10
    READ_INPUT         = 20
    WRITE_OUTPUT       = 21
    JOINT_TRAJ_PT      = 11
    JOINT_TRAJ         = 12
    STATUS             = 13
    JOINT_TRAJ_PT_FULL = 14
    JOINT_FEEDBACK     = 15

    SWRI_MSG_BEGIN     = 1000
    UR_MSG_BEGIN       = 1100
    ADEPT_MSG_BEGIN    = 1200
    ABB_MSG_BEGIN      = 1300
    FANUC_MSG_BEGIN    = 1400
    MOTOMAN_MSG_BEGIN  = 2000

    ALL                = -1


# from
#  simple_message/include/simple_message/simple_message.h
class CommTypes():
    INVALID         = 0
    TOPIC           = 1
    SERVICE_REQUEST = 2
    SERVICE_REPLY   = 3


# from
#  simple_message/include/simple_message/simple_message.h
class ReplyTypes():
    INVALID_UNUSED = 0
    SUCCES         = 1
    FAILURE        = 2


# from
#  simple_message/include/simple_message/robot_status.h
class TriStates():
    UNKNOWN  = -1
    FALSE    = 0
    OFF      = 0
    DISABLED = 0
    LOW      = 0
    TRUE     = 1
    ON       = 1
    ENABLED  = 1
    HIGH     = 1


# from
#  simple_message/include/simple_message/joint_feedback.h
class ValidFieldTypes():
    TIME         = 0x01
    POSITION     = 0x02
    VELOCITY     = 0x04
    ACCELERATION = 0x08
