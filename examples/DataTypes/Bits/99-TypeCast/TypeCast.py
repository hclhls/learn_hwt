#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class TypeCast(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W,   signed=True))
        self.a_add_b = Signal(Bits(self.D_W+1, signed=True))._m()
        self.c       = Signal(Bits(self.D_W*2))._m()
        self.d       = Signal(Bits(self.D_W*2, signed=True))._m()

    def _impl(self):
        self.a_signed = self._sig(name="a_signed", dtype=Bits(self.D_W,   signed=True))

        self.a_signed(self.a._auto_cast(self.a_signed._dtype))

        self.a_add_b (self.a_signed._reinterpret_cast(self.a_add_b._dtype) +  self.b._reinterpret_cast(self.a_add_b._dtype))

        self.c(self.a, fit=True)
        self.d(self.b, fit=True)  

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(TypeCast(), serializer_cls=HwtSerializer))
    print(to_rtl_str(TypeCast(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(TypeCast(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(TypeCast(), serializer_cls=SystemCSerializer))
