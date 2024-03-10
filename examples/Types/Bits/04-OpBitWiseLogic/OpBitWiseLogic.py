#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpBitWiseLogic(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))
        self.a_and_b = Signal(Bits(self.D_W))._m()
        self.a_or_b  = Signal(Bits(self.D_W))._m()
        self.a_xor_b = Signal(Bits(self.D_W))._m()
        self.not_a   = Signal(Bits(self.D_W))._m()

    def _impl(self):
        
        self.a_and_b(self.a & self.b)
        self.a_or_b (self.a | self.b)
        self.a_xor_b(self.a ^ self.b)
        self.not_a  (~self.a)


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpBitWiseLogic(), serializer_cls=HwtSerializer))
    print(to_rtl_str(OpBitWiseLogic(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(OpBitWiseLogic(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(OpBitWiseLogic(), serializer_cls=SystemCSerializer))
