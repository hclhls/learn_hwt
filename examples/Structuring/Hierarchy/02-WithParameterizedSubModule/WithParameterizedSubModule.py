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
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.i0 = VectSignal(self.D_W)
        self.i1 = VectSignal(self.D_W)
        self.o  = VectSignal(self.D_W)._m()

    def _impl(self):
        self.o(self.i0 & self.i1)

@serializeParamsUniq
class WithParameterizedSubModule(Unit):
    def _config(self):
        self.D_W = Param(4)

    def _declr(self):
        self.a  = VectSignal(self.D_W)
        self.b  = VectSignal(self.D_W)
        self.c  = VectSignal(self.D_W)._m()      

        self.add21 = HObjList([])
        for _ in range(self.D_W//2):
            self.add21.append(SubModule())
            self.add21[-1].D_W = self.D_W//2

    def _impl(self):        
        for idx, subm in enumerate(self.add21):
            subm.i0(self.a[idx*2+2:idx*2])
            subm.i1(self.b[idx*2+2:idx*2])
            self.c[idx*2+2:idx*2](subm.o)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(WithParameterizedSubModule(), serializer_cls=HwtSerializer))
    print(to_rtl_str(WithParameterizedSubModule(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(WithParameterizedSubModule(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(WithParameterizedSubModule(), serializer_cls=SystemCSerializer))
