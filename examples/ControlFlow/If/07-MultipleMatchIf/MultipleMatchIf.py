#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import SwitchLogic, Switch, In
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.bits import Bits

class MultipleMatch(Unit):

    def _declr(self):
        self.s  = Signal(Bits(4))
        self.a  = Signal(Bits(8))
        self.b  = Signal(Bits(8))
        self.c  = Signal(Bits(8))
        self.d  = Signal(Bits(8))._m()
    
    def _impl(self):

        SwitchLogic(
            [(In(self.s,[0b0010, 0b0001]), self.d(self.b)),
             (In(self.s,[0b0100, 0b1000]), self.d(self.c))
             ],
             self.d(self.a)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(MultipleMatch(), serializer_cls=HwtSerializer))
    print(to_rtl_str(MultipleMatch(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(MultipleMatch(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(MultipleMatch(), serializer_cls=SystemCSerializer))
