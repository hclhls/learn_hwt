#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from hwt.code import If, Switch
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class ConditionalCodeGeneration(Unit):

    def _config(self):
        self.D_W     = Param(int(sys.argv[1]))

    def _declr(self):
        
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))
        self.s       = Signal(Bits(2))
        self.c       = Signal(Bits(self.D_W))._m()        

    def _impl(self):
        
        SWAP_AB = True if int(sys.argv[1])==1 else False

        if SWAP_AB:
            If(self.s._eq(0b01),
                self.c(self.b)
            ).Elif(self.s._eq(0b10),
                self.c(self.a)
            ).Else(
                self.c(0)
            )
        else:
            If(self.s._eq(0b01),
                self.c(self.a)
            ).Elif(self.s._eq(0b10),
                self.c(self.b)
            ).Else(
                self.c(0)
            )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(ConditionalCodeGeneration(), serializer_cls=HwtSerializer))
    print(to_rtl_str(ConditionalCodeGeneration(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(ConditionalCodeGeneration(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(ConditionalCodeGeneration(), serializer_cls=SystemCSerializer))
