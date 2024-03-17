#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, BramPort, BramPort_withoutClk
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClk
from hwtLib.mem.ram import RamSingleClock
from hwt.synthesizer.hObjList import HObjList

class Ram1PBramPort(Unit):
    
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(16)
        self.PORT_CNT   = Param(1)
        self.HAS_BE     = Param(False)
        self.MAX_BLOCK_DATA_WIDTH = Param(None)
        self.INIT_DATA = Param(None)

    def _declr(self):
        addClkRstn(self)

        with self._paramsShared():
            self.port = BramPort_withoutClk()
            self.ram = RamSingleClock()

    def _impl(self):
        propagateClk(self)
        
        self.ram.port[0](self.port)


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Ram1PBramPort(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Ram1PBramPort(), serializer_cls=VerilogSerializer))
