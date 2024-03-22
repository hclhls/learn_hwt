#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, HandshakeSync
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class HandshakeSyncSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = HandshakeSync()._m()
        
        addClkRstn(self)

    def _impl(self):
        self.vld_reg  = self._reg(name="vld_reg", dtype=Bits(1), def_val=0)

        self.hs.vld(self.vld_reg)

        If(self.hs.rd._isOn(),
            self.vld_reg(0)
        ).Else(
            self.vld_reg(1)
        )

@serializeParamsUniq
class HandshakeSyncDst(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = HandshakeSync()
        self.target_reached = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        self.rev_cnt    = self._reg(name="rev_cnt", dtype=Bits(self.DATA_WIDTH), def_val=0)
        self.target_reg = self._reg(name="target_reg", dtype=Bits(1), def_val=0)

        self.target_reached(self.target_reg)

        CodeBlock(
            self.target_reg(0),
            If(self.hs.vld._isOn(),
                self.hs.rd(1),
                self.rev_cnt(self.rev_cnt+1),
                If(self.rev_cnt._eq(self.TARGET),
                    self.target_reg(1)
                )
            ).Else(
                self.hs.rd(0)
            )
        )


class HandshakeSyncDemo(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.target_reached = Signal()._m()

        with self._paramsShared():
            self.src = HandshakeSyncSrc()
            self.dst = HandshakeSyncDst()

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

    print(to_rtl_str(HandshakeSyncDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(HandshakeSyncDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(HandshakeSyncDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(HandshakeSyncDemo(), serializer_cls=SystemCSerializer))
