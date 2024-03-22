#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal
from hwt.hdl.types.array import HArray

class LUTSin(Unit):
   
    def _declr(self):
        self.idx  = Signal(Bits(4))
        self.data = Signal(Bits(8))._m()

    def _impl(self):
    
        lut = self._sig(name="lut", dtype=HArray(Bits(8,signed=True),16), 
                                    def_val=[int(math.sin(i*math.pi*2/16)*127+0.5) for i in range(16)])

        self.data(lut[self.idx])


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(LUTSin(), serializer_cls=HwtSerializer))
    print(to_rtl_str(LUTSin(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(LUTSin(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(LUTSin(), serializer_cls=SystemCSerializer))
