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
        self.D1_W = Param(8)
        self.D2_W = Param(8)

    def _declr(self):
        self.i0 = VectSignal(self.D1_W)
        self.i1 = VectSignal(self.D1_W)
        self.i2 = VectSignal(self.D2_W)
        self.i3 = VectSignal(self.D2_W)
        self.o0 = VectSignal(self.D1_W)._m()
        self.o1 = VectSignal(self.D2_W)._m()

    def _impl(self):
        self.o0(self.i0 & self.i1)
        self.o1(self.i3 | self.i2)

@serializeParamsUniq
class WithSharedParameterizedSubModule(Unit):
    def _config(self):
        self.D1_W = Param(4)
        self.D2_W = Param(3)

    def _declr(self):
        self.a0  = VectSignal(self.D1_W)
        self.b0  = VectSignal(self.D1_W)
        self.c0  = VectSignal(self.D1_W)._m()
        self.a1  = VectSignal(self.D2_W)
        self.b1  = VectSignal(self.D2_W)
        self.c1  = VectSignal(self.D2_W)._m()       

        with self._paramsShared():
            self.subm = SubModule()

    def _impl(self):        
        self.subm.i0(self.a0)
        self.subm.i1(self.b0)
        self.c0(self.subm.o0)
        self.subm.i2(self.a1)
        self.subm.i3(self.b1)
        self.c1(self.subm.o1)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(WithSharedParameterizedSubModule(), serializer_cls=HwtSerializer))
    print(to_rtl_str(WithSharedParameterizedSubModule(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(WithSharedParameterizedSubModule(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(WithSharedParameterizedSubModule(), serializer_cls=SystemCSerializer))
