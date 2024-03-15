#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, CodeBlock
from hwt.interfaces.std import Signal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class NopValOptimizedOut(Unit):

    def _declr(self):
        self.a = Signal()
        self.b = Signal()
        self.c = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        r = self._reg("r")
        CodeBlock(
            If(self.b,
               r(self.a),
            ),
            self.c(self.a),
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(NopValOptimizedOut(), serializer_cls=HwtSerializer))
    print(to_rtl_str(NopValOptimizedOut(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(NopValOptimizedOut(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(NopValOptimizedOut(), serializer_cls=SystemCSerializer))
