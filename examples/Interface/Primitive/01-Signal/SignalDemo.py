#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal

class SignalSubmodule(Unit):
    
    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()._m()
        self.c       = Signal()._m()        

    def _impl(self):
        
        self.b(self.a)
        self.c(0)

class SignalDemo(Unit):
    
    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()._m()
        self.c       = Signal()._m()        

        self.sub = SignalSubmodule()

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

    print(to_rtl_str(SignalDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(SignalDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(SignalDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(SignalDemo(), serializer_cls=SystemCSerializer))
