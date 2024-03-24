#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.bits import Bits

class VectSignalSubmodule(Unit):
    def _config(self):
        self.D_W     = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = VectSignal(self.D_W)._m()
        self.c       = Signal(Bits(self.D_W))._m()        

    def _impl(self):
        
        self.b(self.a)
        self.c(Bits(self.D_W).from_py(0))

class VectSignalDemo(Unit):
    def _config(self):
        self.D_W     = Param(8)

    def _declr(self):
        self.a       = VectSignal(self.D_W)
        self.b       = Signal(Bits(self.D_W))._m()
        self.c       = VectSignal(self.D_W)._m()        

        with self._paramsShared():
            self.sub = VectSignalSubmodule()

    def _impl(self):
        
        self.sub.a(self.a)
        self.b(self.sub.b)
        self.c(self.sub.c)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(VectSignalDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(VectSignalDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(VectSignalDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(VectSignalDemo(), serializer_cls=SystemCSerializer))
