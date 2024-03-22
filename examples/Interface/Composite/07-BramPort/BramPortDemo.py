#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import FsmBuilder, If, Switch, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, VectSignal, BramPort, Clk, Rst_n
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.interfaces.utils import addClkRstn, propagateClkRstn
from hwt.math import log2ceil

@serializeParamsUniq
class BramPortSrc(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)
        self.HAS_R      = Param(True)
        self.HAS_W      = Param(True)
        self.HAS_BE     = Param(True)

    def _declr(self):
        assert self.HAS_R and self.HAS_W, "has to have both read and write part"
        assert self.HAS_BE, "has to have byte-enable"
        
        with self._paramsShared():
            self.hs = BramPort()._m()

        self.read_phase = Signal()._m()
        self.data       = VectSignal(self.DATA_WIDTH)._m()
        
        addClkRstn(self)

    def _impl(self):
        BYTE_NUM  = self.DATA_WIDTH//8
        BYTE_BITS = log2ceil(BYTE_NUM)
        
        self.addr_reg = self._reg(name="addr_reg", dtype=Bits(self.ADDR_WIDTH+BYTE_BITS),def_val=0)
        self.data_reg = self._reg(name="data_reg", dtype=Bits(self.DATA_WIDTH),def_val=(1<<self.DATA_WIDTH)-1)
        stT = HEnum("st_t", ["write", "read"])

        self.hs.clk(self.clk)

        st = FsmBuilder(self, stT)\
        .Trans(stT.write,
            (self.addr_reg._eq((1<<self.ADDR_WIDTH)-1), stT.read)
        ).Trans(stT.read,
            (self.addr_reg._eq((1<<self.ADDR_WIDTH)-1), stT.write)
        ).stateReg

        CodeBlock(
            self.hs.we(0),
            self.hs.en(0),
            self.read_phase(0),
            self.data(self.hs.dout),
            Switch(st
            ).Case(stT.write,
                self.hs.en(1),
                self.addr_reg(self.addr_reg+1),
                self.data_reg(self.data_reg-1),
                self.hs.addr(self.addr_reg[:BYTE_BITS]),
                self.hs.din(self.data_reg),
                Switch(self.addr_reg[BYTE_BITS:]).add_cases([(i, self.hs.we(1<<i)) for i in range(BYTE_NUM)])
            ).Case(stT.read,
                self.hs.en(1),
                self.read_phase(1),
                self.addr_reg(self.addr_reg+1),
                self.hs.addr(self.addr_reg[:BYTE_BITS])
            )
        )
@serializeParamsUniq
class BramPortDst(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)
        self.HAS_R      = Param(True)
        self.HAS_W      = Param(True)
        self.HAS_BE     = Param(True)

    def _declr(self):
        assert self.HAS_R and self.HAS_W, "has to have both read and write part"
        assert self.HAS_BE, "has to have byte-enable"
        
        with self._paramsShared():
            self.hs = BramPort()
            
    def _impl(self):
        BYTE_NUM  = self.DATA_WIDTH//8
        
        self.mem = self._sig(name="mem", dtype=Bits(self.DATA_WIDTH)[1<<self.ADDR_WIDTH])
    
        If(self.hs.clk._onRisingEdge(),
            self.hs.dout(Bits(self.DATA_WIDTH).from_py(None)),
            If(self.hs.en._eq(1),
                If(self.hs.we._eq(0),
                    self.hs.dout(self.mem[self.hs.addr])
                ).Else(
                    [If(self.hs.we[i]._eq(1),
                        self.mem[self.hs.addr][8*(i+1):8*i](self.hs.din[8*(i+1):8*i])) for i in range(BYTE_NUM)]
                )
            )
        )
        
class BramPortDemo(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(6)
        self.DATA_WIDTH = Param(32)
        self.HAS_R      = Param(True)
        self.HAS_W      = Param(True)
        self.HAS_BE     = Param(True)

    def _declr(self):
        addClkRstn(self)

        self.read_phase = Signal()._m()
        self.dout = VectSignal(self.DATA_WIDTH)._m()

        with self._paramsShared():
            self.src = BramPortSrc()
            self.dst = BramPortDst()

    def _impl(self):
        
        propagateClkRstn(self)
        self.dst.hs(self.src.hs)
        self.read_phase(self.src.read_phase)
        self.dout(self.src.data)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(BramPortDemo(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(BramPortDemo(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(BramPortDemo(), serializer_cls=SystemCSerializer))
