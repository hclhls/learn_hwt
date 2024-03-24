#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk, Rst
from hwt.interfaces.utils import propagateClkRst

class RstSubmodule(Unit):
    
    def _declr(self):
        self.clk     = Clk()
    
        with self._associated(clk=self.clk):
            self.rst     = Rst()
            with self._associated(rst=self.rst):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self._make_association()

    def _impl(self):
        b_reg = self._reg(name="b_reg", clk=self.clk, def_val=0)

        b_reg(self.a)
        self.b(b_reg)
        

class RstDemo(Unit):
    
    def _declr(self):
        self.clk = Clk()

        with self._associated(clk=self.clk):
            self.rst     = Rst()
            with self._associated(rst=self.rst):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self.sub = RstSubmodule()

        self._make_association()

    def _impl(self):
        
        propagateClkRst(self)

        self.sub.a(self.a)
        self.b(self.sub.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(RstDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(RstDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(RstDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(RstDemo(), serializer_cls=SystemCSerializer))
