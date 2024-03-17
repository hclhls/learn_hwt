#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal,  Clk, Rst
from hwt.hdl.types.bits import Bits

class NoRst(Unit):
    
    def _declr(self):
        self.u8       = Bits(8)
        self.a        = Signal(self.u8)
        self.c        = Signal(self.u8)._m()
        self.clk      = Clk()

    def _impl(self):
        c_reg = self._reg(name="c_reg", dtype=self.u8, clk=self.clk)
        
        c_reg(self.a)
        self.c(c_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(NoRst(), serializer_cls=HwtSerializer))
    print(to_rtl_str(NoRst(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(NoRst(), serializer_cls=VerilogSerializer))