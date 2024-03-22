#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.hdl.types.union import HUnion
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class HUnionValue(Unit):
    
    def _declr(self):
        self.b = Signal(Bits(2))._m()

    def _impl(self):
        hu_t = HUnion((Bits(2), "a"),
                      (Bits(2), "b"),
                     )
        hu_val = hu_t.from_py(("a",2))

        self.b(hu_val.b)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(HUnionValue(), serializer_cls=HwtSerializer))
    print(to_rtl_str(HUnionValue(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(HUnionValue(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(HUnionValue(), serializer_cls=SystemCSerializer))
