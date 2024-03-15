#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.bits import Bits
from hwt.synthesizer.hObjList import HObjList
from hwt.serializer.mode import serializeParamsUniq

@serializeParamsUniq
class SubModule(Unit):
    def _declr(self):
        self.i0 = Signal()
        self.i1 = Signal()
        self.o  = Signal()._m()

    def _impl(self):
        self.o(self.i0 & self.i1)

@serializeParamsUniq
class WithSubModule(Unit):
    def _config(self):
        self.D_W = Param(4)

    def _declr(self):
        self.a  = VectSignal(self.D_W)
        self.b  = VectSignal(self.D_W)
        self.c  = VectSignal(self.D_W)._m()      

        self.add21 = HObjList([
           SubModule() for _ in range(self.D_W)
        ])

    def _impl(self):
        
        for idx, item in enumerate(self.c):
            self.add21[idx].i0(self.a[idx])
            self.add21[idx].i1(self.b[idx])
            item(self.add21[idx].o)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(WithSubModule(), serializer_cls=HwtSerializer))
    print(to_rtl_str(WithSubModule(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(WithSubModule(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(WithSubModule(), serializer_cls=SystemCSerializer))
