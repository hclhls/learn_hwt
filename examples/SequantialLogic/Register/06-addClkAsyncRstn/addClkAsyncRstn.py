#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk, Rst_n
from hwt.interfaces.utils import addClkRstn, propagateClkRst
from hwt.hdl.types.bits import Bits

def add_domain(domain, reg, in_statement, def_val=0):
    return If(domain["rst"]._isOn(),
        reg(def_val)
    ).Elif(domain["rst"]._onRisingEdge(),
        reg(in_statement)
    )

class addClkAsyncRstn(Unit):
    def _declr(self):
        self.u8       = Bits(8)
        self.a        = Signal(self.u8)
        self.c        = Signal(self.u8)._m()
        self.clk      = Clk()
        self.rst_n    = Rst_n()

    def _impl(self):
        clk_domain = {"clk": self.clk, "rst": self.rst_n}

        c_reg = self._sig(name="c_reg", dtype=self.u8, def_val=False)
        add_domain(clk_domain, c_reg, self.a, 0)
        
        self.c(c_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(addClkAsyncRstn(), serializer_cls=HwtSerializer))
    print(to_rtl_str(addClkAsyncRstn(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(addClkAsyncRstn(), serializer_cls=VerilogSerializer))
