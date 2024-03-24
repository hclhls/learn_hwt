#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal

class serv_mem_if(Unit):
    def _config(self):
        self.WITH_CSR   = Param(1)
        self.W          = Param(1)
        self.B          = Param(self.W-1)

    def _declr(self):
        W = self.W
        B = self.B
        self.i_clk = Clk()
        
        with self._associated(clk=self.i_clk):  
            # State
            self.i_bytecnt = VectSignal(2)
            self.i_lsb = VectSignal(2)
            self.o_byte_valid = Signal()._m()
            self.o_misalign = Signal()._m()
            # Control
            self.i_signed = Signal()
            self.i_word = Signal()
            self.i_half = Signal()
            # MDU
            self.i_mdu_op = Signal()
            # Data
            self.i_bufreg2_q = VectSignal(W)
            self.o_rd = VectSignal(W)._m()
            # External interface
            self.o_wb_sel = VectSignal(4)._m()
   
        self._make_association()

    def _impl(self):
        W = self.W
        B = self.B

        self.clk = self.i_clk
        
        i_bytecnt,i_lsb,o_byte_valid,o_misalign,i_signed,i_word,i_half,i_mdu_op,i_bufreg2_q,o_rd,o_wb_sel=\
            self.i_bytecnt,self.i_lsb,self.o_byte_valid,self.o_misalign,\
            self.i_signed,self.i_word,self.i_half,\
            self.i_mdu_op,\
            self.i_bufreg2_q,\
            self.o_rd,\
            self.o_wb_sel
        
        signbit = self._reg("signbit")

        """
            Before a store operation, the data to be written needs to be shifted into
            place. Depending on the address alignment, we need to shift different
            amounts. One formula for calculating this is to say that we shift when
            i_lsb + i_bytecnt < 4. Unfortunately, the synthesis tools don't seem to be
            clever enough so the hideous expression below is used to achieve the same
            thing in a more optimal way.
        """

        o_byte_valid(
            (~i_lsb[0] & ~i_lsb[1])         |
            (~i_bytecnt[0] & ~i_bytecnt[1]) |
            (~i_bytecnt[1] & ~i_lsb[1])     |
            (~i_bytecnt[1] & ~i_lsb[0])     |
            (~i_bytecnt[0] & ~i_lsb[1])     )

        dat_valid = self._sig("dat_valid")
        dat_valid(
	        i_mdu_op |
	        i_word |
	        (i_bytecnt._eq(0)) |
	        (i_half & ~i_bytecnt[1]))

        o_rd(dat_valid._ternary(i_bufreg2_q , replicate(W, i_signed & signbit)));

        o_wb_sel[3]((i_lsb._eq(0b11)) | i_word | (i_half & i_lsb[1]))
        o_wb_sel[2]((i_lsb._eq(0b10)) | i_word)
        o_wb_sel[1]((i_lsb._eq(0b01)) | i_word | (i_half & ~i_lsb[1]))
        o_wb_sel[0]((i_lsb._eq(0b00)))

        If(dat_valid,
           signbit(i_bufreg2_q[B])
        )
   
        """
            mem_misalign is checked after the init stage to decide whether to do a data
            bus transaction or go to the trap state. It is only guaranteed to be correct
            at this time
        """
        with_csr = self._sig("with_csr")
        with_csr(self.WITH_CSR)
        o_misalign(with_csr & ((i_lsb[0] & (i_word | i_half)) | (i_lsb[1] & i_word)))

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_mem_if(), serializer_cls=VerilogSerializer))
    