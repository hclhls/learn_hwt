#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class BitsConst(Unit):
    
    def _declr(self):
        self.a        = Signal(Bits(8))
        self.b        = Signal(Bits(8))._m()
        
    def _impl(self):
        one   = Bits(8).from_py(1)
        two   = Bits(8).from_py(0b00000010)
        three = Bits(8).from_py(0o003)
        four  = Bits(8).from_py(0x04)
        self.b(self.a + one + two + three + four)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(BitsConst(), serializer_cls=HwtSerializer))
    print(to_rtl_str(BitsConst(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(BitsConst(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(BitsConst(), serializer_cls=SystemCSerializer))
