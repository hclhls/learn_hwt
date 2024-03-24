#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal

class serv_bufreg(Unit):
    def _config(self):
        self.MDU = Param(0)
        self.W   = Param(1)
        self.B   = Param(self.W-1)

    def _declr(self):
        W = self.W
        B = self.B

        self.i_clk = Clk()
        
        with self._associated(clk=self.i_clk):
            # State
            self.i_cnt0     = Signal()
            self.i_cnt1     = Signal()
            self.i_en       = Signal()
            self.i_init     = Signal()
            self.i_mdu_op   = Signal()
            self.o_lsb      = VectSignal(2)._m()
            # Control
            self.i_rs1_en   = Signal()
            self.i_imm_en   = Signal()
            self.i_clr_lsb  = Signal()
            self.i_sh_signed = Signal()
            # Data
            self.i_rs1      = VectSignal(W)
            self.i_imm      = VectSignal(W)
            self.o_q        = VectSignal(W)._m()
            # External
            self.o_dbus_adr = VectSignal(32)._m()
            # Extension
            self.o_ext_rs1  = VectSignal(32)._m()
   
        self._make_association()

    def _impl(self):
        W = self.W
        B = self.B
        
        self.clk = self.i_clk
        
        i_cnt0,i_cnt1,i_en,i_init,i_mdu_op,o_lsb,i_rs1_en,i_imm_en,i_clr_lsb,i_sh_signed,i_rs1,i_imm,o_q,o_dbus_adr,o_ext_rs1=\
            self.i_cnt0,self.i_cnt1,self.i_en,self.i_init,self.i_mdu_op,self.o_lsb,\
            self.i_rs1_en,self.i_imm_en,self.i_clr_lsb,self.i_sh_signed,\
            self.i_rs1,self.i_imm,self.o_q,\
            self.o_dbus_adr,self.o_ext_rs1

        c       = self._sig("c")
        q       = self._sig("q",dtype=Bits(W))
        c_r     = self._reg("c_r",dtype=Bits(W))
        data    = self._reg("data",dtype=Bits(32));
        clr_lsb = self._sig("clr_lsb", dtype=Bits(W))

        clr_lsb[0](i_cnt0 & i_clr_lsb)

        c_q = c._concat(q)
        c_q_dtype = c_q._dtype
        c._concat(q)(Concat(Bits(1).from_py(0),(i_rs1 & replicate(W,i_rs1_en)           )) + \
                     Concat(Bits(1).from_py(0),(i_imm & replicate(W,i_imm_en) & ~clr_lsb)) + c_r._reinterpret_cast(c_q_dtype))

        CodeBlock(
            c_r(0),
            c_r[0](c & i_en)
        )
        
        lsb = self._sig("lsb", dtype=Bits(2))

        if W==1:
            If(i_en,
                data[32:2](i_init._ternary(q, replicate(W, data[31] & i_sh_signed))._concat(data[32:3]))
            )
            If(i_init._ternary((i_cnt0 | i_cnt1),i_en),
                data[2:](i_init._ternary(q,data[2])._concat(data[1]))
            )
            
            lsb(data[2:])
            o_q(data[0] & replicate(W,i_en))

        o_dbus_adr(data[32:2]._concat(Bits(2).from_py(0)))
        o_ext_rs1(data)
        
        mdu_on = self._sig("mdu_on")
        mdu_on(self.MDU)
        If(i_mdu_op & mdu_on,
           o_lsb(0)
        ).Else(
            o_lsb(lsb)
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_bufreg(), serializer_cls=VerilogSerializer))
    