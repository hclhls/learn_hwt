#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Switch,SwitchLogic,If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.hdl.valueUtils import isSameHVal, areSameHVals

class WildCardMatchIf(Unit):
    
    def _declr(self):
        self.a  = Signal(Bits(32))
        self.s  = Signal(Bits(3))
        self.b  = Signal(Bits(8))._m()
        
    def _impl(self):
        u3 = Bits(3)
        SwitchLogic(
            [(self.s._eq(u3.from_py(0b001, vld_mask=0b001)), self.b(self.a[8:0])),
             (self.s._eq(u3.from_py(0b010, vld_mask=0b010)), self.b(self.a[16:8])),
             (self.s._eq(u3.from_py(0b100, vld_mask=0b100)), self.b(self.a[24:16])),
             ],
             self.b(self.a[32:24])
        )
     

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(WildCardMatchIf(), serializer_cls=HwtSerializer))
    print(to_rtl_str(WildCardMatchIf(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(WildCardMatchIf(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(WildCardMatchIf(), serializer_cls=SystemCSerializer))
