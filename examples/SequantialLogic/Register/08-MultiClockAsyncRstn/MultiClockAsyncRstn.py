#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal,  Clk, Rst_n
from hwt.hdl.types.bits import Bits

def add_reg(domain, reg, in_statement, def_val=0):
    return If(domain["rst"]._isOn(),
        reg(def_val)
    ).Elif(domain["clk"]._onRisingEdge(),
        reg(in_statement)
    )

class MultiClockAsyncRstn(Unit):
    
    def _declr(self):
        self.a        = Signal()
        self.c        = Signal()._m()
        self.i_clk    = Clk()
        self.i_rstn   = Rst_n()
        self.o_clk    = Clk()
        self.o_rstn   = Rst_n()

    def _impl(self):
        c_reg0 = self._sig(name="c_reg0")
        c_reg1 = self._sig(name="c_reg1")
        c_reg2 = self._sig(name="c_reg2")
        
        i_domain={"clk":self.i_clk, "rst": self.i_rstn}
        o_domain={"clk":self.o_clk, "rst": self.o_rstn}

        add_reg(i_domain, c_reg0, self.a, 0)
        add_reg(o_domain, c_reg1, c_reg0, 0)
        add_reg(o_domain, c_reg2, c_reg1, 0)

        self.c(c_reg2)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(MultiClockAsyncRstn(), serializer_cls=HwtSerializer))
    print(to_rtl_str(MultiClockAsyncRstn(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(MultiClockAsyncRstn(), serializer_cls=VerilogSerializer))
