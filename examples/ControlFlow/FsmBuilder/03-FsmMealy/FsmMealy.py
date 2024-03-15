#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import FsmBuilder, Switch, If
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.interfaces.std import Signal, VectSignal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class FsmMealy(Unit):

    def _declr(self):
        addClkRstn(self)
        self.a = Signal()
        self.b = Signal()
        self.dout = VectSignal(3)._m()

    def _impl(self):
        # :note: stT member names are colliding with port names and thus
        #     they will be renamed in HDL
        stT = HEnum("st_t", ["a", "b", "aAndB"])

        a = self.a
        b = self.b
        out = self.dout

        st = FsmBuilder(self, stT)\
        .Trans(stT.a,
            (a & b, stT.aAndB),
            (b, stT.b)
        ).Trans(stT.b,
            (a & b, stT.aAndB),
            (a, stT.a)
        ).Trans(stT.aAndB,
            (a & ~b, stT.a),
            (~a & b, stT.b),
        ).stateReg

        If(st._eq(stT.a) & b,
            out(1)
        ).Elif(st._eq(stT.b) & a,
            out(2) 
        ).Elif(st._eq(stT.aAndB) & (~a),
            out(3)
        ).Elif(st._eq(stT.aAndB) & (~b),
            out(4)
        ).Else(
            out(0)
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(FsmMealy(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(FsmMealy(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(FsmMealy(), serializer_cls=SystemCSerializer))