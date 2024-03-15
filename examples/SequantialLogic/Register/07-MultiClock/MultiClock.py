#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk, Rst
from hwt.hdl.types.bits import Bits

class MultiClock(Unit):
    
    def _declr(self):
        self.a        = Signal()
        self.c        = Signal()._m()
        self.i_clk    = Clk()
        self.i_rst    = Rst()
        self.o_clk    = Clk()
        self.o_rst    = Rst()

    def _impl(self):
        c_reg0 = self._reg(name="c_reg0", def_val=0, clk=self.i_clk, rst=self.i_rst, rst_async=False)
        c_reg1 = self._reg(name="c_reg1", def_val=0, clk=self.o_clk, rst=self.o_rst, rst_async=False)
        c_reg2 = self._reg(name="c_reg2", def_val=0, clk=self.o_clk, rst=self.o_rst, rst_async=False)
        
        c_reg0(self.a)
        c_reg1(c_reg0)
        c_reg2(c_reg1)
        self.c(c_reg2)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(MultiClock(), serializer_cls=HwtSerializer))
    print(to_rtl_str(MultiClock(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(MultiClock(), serializer_cls=VerilogSerializer))
