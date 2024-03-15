#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Concat
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpConcat(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))
        self.c       = Signal(Bits(self.D_W))._m()
        self.d       = Signal(Bits(self.D_W))._m()

    def _impl(self):
        self.c(Concat(self.a[self.D_W//2:],self.b[self.D_W:self.D_W//2]))
        self.d(self.a[self.D_W:self.D_W//2]._concat(self.b[self.D_W//2:]))

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpConcat(), serializer_cls=HwtSerializer))
    print(to_rtl_str(OpConcat(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(OpConcat(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(OpConcat(), serializer_cls=SystemCSerializer))
