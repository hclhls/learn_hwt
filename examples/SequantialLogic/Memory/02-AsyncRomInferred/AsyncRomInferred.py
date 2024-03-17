#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal,  Clk, Rst
from hwt.hdl.types.bits import Bits

class AsyncRomInferred(Unit):
    
    def _declr(self):
        self.a        = Signal(Bits(2))
        self.d        = Signal(Bits(8))._m()

    def _impl(self):
        rom = self._sig("rom", Bits(8)[4], def_val=[i for i in range(4)])

        self.d(rom[self.a])

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(AsyncRomInferred(), serializer_cls=HwtSerializer))
    print(to_rtl_str(AsyncRomInferred(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(AsyncRomInferred(), serializer_cls=VerilogSerializer))
