#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk, Rst_n
from hwt.interfaces.utils import propagateClkRstn

class Rst_nSubmodule(Unit):
    
    def _declr(self):
        self.clk = Clk()
    
        with self._associated(clk=self.clk):
            self.rst_n = Rst_n()
            with self._associated(rst=self.rst_n):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self._make_association()

    def _impl(self):
        b_reg = self._reg(name="b_reg", def_val=0)

        b_reg(self.a)
        self.b(b_reg)
        

class Rst_nDemo(Unit):
    
    def _declr(self):
        self.clk = Clk()

        with self._associated(clk=self.clk):
            self.rst_n = Rst_n()
            with self._associated(rst=self.rst_n):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self.sub = Rst_nSubmodule()

        self._make_association()

    def _impl(self):
        
        propagateClkRstn(self)

        self.sub.a(self.a)
        self.b(self.sub.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(Rst_nDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(Rst_nDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Rst_nDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(Rst_nDemo(), serializer_cls=SystemCSerializer))
