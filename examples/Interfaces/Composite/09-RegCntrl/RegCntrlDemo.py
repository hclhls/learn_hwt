#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, VldSynced, RegCntrl
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class RegCntrlSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        self.INTERVAL   = Param(8)
        self.TARGET     = Param(11)

    def _declr(self):
        with self._paramsShared():
            self.hs = RegCntrl()._m()
        
        self.target_reached = Signal()._m()

        addClkRstn(self)

    def _impl(self):
        self.cnt_int = self._reg(name="cnt_int", dtype=Bits(4), def_val=self.INTERVAL-1)
        self.cnt_val = self._reg(name="cnt_val", dtype=Bits(4), def_val=0)
        
        If(self.hs.din._eq(self.TARGET),
            self.target_reached(1)
        ).Else(
            self.target_reached(0)
        )

        If(self.cnt_int._eq(0),
            self.cnt_int(self.INTERVAL-1),
            self.hs.dout.vld(1),
            self.hs.dout.data(self.cnt_val),
            self.cnt_val(self.cnt_val+1)
        ).Else(
            self.cnt_int(self.cnt_int-1),
            self.hs.dout.vld(0),
            self.hs.dout.data(0)
        )

@serializeParamsUniq
class RegCntrlDst(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)
        

    def _declr(self):
        with self._paramsShared():
            self.hs = RegCntrl()

        addClkRstn(self)

    def _impl(self):
        
        If(self.hs.dout.vld._isOn(),
            self.hs.din(self.hs.dout.data)
        ).Else(
            self.hs.din(0)
        )


class RegCntrlDemo(Unit):
    def _config(self):
        self.INTERVAL   = Param(8)
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.target_reached = Signal()._m()

        with self._paramsShared():
            self.src = RegCntrlSrc()
            self.dst = RegCntrlDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.target_reached(self.src.target_reached)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(RegCntrlDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(RegCntrlDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(RegCntrlDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(RegCntrlDemo(), serializer_cls=SystemCSerializer))
