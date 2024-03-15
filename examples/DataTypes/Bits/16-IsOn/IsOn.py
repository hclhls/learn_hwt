#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn

class IsOn(Unit):
    
    def _declr(self):
        self.u8       = Bits(8)
        self.a        = Signal(self.u8)
        self.b        = Signal(self.u8)
        self.s        = Signal()
        self.c        = Signal(self.u8)._m()
        addClkRstn(self)

    def _impl(self):
        c_reg = self._reg(name="c_reg", dtype=self.u8, def_val=0)
        
        print(type(self.b._vec()))
        self.c(c_reg)
        If(self.s._isOn(),
            c_reg(self.a)
        ).Else(
            c_reg(self.b._vec()._reversed())
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(IsOn(), serializer_cls=HwtSerializer))
    print(to_rtl_str(IsOn(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(IsOn(), serializer_cls=VerilogSerializer))
