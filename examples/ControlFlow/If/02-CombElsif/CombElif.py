#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class CombElif(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.s  = Signal(Bits(2))
        self.d  = Signal(self.u8)._m()
        
    def _impl(self):
        
        If(self.s[0]&(~self.s[1]),
            self.d(self.b)
        ).Elif(self.s[1]&(~self.s[0]),
            self.d(self.c)
        ).Else(
            self.d(self.a)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(CombElif(), serializer_cls=HwtSerializer))
    print(to_rtl_str(CombElif(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(CombElif(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(CombElif(), serializer_cls=SystemCSerializer))
