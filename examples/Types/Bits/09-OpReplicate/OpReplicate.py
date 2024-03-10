#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Concat, replicate
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpReplicate(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W+2))._m()


    def _impl(self):
        self.b(Concat(replicate(2, self.a[self.D_W-1]),self.a))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpReplicate(), serializer_cls=HwtSerializer))
    print(to_rtl_str(OpReplicate(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(OpReplicate(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(OpReplicate(), serializer_cls=SystemCSerializer))
