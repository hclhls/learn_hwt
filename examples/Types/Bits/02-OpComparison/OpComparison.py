#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class OpComparison(Unit):
    
    def _declr(self):
        self.a       = Signal(Bits(8))
        self.b       = Signal(Bits(8))
        self.a_eq_b  = Signal()._m()
        self.a_ne_b  = Signal()._m()
        self.a_ge_b  = Signal()._m()
        self.a_gt_b  = Signal()._m()
        self.a_le_b  = Signal()._m()
        self.a_lt_b  = Signal()._m()
        
    def _impl(self):
        self.a_eq_b(self.a._eq(self.b))
        self.a_ne_b(self.a != self.b)
        self.a_ge_b(self.a >= self.b)
        self.a_gt_b(self.a >  self.b)
        self.a_le_b(self.a <= self.b)
        self.a_lt_b(self.a <  self.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpComparison(), serializer_cls=HwtSerializer))
    print(to_rtl_str(OpComparison(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(OpComparison(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(OpComparison(), serializer_cls=SystemCSerializer))
