#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Concat, replicate
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class BitsObj(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)._m()
        self.c  = Signal(self.u8)._m()
        
    def _impl(self):
        a, b, c = self.a, self.b, self.c
        one  = self.u8.from_py(1)
        
        b(a + one)
        c(a + one*2)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(BitsObj(), serializer_cls=HwtSerializer))
    print(to_rtl_str(BitsObj(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(BitsObj(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(BitsObj(), serializer_cls=SystemCSerializer))
