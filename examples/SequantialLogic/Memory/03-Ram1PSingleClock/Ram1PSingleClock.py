#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClk
from hwtLib.mem.ram import RamSingleClock

class Ram1PSingleClock(Unit):
    
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(32)
        self.PORT_CNT   = Param(1)
        self.HAS_BE     = Param(False)
        self.MAX_BLOCK_DATA_WIDTH = Param(None)
        self.INIT_DATA = Param(None)

    def _declr(self):
        self.addr    = Signal(Bits(8))
        self.din     = Signal(Bits(32))
        self.dout    = Signal(Bits(32))._m()
        self.en      = Signal()
        self.we      = Signal()
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

        ram.port_0.addr(addr)
        ram.port_0.din(din)
        ram.port_0.en(en)
        ram.port_0.we(we)
        dout(ram.port_0.dout)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Ram1PSingleClock(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(Ram1PSingleClock(), serializer_cls=VerilogSerializer))
