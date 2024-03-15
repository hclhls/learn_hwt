#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Switch
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class WithoutDefaultCase(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.u2 = Bits(2)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.d  = Signal(self.u8)
        self.s  = Signal(self.u2)
        self.e  = Signal(self.u8)._m()
        
    def _impl(self):
        
        Switch(self.s
        ).Case(0b00,
            self.e  (self.a)
        ).Case(0b01,
            self.e  (self.b)
        ).Case(0b10,
            self.e  (self.c)
        ).Case(0b11,
            self.e  (self.d)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(WithoutDefaultCase(), serializer_cls=HwtSerializer))
    print(to_rtl_str(WithoutDefaultCase(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(WithoutDefaultCase(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(WithoutDefaultCase(), serializer_cls=SystemCSerializer))
