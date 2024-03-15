#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Switch
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class WithDefaultCase(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.u3 = Bits(3)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.s  = Signal(self.u3)
        self.d  = Signal(self.u8)._m()
        
    def _impl(self):
        
        Switch(self.s
        ).Case(0b001,
            self.d  (self.a)
        ).Case(0b010,
            self.d  (self.b)
        ).Case(0b100,
            self.d  (self.c)
        ).Default(
            self.d  (0)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(WithDefaultCase(), serializer_cls=HwtSerializer))
    print(to_rtl_str(WithDefaultCase(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(WithDefaultCase(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(WithDefaultCase(), serializer_cls=SystemCSerializer))
