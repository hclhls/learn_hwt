#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Switch
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class AddCases(Unit):
    
    def _declr(self):
        self.a  = Signal(Bits(24))
        self.s  = Signal(Bits(3))
        self.b  = Signal(Bits(8))._m()
        
    def _impl(self):
        
        sel_cases = [(0b001<<i, self.b(self.a[8*(i+1):8*i])) for i in range(3)]
        
        Switch(self.s
        ).add_cases(
            sel_cases
        ).Default(
            self.b  (0)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(AddCases(), serializer_cls=HwtSerializer))
    print(to_rtl_str(AddCases(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(AddCases(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(AddCases(), serializer_cls=SystemCSerializer))
