#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import FsmBuilder, If, Switch, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, VectSignal, FifoWriter, FifoReader
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn
from hwt.synthesizer.rtlLevel.constants import NOT_SPECIFIED
from hwt.math import log2ceil
from hwtLib.mem.fifo import Fifo

@serializeParamsUniq
class FifoSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        self.DEPTH = Param(0)
        self.EXPORT_SIZE = Param(False)
        self.EXPORT_SPACE = Param(False)
        self.INIT_DATA: tuple = Param(())
        self.INIT_DATA_FIRST_WORD = Param(NOT_SPECIFIED)

        self.DURATION = Param(4)

    def _declr(self):
        
        with self._paramsShared():
            self.hs = FifoWriter()._m()

        addClkRstn(self)

    def _impl(self):
        self.wd_cnt  = self._reg(name="wd_cnt",  dtype=Bits(log2ceil(self.DURATION)), def_val=0)
        self.dat_reg = self._reg(name="dat_reg", dtype=Bits(self.DATA_WIDTH), def_val=0)
        
        CodeBlock(
            self.hs.en(0),
            self.hs.data(0), 
            If(~self.hs.wait._isOn(),
                self.wd_cnt(self.wd_cnt+1),
                If(self.wd_cnt._eq(self.DURATION-1),
                    self.hs.en(1),
                    self.hs.data(self.dat_reg),
                    self.dat_reg(self.dat_reg+1)
                )
            )
        )

@serializeParamsUniq
class FifoDst(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        self.DEPTH = Param(0)
        self.EXPORT_SIZE = Param(False)
        self.EXPORT_SPACE = Param(False)
        self.INIT_DATA: tuple = Param(())
        self.INIT_DATA_FIRST_WORD = Param(NOT_SPECIFIED)

    def _declr(self):
        
        with self._paramsShared():
            self.hs = FifoReader()
        
        self.dout = VectSignal(self.DATA_WIDTH)._m()
        self.vld  = Signal()._m()

        addClkRstn(self)

    def _impl(self):
        
        CodeBlock(
            self.hs.en(0),
            self.vld(0),
            self.dout(0),
            If(~self.hs.wait._isOn(),
                self.hs.en(1),
                self.vld(1),
                self.dout(self.hs.data)
            )
        )
        
class FifiWriterFifoReaderDemo(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        self.DEPTH = Param(8)
        self.EXPORT_SIZE = Param(False)
        self.EXPORT_SPACE = Param(False)
        self.INIT_DATA: tuple = Param(())
        self.INIT_DATA_FIRST_WORD = Param(NOT_SPECIFIED)

    def _declr(self):
        addClkRstn(self)

        self.dout = VectSignal(self.DATA_WIDTH)._m()
        self.vld  = Signal()._m()

        with self._paramsShared():
            self.src  = FifoSrc()
            self.fifo = Fifo()
            self.dst  = FifoDst()

        self.src.DURATION = 4

    def _impl(self):
        
        propagateClkRstn(self)
        
        self.fifo.dataIn(self.src.hs)
        self.dst.hs(self.fifo.dataOut)
        self.vld(self.dst.vld)
        self.dout(self.dst.dout)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(FifiWriterFifoReaderDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(FifiWriterFifoReaderDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(FifiWriterFifoReaderDemo(), serializer_cls=SystemCSerializer))
