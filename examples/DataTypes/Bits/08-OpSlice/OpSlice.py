#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Concat
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpSlice(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))._m()
        self.b       = Signal(Bits(self.D_W))._m()
        self.c       = Signal(Bits(self.D_W*2))


    def _impl(self):
        self.a(self.c[self.D_W*2:self.D_W])
        self.b(self.c[self.D_W:])
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpSlice(), serializer_cls=HwtSerializer))
    print(to_rtl_str(OpSlice(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(OpSlice(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(OpSlice(), serializer_cls=SystemCSerializer))
