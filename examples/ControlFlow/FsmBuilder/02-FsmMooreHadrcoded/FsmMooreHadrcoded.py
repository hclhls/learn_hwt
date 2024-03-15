#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import FsmBuilder, Switch, If
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.interfaces.std import Signal, VectSignal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class FsmMooreHadrcoded(Unit):
    
    def _declr(self):
        addClkRstn(self)
        self.a = Signal()
        self.b = Signal()
        self.dout = VectSignal(3)._m()

    def _impl(self):
        a = self.a
        b = self.b
        out = self.dout

        st = self._reg("st", Bits(3), 1)

        If(st._eq(1),
            If(a & b,
                st(3)
            ).Elif(b,
                st(2)
            )
        ).Elif(st._eq(2),
            If(a & b,
               st(3)
            ).Elif(a,
                st(1)
            )
        ).Elif(st._eq(3),
            If(a & ~b,
               st(1)
            ).Elif(~a & b,
                st(2)
            )
        ).Else(
            st(1)
        )

        Switch(st)\
        .Case(1,
            out(1)
        ).Case(2,
            out(2)
        ).Case(3,
            out(3)
        ).Default(
            out(None)
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(FsmMooreHadrcoded(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(FsmMooreHadrcoded(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(FsmMooreHadrcoded(), serializer_cls=SystemCSerializer))