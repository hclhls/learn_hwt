#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal
from hwt.interfaces.utils import propagateClk
from hwt.math import log2ceil

class serv_rf_ram(Unit):
    def _config(s):
        s.width          = Param(2) 
        s.csr_regs       = Param(4)
        s.depth          = Param(32*(32+s.csr_regs)//s.width)
        s.SERV_CLEAR_RAM = Param(1)

    def _declr(s):
        s.i_clk = Clk()

        with s._associated(clk=s.i_clk):
            s.i_waddr   = VectSignal(log2ceil(s.depth))
            s.i_wdata   = VectSignal(s.width)
            s.i_wen     = Signal()
            s.i_raddr   = VectSignal(log2ceil(s.depth))
            s.i_ren     = Signal()
            s.o_rdata   = VectSignal(s.width)._m()
    
        s._make_association()

    def _impl(s):
        s.clk = s.i_clk
        propagateClk(s)

        if s.SERV_CLEAR_RAM==0:
            memory  = s._sig("memory", dtype=Bits(s.width)[s.depth])
        else:
            memory  = s._sig("memory", dtype=Bits(s.width)[s.depth], def_val=[0]*s.depth)

        rdata = s._reg("rdata", dtype=Bits(s.width))

        If(s.i_clk._onRisingEdge(),
            If(s.i_wen,
                memory[s.i_waddr](s.i_wdata),
            )
        )

        rdata(s.i_ren._ternary(memory[s.i_raddr], None))
	
        """ 
        Reads from reg x0 needs to return 0
        Check that the part of the read address corresponding to the register
        is zero and gate the output
        width LSB of reg index $clog2(width)
        2     4                1
        4     3                2
        8     2                3
        16    1                4
        32    0                5
        """

        regzero = s._reg("regzero")

        regzero(s.i_raddr[log2ceil(s.depth):5-log2ceil(s.width)]._eq(0))

        s.o_rdata(rdata & ~replicate(s.width,regzero))

        
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_rf_ram(), serializer_cls=VerilogSerializer))
    