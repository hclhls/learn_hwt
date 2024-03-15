#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class NestedIf(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.d  = Signal(self.u8)
        self.s  = Signal(Bits(2))
        self.e  = Signal(self.u8)._m()
        self.f  = Signal(self.u8)._m()

    def _impl(self):
        
        If(self.s[0],
            self.e(self.b),
            If(self.s[1],
                self.f(self.c)
            ).Else(
                self.f(self.d)
            )
        ).Else(
            self.e(self.a),
            If(self.s[1],
                self.f(self.d)
            ).Else(
                self.f(self.e)
            )
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(NestedIf(), serializer_cls=HwtSerializer))
    print(to_rtl_str(NestedIf(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(NestedIf(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(NestedIf(), serializer_cls=SystemCSerializer))
