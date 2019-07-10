
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
        _default_=Pass #@UndefinedVariable
    )


def CommTypeEnum(subcon):
    return c2.Enum(subcon,
        INVALID=smc.INVALID,
        TOPIC=smc.TOPIC,
        SERVICE_REQUEST=smc.SERVICE_REQUEST,
        SERVICE_REPLY=smc.SERVICE_REPLY,
        _default_=Pass #@UndefinedVariable
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
    'header',
    #MsgTypeEnum(SM_Integer('msg_type')),
    #CommTypeEnum(SM_Integer('comm_type')),
    #ReplyTypeEnum(SM_Integer('reply_type')),
    SM_Integer("msg_type"),
    SM_Integer('comm_type'),
    SM_Integer('reply_type'),
)


def JointData(name, num):
    return c2.Array(num, SM_Float(name))

SequenceNumber = SM_Integer

TriState = SM_Integer

Time = SM_Float

ValidFields = c2.BitStruct(
    'ValidFields',
    c2.Flag('time'),
    c2.Flag('position'),
    c2.Flag('velocity'),
    c2.Flag('acceleration'),
    c2.BitsInteger('reserved', 28),
)


GenericBody = c2.Struct(
    'GenericBody',
    # use optional here, as body may be zero-length
    c2.GreedyRange(c2.Int8ub('data')),
)

GenericBody = c2.GreedyRange(c2.Int8ub('data'))

# generic simple message
GenericMessage = c2.Struct(
    'GenericMessage',
    Header,
    c2.Renamed('body', GenericBody),
    c2.Terminated
)


PingBody = c2.Struct(
    'PingBody',
    JointData('joint_data', 10)
)

Ping = c2.Struct(
    'Ping',
    Header,
    c2.Renamed('body', PingBody),
    c2.Terminated
)


JointPositionBody = c2.Struct(
    'JointPositionBody',
    SequenceNumber('seq_nr'),
    JointData('joint_data', 10),
)

JointPosition = c2.Struct(
    'JointPosition',
    Header,
    c2.Renamed('body', JointPositionBody),
    c2.Terminated
)


JointTrajectoryPointBody = c2.Struct(
    'JointTrajectoryPointBody',
    SequenceNumber('seq_nr'),
    JointData('joint_data', 10),
    SM_Float('velocity'),
    SM_Float('duration'),
)

JointTrajectoryPoint = c2.Struct(
    'JointTrajectoryPoint',
    Header,
    c2.Renamed('body', JointTrajectoryPointBody),
    c2.Terminated
)


RobotStatusBody = c2.Struct(
    'RobotStatusBody',
    TriState('drives_powered'),
    TriState('e_stopped'),
    SM_Integer('error_code'),
    TriState('in_error'),
    TriState('in_motion'),
    TriState('mode'),
    TriState('motion_possible'),
)

RobotStatus = c2.Struct(
    'RobotStatus',
    Header,
    c2.Renamed('body', RobotStatusBody),
    c2.Terminated
)


JointTrajectoryPointFullBody = c2.Struct(
    'JointTrajectoryPointFullBody',
    SM_Integer('robot_id'),
    SequenceNumber('seq_nr'),
    c2.Renamed('valid_fields', ValidFields),
    Time('time'),
    JointData('positions', 10),
    JointData('velocities', 10),
    JointData('accelerations', 10),
)

JointTrajectoryPointFull = c2.Struct(
    'JointTrajectoryPointFull',
    Header,
    c2.Renamed('body', JointTrajectoryPointFullBody),
    c2.Terminated
)


JointFeedbackBody = c2.Struct(
    'JointFeedbackBody',
    SM_Integer('robot_id'),
    c2.Renamed('valid_fields', ValidFields),
    Time('time'),
    JointData('positions', 10),
    JointData('velocities', 10),
    JointData('accelerations', 10),
)

JointFeedback = c2.Struct(
    'JointFeedback',
    Header,
    c2.Renamed('body', JointFeedbackBody),
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
    'SimpleMessage',
    Header,
    c2.Switch(
        'body',
        lambda ctx: ctx.header.msg_type,
        msg_type_body_map,
        default = GenericBody
    ),
    c2.Terminated
)
