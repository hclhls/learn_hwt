#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import rol, ror
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpRotate(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))._m()
        self.c       = Signal(Bits(self.D_W))._m()

    def _impl(self):
        self.b(rol(self.a, 1))
        self.c(ror(self.a, 2))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpRotate(), serializer_cls=HwtSerializer))
    print(to_rtl_str(OpRotate(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(OpRotate(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(OpRotate(), serializer_cls=SystemCSerializer))
