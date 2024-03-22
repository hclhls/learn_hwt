#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, ReqDoneSync
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class ReqDoneSyncSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = ReqDoneSync()._m()
        
        self.done = Signal()._m()

        addClkRstn(self)

    def _impl(self):
        self.req_reg  = self._reg(name="reg_reg",  dtype=Bits(1), def_val=0)
        self.req_wait = self._reg(name="req_wait", dtype=Bits(self.DATA_WIDTH), def_val=(1<<self.DATA_WIDTH)-1)

        self.done(self.hs.done)
        self.hs.req(self.req_reg)

        If(self.hs.done._isOn(),
            self.req_wait((1<<self.DATA_WIDTH)-1),
            self.req_reg(0)
        ).Elif(self.req_wait._eq(0),
            self.req_reg(1)
        ).Else(
            self.req_wait(self.req_wait-1)
        )

@serializeParamsUniq
class ReqDoneSyncDst(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = ReqDoneSync()
        addClkRstn(self)

    def _impl(self):
        self.done_cnt = self._reg(name="done_cnt", dtype=Bits(self.DATA_WIDTH), def_val=(1<<self.DATA_WIDTH)-1)

        CodeBlock(
            self.hs.done(0),
            If(self.hs.req._isOn(),
                If(self.done_cnt._eq(0),
                    self.hs.done(1)
                ).Else(
                    self.done_cnt(self.done_cnt-1)
                )   
            )
        )

class ReqDoneSyncDemo(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.done = Signal()._m()

        with self._paramsShared():
            self.src = ReqDoneSyncSrc()
            self.dst = ReqDoneSyncDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.done(self.src.done)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(ReqDoneSyncDemo(), serializer_cls=HwtSerializer))
    print(to_rtl_str(ReqDoneSyncDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(ReqDoneSyncDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(ReqDoneSyncDemo(), serializer_cls=SystemCSerializer))
