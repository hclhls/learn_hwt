#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Concat, replicate
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwtLib.types.ctypes import uint32_t, int32_t, uint16_t, int16_t, uint8_t, int8_t


class CType(Unit):
    
    def _declr(self):
        self.a        = Signal(uint8_t)
        self.a_signed = Signal(int8_t)
        self.b        = Signal(uint16_t)._m()
        self.b_signed = Signal(int16_t)._m()
        self.c        = Signal(uint32_t)._m()
        self.c_signed = Signal(int32_t)._m()
        

    def _impl(self):
        self.b(Concat(self.a,self.a))
        self.b_signed(Concat(self.a_signed,self.a))
        self.c(Concat(self.b,self.b))
        self.c_signed(Concat(self.b_signed,self.b))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(CType(), serializer_cls=HwtSerializer))
    print(to_rtl_str(CType(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(CType(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(CType(), serializer_cls=SystemCSerializer))
