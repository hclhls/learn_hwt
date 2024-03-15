#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal

class Assign(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()._m()
        self.c       = Signal()._m()        

    def _impl(self):
        
        self.b(self.a)
        self.c(0)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(Assign(), serializer_cls=HwtSerializer))
    print(to_rtl_str(Assign(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Assign(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(Assign(), serializer_cls=SystemCSerializer))
