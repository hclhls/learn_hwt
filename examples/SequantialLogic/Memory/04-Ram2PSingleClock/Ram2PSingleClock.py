#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClk
from hwtLib.mem.ram import RamSingleClock
from hwt.synthesizer.hObjList import HObjList

class Ram2PSingleClock(Unit):
    
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(16)
        self.PORT_CNT   = Param(2)
        self.HAS_BE     = Param(False)
        self.MAX_BLOCK_DATA_WIDTH = Param(None)
        self.INIT_DATA = Param(None)

    def _declr(self):
        self.addr    = HObjList([Signal(Bits(8)) for _ in range(2)])
        self.din     = HObjList([Signal(Bits(16)) for _ in range(2)])
        self.dout    = HObjList([Signal(Bits(16))._m() for _ in range(2)])
        self.en      = HObjList([Signal() for _ in range(2)])
        self.we      = HObjList([Signal() for _ in range(2)])
        addClkRstn(self)

        with self._paramsShared():
            self.ram = RamSingleClock()

    def _impl(self):
        
        addr, din, dout, en, we, ram =  self.addr, \
                                        self.din, \
                                        self.dout, \
                                        self.en, \
                                        self.we, \
                                        self.ram
        
        propagateClk(self)

        for i, port in enumerate(ram.port):
            port.addr(addr[i])
            port.din(din[i])
            port.en(en[i])
            port.we(we[i])
            dout[i](port.dout)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Ram2PSingleClock(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Ram2PSingleClock(), serializer_cls=VerilogSerializer))
