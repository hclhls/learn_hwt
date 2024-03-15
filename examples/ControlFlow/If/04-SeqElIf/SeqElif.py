#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn

class SeqElif(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.s  = Signal(Bits(2))
        self.d  = Signal(self.u8)._m()
        addClkRstn(self)

    def _impl(self):
        d_reg = self._reg(name="d_reg", dtype=self.u8, def_val=0)

        If(self.s[0],
            d_reg(self.b)
        ).Elif(self.s[1],
            d_reg(self.c)
        )
        self.d(d_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(SeqElif(), serializer_cls=HwtSerializer))
    print(to_rtl_str(SeqElif(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(SeqElif(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(SeqElif(), serializer_cls=SystemCSerializer))
