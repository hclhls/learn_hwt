#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal

class serv_bufreg2(Unit):
    
    def _declr(self):
       
        self.i_clk = Clk()
        
        with self._associated(clk=self.i_clk):  
            # State
            self.i_en           = Signal()
            self.i_init         = Signal()
            self.i_cnt_done     = Signal()
            self.i_lsb          = VectSignal(2)
            self.i_byte_valid   = Signal()
            self.o_sh_done      = Signal()._m()
            self.o_sh_done_r    = Signal()._m()
            # Control
            self.i_op_b_sel     = Signal()
            self.i_shift_op     = Signal()
            # Data
            self.i_rs2          = Signal()
            self.i_imm          = Signal()
            self.o_op_b         = Signal()._m()
            self.o_q            = Signal()._m()
            # External
            self.o_dat          = VectSignal(32)._m()
            self.i_load         = Signal()
            self.i_dat          = VectSignal(32)
   
        self._make_association()

    def _impl(self):
        self.clk = self.i_clk
        
        i_en,i_init,i_cnt_done,i_lsb,i_byte_valid,o_sh_done,o_sh_done_r,i_op_b_sel,i_shift_op,i_rs2,i_imm,o_op_b,o_q,o_dat,i_load,i_dat = \
            self.i_en ,self.i_init,self.i_cnt_done,self.i_lsb,self.i_byte_valid,self.o_sh_done,self.o_sh_done_r,\
            self.i_op_b_sel,self.i_shift_op,\
            self.i_rs2,self.i_imm,self.o_op_b,self.o_q,\
            self.o_dat,self.i_load,self.i_dat
        
        dat = self._reg("dat",dtype=Bits(32))
        o_op_b(i_op_b_sel._ternary(i_rs2,i_imm))

        dat_en = self._sig("dat_en")
        dat_en(i_shift_op | (i_en & i_byte_valid))

        """
            The dat register has three different use cases for store, load and
            shift operations.
            store : Data to be written is shifted to the correct position in dat during
                    init by dat_en and is presented on the data bus as o_wb_dat
            load  : Data from the bus gets latched into dat during i_wb_ack and is then
                    shifted out at the appropriate time to end up in the correct
                    position in rd
            shift : Data is shifted in during init. After that, the six LSB are used as
                    a downcounter (with bit 5 initially set to 0) that triggers
                    o_sh_done and o_sh_done_r when they wrap around to indicate that
                    the requested number of shifts have been performed
        """

        dat_shamt = self._sig("dat_shamt",dtype=Bits(6))
        If(i_shift_op & ~i_init,
            # Down counter mode
            dat_shamt(dat[6:0]-1)
        ).Else(
            # Shift reg mode with optional clearing of bit 5
            dat_shamt((dat[6] & ~(i_shift_op & i_cnt_done))._concat(dat[6:1])) 
        )
        
        o_sh_done(dat_shamt[5])
        o_sh_done_r(dat[5])

        o_q(
	       (i_lsb._eq(3) & dat[24]) |
	       (i_lsb._eq(2) & dat[16]) |
	       (i_lsb._eq(1) & dat[8]) |
	       (i_lsb._eq(0) & dat[0]))

        o_dat(dat)

        If(dat_en | i_load,
           dat(i_load._ternary(i_dat,Concat(o_op_b, dat[32:7], dat_shamt)))
        )
   

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_bufreg2(), serializer_cls=VerilogSerializer))
    