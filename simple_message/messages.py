
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

# NOTE: the 'pkt_length' field from the 'prefix' msg part is not modelled as
#       part of these message structures


from .constants import \
    StandardMsgTypes as smt, \
    CommTypes        as smc, \
    ReplyTypes       as smr

import construct as c2




# TODO: deal with little- and big-endian switching
SM_Bool = c2.Int32sl
SM_Float = c2.Float32l
SM_Integer = c2.Int32sl



def MsgTypeEnum(subcon):
    return c2.Enum(subcon,
        PING=smt.PING,
        JOINT_POSITION=smt.JOINT_POSITION,
        JOINT=smt.JOINT,
        READ_INPUT=smt.READ_INPUT,
        WRITE_OUTPUT=smt.WRITE_OUTPUT,
        JOINT_TRAJ_PT=smt.JOINT_TRAJ_PT,
        JOINT_TRAJ=smt.JOINT_TRAJ,
        STATUS=smt.STATUS,
        JOINT_TRAJ_PT_FULL=smt.JOINT_TRAJ_PT_FULL,
        JOINT_FEEDBACK=smt.JOINT_FEEDBACK,
        _default_=Pass
    )


def CommTypeEnum(subcon):
    return c2.Enum(subcon,
        INVALID=smc.INVALID,
        TOPIC=smc.TOPIC,
        SERVICE_REQUEST=smc.SERVICE_REQUEST,
        SERVICE_REPLY=smc.SERVICE_REPLY,
        _default_=Pass
    )


def ReplyTypeEnum(subcon):
    return c2.Enum(subcon,
        INVALID_UNUSED=smr.INVALID_UNUSED,
        SUCCES=smr.SUCCES,
        FAILURE=smr.FAILURE,
        _default_=Pass
    )






PktLen = SM_Integer

Header = c2.Struct(
    #MsgTypeEnum(SM_Integer('msg_type')),
    #CommTypeEnum(SM_Integer('comm_type')),
    #ReplyTypeEnum(SM_Integer('reply_type')),
    'msg_type' / SM_Integer ,
    'comm_type' / SM_Integer,
    'reply_type' / SM_Integer,
)


def JointData(num):
    return  c2.Float32l[num]

SequenceNumber = SM_Integer

TriState = SM_Integer

Time = SM_Float

ValidFields = c2.BitStruct(
    'time' / c2.Flag,
    'position' /  c2.Flag,
    'velocity' / c2.Flag,
    'accelerations' / c2.Flag,
    'reserved' / c2.BitsInteger(28)
)


GenericBody = c2.Struct(
    # use optional here, as body may be zero-length
    c2.GreedyRange('data' / c2.Int8ub)
)

GenericBody = c2.GreedyRange('data' / c2.Int8ub)

# generic simple message
GenericMessage = c2.Struct(
    'Header'/ Header,
    'body' / c2.Renamed(GenericBody),
    c2.Terminated
)


PingBody = c2.Struct(
    'joint_data'/ JointData(10)
)

Ping = c2.Struct(
    'Header'/ Header,
    'body' / c2.Renamed(PingBody),
    c2.Terminated
)


JointPositionBody = c2.Struct(
    'seq_nr' / SequenceNumber ,
    'joint_data'/ JointData(10)
)

JointPosition = c2.Struct(
    'Header'/ Header,
    'body' / c2.Renamed(JointPositionBody),
    c2.Terminated
)


JointTrajectoryPointBody = c2.Struct(
    'seq_nr' / SequenceNumber ,
    'joint_data'/  JointData(10),
    'velocity' / SM_Float,
    'duration' / SM_Float,
)

JointTrajectoryPoint = c2.Struct(
    'Header'/ Header,
    'body' / c2.Renamed(JointTrajectoryPointBody),
    c2.Terminated
)


RobotStatusBody = c2.Struct(
    'drives_powered' / TriState,
    'e_stopped' / TriState,
    'error_code' / SM_Integer,
    'in_error' / TriState,
    'in_motion' / TriState,
    'mode' / TriState,
    'motion_possible' / TriState
)

RobotStatus = c2.Struct(
    'Header'/ Header,
    'body' / c2.Renamed(RobotStatusBody),
    c2.Terminated,
)


JointTrajectoryPointFullBody = c2.Struct(
    'robot_id' / SM_Integer,
    'seq_nr' / SequenceNumber ,
    'valid_fields' / c2.Renamed(ValidFields),
    'time' / Time,
    'positions' / JointData( 10),
    'velocities' / JointData( 10),
    'accelerations' / JointData( 10),
)

JointTrajectoryPointFull = c2.Struct(
    'Header'/ Header,
    'body' / c2.Renamed(JointTrajectoryPointFullBody),
    c2.Terminated
)


JointFeedbackBody = c2.Struct(
    'robot_id' / SM_Integer,
    'valid_fields'/ ValidFields,
    'time' / Time,
    'positions' / JointData( 10),
    'velocities' / JointData( 10),
    'accelerations' / JointData( 10),
)

JointFeedback = c2.Struct(
    'Header'/ Header,
    'body' / c2.Renamed(JointFeedbackBody),
    c2.Terminated
)


msg_type_body_map = {
    smt.PING               : PingBody,
    smt.JOINT_POSITION     : JointPositionBody,
    #smt.JOINT              : ,
    #smt.READ_INPUT         : ,
    #smt.WRITE_OUTPUT       : ,
    smt.JOINT_TRAJ_PT      : JointTrajectoryPointBody,
    #smt.JOINT_TRAJ         : ,
    smt.STATUS             : RobotStatusBody,
    smt.JOINT_TRAJ_PT_FULL : JointTrajectoryPointFullBody,
    smt.JOINT_FEEDBACK     : JointFeedbackBody,
}


SimpleMessage = c2.Struct(
    'Header'/ Header,
    c2.Switch(lambda ctx: ctx.header.msg_type, msg_type_body_map, default = GenericBody),
    c2.Terminated
)
