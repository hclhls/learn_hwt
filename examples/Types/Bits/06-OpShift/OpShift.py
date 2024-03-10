#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpShift(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W, signed=True))
        self.c       = Signal(Bits(self.D_W))._m()
        self.d       = Signal(Bits(self.D_W))._m()
        self.e       = Signal(Bits(self.D_W))._m()
        self.f       = Signal(Bits(self.D_W))._m()
        self.g       = Signal(Bits(self.D_W))._m()

    def _impl(self):
        self.c(self.a >> 1)
        self.d(self.a << 2)
        self.e(self.b >> 3)
        self.f((self.b._reinterpret_cast(Bits(self.D_W+3, signed=True)) >> 3)._reinterpret_cast(Bits(self.D_W)))
        self.g(self.b << 4)


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpShift(), serializer_cls=HwtSerializer))
    print(to_rtl_str(OpShift(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(OpShift(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(OpShift(), serializer_cls=SystemCSerializer))
