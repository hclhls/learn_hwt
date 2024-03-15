#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

def IfElifElse(condition0, statements, condition1, fallback0, fallback1):
    return If(condition0,
        statements
    ).Elif(condition1,
        fallback0,
    ).Else(
        fallback1
    )

class FunctionInline(Unit):

    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()
        self.s       = Signal(Bits(2))
        self.c       = Signal()._m()        

    def _impl(self):
        
        IfElifElse(self.s._eq(0b01), self.c(self.a),
               self.s._eq(0b01), self.c(self.b),
               self.c(0))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(FunctionInline(), serializer_cls=HwtSerializer))
    print(to_rtl_str(FunctionInline(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(FunctionInline(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(FunctionInline(), serializer_cls=SystemCSerializer))
