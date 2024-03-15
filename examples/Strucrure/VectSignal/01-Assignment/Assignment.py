#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, VectSignal

class Assignment(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = VectSignal(self.D_W)._m()
        self.c       = VectSignal(self.D_W//2)._m()

    def _impl(self):
        
        self.b(self.a)
        for idx, item in enumerate(self.c):
            item(~(self.a[idx*2] & self.a[idx*2+1]))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(Assignment(), serializer_cls=HwtSerializer))
    print(to_rtl_str(Assignment(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Assignment(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(Assignment(), serializer_cls=SystemCSerializer))
