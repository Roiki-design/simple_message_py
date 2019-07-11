#!/usr/bin/env python

from scapy.all import*

class Header(packet):
    name = "Header"
    fields_desc=[SignedIntField("msg_type",10),
                 SignedIntField("comm_type",1),
                 SignedIntField("reply_type",0)

    ]



class SimpleMessaData(Packet):
    name = "DATA"
    fields_desc = [ VarLenQField("len", None, "data"),
                    StrLenField("data", "", "len") ]
