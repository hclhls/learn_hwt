#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.defs import BIT

class Bit(Unit):
    
    def _declr(self):
        self.a        = Signal(BIT)
        self.b        = Signal(BIT)
        self.c        = Signal(BIT)._m()

    def _impl(self):
        self.c(self.a & self.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(Bit(), serializer_cls=HwtSerializer))
    print(to_rtl_str(Bit(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Bit(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(Bit(), serializer_cls=SystemCSerializer))
