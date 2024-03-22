#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, Handshaked
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class HandshakedSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = Handshaked()._m()
        
        addClkRstn(self)

    def _impl(self):
        self.vld_reg  = self._reg(name="vld_reg", dtype=Bits(1), def_val=0)
        self.cnt_val  = self._reg(name="cnt_val", dtype=Bits(4), def_val=0)

        self.hs.data(self.cnt_val)
        self.hs.vld(self.vld_reg)

        If(self.hs.rd._isOn(),
            self.cnt_val(self.cnt_val+1),
            self.vld_reg(0)
        ).Else(
            self.vld_reg(1)
        )

@serializeParamsUniq
class HandshakedDst(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = Handshaked()
        self.target_reached = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        self.target_reg = self._reg(name="target_reg", dtype=Bits(1), def_val=0)

        self.target_reached(self.target_reg)

        CodeBlock(
            self.target_reg(0),
            If(self.hs.vld._isOn(),
                self.hs.rd(1),
                If(self.hs.data._eq(self.TARGET),
                    self.target_reg(1)
                )
            ).Else(
                self.hs.rd(0)
            )
        )


class HandshakedDemo(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.target_reached = Signal()._m()

        with self._paramsShared():
            self.src = HandshakedSrc()
            self.dst = HandshakedDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.target_reached(self.dst.target_reached)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(HandshakedDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(HandshakedDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(HandshakedDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(HandshakedDemo(), serializer_cls=SystemCSerializer))
