#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class CombIf(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.s  = Signal()
        self.c  = Signal(self.u8)._m()
        self.d  = Signal(self.u8)._m()
        
    def _impl(self):
        
        If(self.s,
            self.c(self.b),
            self.d(self.a)
        ).Else(
            self.c(self.a),
            self.d(self.b)
        )
        
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(CombIf(), serializer_cls=HwtSerializer))
    print(to_rtl_str(CombIf(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(CombIf(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(CombIf(), serializer_cls=SystemCSerializer))
