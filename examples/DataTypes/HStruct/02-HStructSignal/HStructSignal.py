#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.hdl.types.struct import HStruct
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal
from hwt.hdl.types.defs import BIT

class HStructSignal(Unit):
    
    def _declr(self):
        self.a = Signal(Bits(2))
        self.b = Signal(Bits(2))._m()

    def _impl(self):
        c = self._sig(dtype=HStruct((BIT,"b0"), (BIT,"b1"),), 
                      name="temp") 
        
        c.b0(self.a[0])
        c.b1(self.a[1])
        
        self.b[0](c.b0 & c.b1)
        self.b[1](c.b0 | c.b1)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(HStructSignal(), serializer_cls=HwtSerializer))
    print(to_rtl_str(HStructSignal(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(HStructSignal(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(HStructSignal(), serializer_cls=SystemCSerializer))
