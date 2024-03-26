#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Switch, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, Rst, VectSignal
from hwt.interfaces.utils import propagateClkRst

class serv_csr(Unit):
    def _config(s):
        s.RESET_STRATEGY_VAL    = Param(1)
        s.W                     = Param(1)
        s.B                     = Param(s.W-1)
        
    def _declr(s):
        W           = s.W
        B           = s.B
        
        s.i_clk = Clk()
        with s._associated(clk=s.i_clk):
            s.i_rst = Rst()
            with s._associated(rst=s.i_rst):
                # State
                s.i_trig_irq    = Signal()
                s.i_en          = Signal()
                s.i_cnt0to3     = Signal()
                s.i_cnt3        = Signal()
                s.i_cnt7        = Signal()
                s.i_cnt_done    = Signal()
                s.i_mem_op      = Signal()
                s.i_mtip        = Signal()
                s.i_trap        = Signal()
                s.o_new_irq     = Signal()._m()
                # Control
                s.i_e_op        = Signal()
                s.i_ebreak      = Signal()
                s.i_mem_cmd     = Signal()
                s.i_mstatus_en  = Signal()
                s.i_mie_en      = Signal()
                s.i_mcause_en   = Signal()
                s.i_csr_source  = Signal(Bits(2))
                s.i_mret        = Signal()
                s.i_csr_d_sel   = Signal()
                # Data
                s.i_rf_csr_out  = Signal(Bits(W))
                s.o_csr_in      = Signal(Bits(W))._m()
                s.i_csr_imm     = Signal(Bits(W))
                s.i_rs1         = Signal(Bits(W))
                s.o_q           = Signal(Bits(W))._m()
        
        s._make_association()

    def _impl(s):
        W = s.W
        B = s.B
        
        s.clk = s.i_clk
        s.rst = s.i_rst
        
        propagateClkRst(s)

        def bv(sz,val,vld_mask=None):
            if vld_mask is None:
                vld_mask = (1<<sz)-1
            if sz==0:
                return None
            return Bits(sz).from_py(val,vld_mask=vld_mask)
        
        CSR_SOURCE_CSR = bv(2,0b00)
        CSR_SOURCE_EXT = bv(2,0b01)
        CSR_SOURCE_SET = bv(2,0b10)
        CSR_SOURCE_CLR = bv(2,0b11)

        mstatus_mie     = s._reg("mstatus_mie", def_val=None)
        mstatus_mpie    = s._reg("mstatus_mpie", def_val=None)
        
        if s.RESET_STRATEGY_VAL != 0:
            o_new_irq = s._reg("o_new_irq", def_val=0)
            mie_mtie  = s._reg("mie_mtie",  def_val=0)
        else:
            o_new_irq = s._reg("o_new_irq", def_val=None)
            mie_mtie  = s._reg("mie_mtie",  def_val=None)

        s.o_new_irq(o_new_irq)

        mcause31        = s._reg("mcause31", def_val=None)
        mcause3_0       = s._reg("mcause31", dtype=Bits(4), def_val=None)
        mcause          = s._sig("mcause", dtype=Bits(W))

        csr_in          = s._sig("csr_in", dtype=Bits(W))
        csr_out         = s._sig("csr_out", dtype=Bits(W))

        timer_irq_r     = s._reg("timer_irq_r", def_val=None)

        d = s._sig("d", dtype=Bits(W))
        d(s.i_csr_d_sel._ternary(s.i_csr_imm, s.i_rs1))

        Switch(s.i_csr_source
        ).Case(CSR_SOURCE_EXT,
            csr_in(d)
        ).Case(CSR_SOURCE_SET,
            csr_in(csr_out | d)      
        ).Case(CSR_SOURCE_CLR,
            csr_in(csr_out & ~d)
        ).Case(CSR_SOURCE_CSR,
            csr_in(csr_out)
        ).Default(
            csr_in(None)
        )

        if B==0:
            csr_out( (s.i_mstatus_en & mstatus_mie & s.i_cnt3 & s.i_en) |
                    s.i_rf_csr_out |
		            (replicate(W, s.i_mcause_en & s.i_en) & mcause))
        else:
            csr_out( (Concat(s.i_mstatus_en & mstatus_mie & s.i_cnt3 & s.i_en, bv(B,0b0))) |
                    s.i_rf_csr_out |
		            (replicate(W, s.i_mcause_en & s.i_en) & mcause))

        s.o_q(csr_out)

        timer_irq = s._sig("timer_irq")
        timer_irq(s.i_mtip & mstatus_mie & mie_mtie)

        if B==0:
            mcause(s.i_cnt0to3._ternary(mcause3_0[W:0], # [3:0]
                                    s.i_cnt_done._ternary(mcause31, # [31]
                                                          bv(W,0b0))))
        else:
            mcause(s.i_cnt0to3._ternary(mcause3_0[W:0], # [3:0]
                                    s.i_cnt_done._ternary(Concat(mcause31, bv(B,0b0)), # [31]
                                                          bv(W,0b0))))
   
        s.o_csr_in(csr_in)

        If(s.i_trig_irq,
            timer_irq_r(timer_irq),
	        o_new_irq(timer_irq & ~timer_irq_r)
        )

        If(s.i_mie_en & s.i_cnt7,
            mie_mtie(csr_in[B])
        )
        
        """
        The mie bit in mstatus gets updated under three conditions

        When a trap is taken, the bit is cleared
        During an mret instruction, the bit is restored from mpie
        During a mstatus CSR access instruction it's assigned when
        bit 3 gets updated

        These conditions are all mutually exclusibe
        """

        If((s.i_trap & s.i_cnt_done) | s.i_mstatus_en & s.i_cnt3 & s.i_en | s.i_mret,
            mstatus_mie(~s.i_trap & (s.i_mret._ternary(mstatus_mpie, csr_in[B])))
        )
        
        """
        Note: To save resources mstatus_mpie (mstatus bit 7) is not
        readable or writable from sw
        """
        If(s.i_trap & s.i_cnt_done,
            mstatus_mpie(mstatus_mie)
        )

        """
        The four lowest bits in mcause hold the exception code

        These bits get updated under three conditions

        During an mcause CSR access function, they are assigned when
        bits 0 to 3 gets updated

        During an external interrupt the exception code is set to
        7, since SERV only support timer interrupts

        During an exception, the exception code is assigned to indicate
        if it was caused by an ebreak instruction (3),
        ecall instruction (11), misaligned load (4), misaligned store (6)
        or misaligned jump (0)

        The expressions below are derived from the following truth table
        irq  => 0111 (timer=7)
        e_op => x011 (ebreak=3, ecall=11)
        mem  => 01x0 (store=6, load=4)
        ctrl => 0000 (jump=0)
        """
    
        mcause3_0_2_w1 = s._sig("mcause3_0_2_w1")
        mcause3_0_1_w1 = s._sig("mcause3_0_1_w1")
        mcause3_0_0_w1 = s._sig("mcause3_0_0_w1")
        if W==1:
            mcause3_0_2_w1(mcause3_0[3])
            mcause3_0_1_w1(mcause3_0[2])
            mcause3_0_0_w1(mcause3_0[1])
        else:
            mcause3_0_2_w1(csr_in[2])
            mcause3_0_1_w1(csr_in[1])
            mcause3_0_0_w1(csr_in[0])

        If((s.i_mcause_en & s.i_en & s.i_cnt0to3) | (s.i_trap & s.i_cnt_done),
            mcause3_0[3]((s.i_e_op & ~s.i_ebreak) | (~s.i_trap & csr_in[B])),
            mcause3_0[2](o_new_irq | s.i_mem_op | (~s.i_trap & (mcause3_0_2_w1))),
            mcause3_0[1](o_new_irq | s.i_e_op | (s.i_mem_op & s.i_mem_cmd) | (~s.i_trap & (mcause3_0_1_w1))),
            mcause3_0[0](o_new_irq | s.i_e_op | (~s.i_trap & (mcause3_0_0_w1)))                                             
        )

        If(s.i_mcause_en & s.i_cnt_done | s.i_trap,
           mcause31(s.i_trap._ternary(o_new_irq,csr_in[B]))
        )
	

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_csr(), serializer_cls=VerilogSerializer))
    