#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.param import Param
from hwt.interfaces.std import Signal,  Clk, Rst_n
from hwt.hdl.types.bits import Bits
from hwtLib.clocking.cdc import SignalCdcBuilder

class CdcBuilder(Unit):
    def _config(self):
        self.NO_CDC_STAGES = Param(2)

    def _declr(self):
        
        self.i_clk    = Clk()
        self.o_clk    = Clk()

        with self._paramsShared():
            with self._associated(clk=self.i_clk):
                self.i_rstn = Rst_n()
                with self._associated(rst=self.i_rstn):
                    self.a  = Signal()

            with self._associated(clk=self.o_clk):
                self.o_rstn = Rst_n()
                with self._associated(rst=self.o_rstn):
                    self.c  = Signal()._m()

    def _impl(self):
        c_reg = self._reg(name="c_reg", def_val=0, clk=self.i_clk, rst=self.i_rstn)
        c_reg(self.a)
        
        i_domain={"clk":self.i_clk, "rst": self.i_rstn}
        o_domain={"clk":self.o_clk, "rst": self.o_rstn}

        cdc_builder = SignalCdcBuilder(
            c_reg,
            (i_domain["clk"], i_domain["rst"]),
            (o_domain["clk"], o_domain["rst"]),
            reg_init_val=0)
        
        for _ in range(self.NO_CDC_STAGES):
            cdc_builder.add_out_reg()
        
        self.c(cdc_builder.path[-1])

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(CdcBuilder(), serializer_cls=HwtSerializer))
    print(to_rtl_str(CdcBuilder(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(CdcBuilder(), serializer_cls=VerilogSerializer))
