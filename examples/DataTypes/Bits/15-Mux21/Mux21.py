#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.defs import BIT

class Mux21(Unit):
    
    def _declr(self):
        self.a        = VectSignal(8)
        self.b        = VectSignal(8)
        self.s        = Signal()
        self.c        = VectSignal(8)._m()

    def _impl(self):
        self.c(self.s._ternary(self.a, self.b))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Mux21(), serializer_cls=HwtSerializer))
    print(to_rtl_str(Mux21(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Mux21(), serializer_cls=VerilogSerializer))
