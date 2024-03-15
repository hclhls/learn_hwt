#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import SwitchLogic
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn

class SwitchLogicIf(Unit):
    
    def _declr(self):
        self.a  = Signal(Bits(32))
        self.b  = Signal(Bits(8))._m()
        self.s  = Signal(Bits(2))
        
    def _impl(self):
    
        cases = [(self.s._eq(i), self.b(self.a[8*(i+1):8*i])) for i in range(4)]

        SwitchLogic(cases)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(SwitchLogicIf(), serializer_cls=HwtSerializer))
    print(to_rtl_str(SwitchLogicIf(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(SwitchLogicIf(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(SwitchLogicIf(), serializer_cls=SystemCSerializer))
