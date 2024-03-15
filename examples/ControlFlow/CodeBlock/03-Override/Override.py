#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, CodeBlock
from hwt.interfaces.std import Signal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class Override(Unit):

    def _declr(self):
        self.a = Signal()
        self.b = Signal()
        self.c = Signal()._m()

    def _impl(self):
        # results in c = a
        CodeBlock(
            If(self.b,
               self.c(0),
            ),
            self.c(self.a),
        )


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(Override(), serializer_cls=HwtSerializer))
    print(to_rtl_str(Override(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Override(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(Override(), serializer_cls=SystemCSerializer))
