#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, Rst, VectSignal
from hwt.interfaces.utils import propagateClkRst

class serv_ctrl(Unit):
    def _config(s):
        s.RESET_STRATEGY_VAL    = Param(1)
        s.RESET_PC              = Param(0)
        s.WITH_CSR              = Param(1)
        s.W                     = Param(1)
        s.B                     = Param(s.W-1)
        
    def _declr(s):
        W           = s.W
        B           = s.B
        
        s.clk = Clk()
        with s._associated(clk=s.clk):
            s.i_rst = Rst()
            with s._associated(rst=s.i_rst):
                # State
                s.i_pc_en = Signal()
                s.i_cnt12to31 = Signal()
                s.i_cnt0 = Signal()
                s.i_cnt1 = Signal()
                s.i_cnt2 = Signal()
                # Control
                s.i_jump = Signal()
                s.i_jal_or_jalr = Signal()
                s.i_utype = Signal()
                s.i_pc_rel = Signal()
                s.i_trap = Signal()
                s.i_iscomp = Signal()
                # Data
                s.i_imm = VectSignal(W)
                s.i_buf  = VectSignal(W)
                s.i_csr_pc  = VectSignal(W)
                s.o_rd = VectSignal(W)._m()
                s.o_bad_pc = VectSignal(W)._m()
                # External
                s.o_ibus_adr = VectSignal(32)._m()
        
        s._make_association()

   
    def _impl(s):
        W           = s.W
        B           = s.B
        WITH_CSR    = s.WITH_CSR
        
        s.rst = s.i_rst
        
        propagateClkRst(s)

        def bv(sz,val,vld_mask=None):
            if vld_mask is None:
                vld_mask = (1<<sz)-1
            return Bits(sz).from_py(val,vld_mask=vld_mask)
        
        pc_plus_4               = s._sig("pc_plus_4", dtype=Bits(W))
        pc_plus_4_cy            = s._sig("pc_plus_4_cy")
        pc_plus_4_cy_r          = s._reg("pc_plus_4_cy_r", def_val=None)
        pc_plus_4_cy_r_w        = s._sig("pc_plus_4_cy_r_w", dtype=Bits(W))
        pc_plus_offset          = s._sig("pc_plus_offsets", dtype=Bits(W))
        pc_plus_offset_cy       = s._sig("pc_plus_offset_cy") 
        pc_plus_offset_cy_r     = s._reg("pc_plus_offset_cy_r", def_val=None)
        pc_plus_offset_cy_r_w   = s._sig("pc_plus_offset_cy_r_w")
        pc_plus_offset_aligned  = s._sig("pc_plus_offset_aligned")
        plus_4                  = s._sig("plus_4", dtype=Bits(W))

        pc = s._sig("pc", dtype=Bits(W))
        pc(s.o_ibus_adr[W:0])

        new_pc = s._sig("new_pc", dtype=Bits(W))

        offset_a = s._sig("offset_a", dtype=Bits(W))
        offset_b = s._sig("offset_b", dtype=Bits(W))

        #  If i_iscomp=1: increment pc by 2 else increment pc by 4

        if W==1:
            plus_4(s.i_iscomp._ternary(s.i_cnt1, s.i_cnt2))
        elif W==4:
            plus_4((s.i_cnt0 | s.i_cnt1)._ternary(s.i_iscomp._ternary(2,4)),0)

        s.o_bad_pc(pc_plus_offset_aligned)

        pc_plus_4_with_cy = Concat(pc_plus_4_cy,pc_plus_4)
        pc_plus_4_with_cy(pc._reinterpret_cast(pc_plus_4_with_cy._dtype)+
                          plus_4._reinterpret_cast(pc_plus_4_with_cy._dtype)+
                          pc_plus_4_cy_r_w._reinterpret_cast(pc_plus_4_with_cy._dtype))


        if WITH_CSR != 0:
            if W == 1:
                new_pc(s.i_trap._ternary((s.i_csr_pc & ~(s.i_cnt0 | s.i_cnt1)), s.i_jump._ternary(pc_plus_offset_aligned ,pc_plus_4)))
            elif W == 4:
                new_pc(s.i_trap._ternary( (s.i_csr_pc & ((s.i_cnt0 | s.i_cnt1)._ternary(bv(4,0b1100),bv(4,0b1111)))), 
                                          s.i_jump._ternary(pc_plus_offset_aligned, pc_plus_4)))
        else:
            new_pc(s.i_jump._ternary(pc_plus_offset_aligned, pc_plus_4))
                   
        s.o_rd((replicate(W,s.i_utype) & pc_plus_offset_aligned) | pc_plus_4 & replicate(W, s.i_jal_or_jalr))

        offset_a(replicate(W,s.i_pc_rel) & pc)
        offset_b(s.i_utype._ternary(s.i_imm & replicate(W, s.i_cnt12to31), s.i_buf))

        pc_plus_offset_with_cy = Concat(pc_plus_offset_cy, pc_plus_offset)
        pc_plus_offset_with_cy( offset_a._reinterpret_cast(pc_plus_offset_with_cy._dtype)+
                                offset_b._reinterpret_cast(pc_plus_offset_with_cy._dtype)+
                                pc_plus_offset_cy_r_w._reinterpret_cast(pc_plus_offset_with_cy._dtype))
        
        if W > 1 :
            pc_plus_offset_aligned[W:1](pc_plus_offset[W:1])
            pc_plus_offset_cy_r_w[W:1](bv(B,0b0))
            pc_plus_4_cy_r_w[W:1](bv(B,0b0))
        
        pc_plus_offset_aligned[0](pc_plus_offset[0] & ~s.i_cnt0)
        pc_plus_offset_cy_r_w[0](pc_plus_offset_cy_r)
        pc_plus_4_cy_r_w[0](pc_plus_4_cy_r)
        
        pc_plus_4_cy_r(s.i_pc_en & pc_plus_4_cy)
        pc_plus_offset_cy_r(s.i_pc_en & pc_plus_offset_cy)
        
        if s.RESET_STRATEGY_VAL == 0:
            o_ibus_adr = s._sig("o_ibus_adr", dtype=Bits(32), def_val=0)
            s.o_ibus_adr(o_ibus_adr)
            If(s.clk._onRisingEdge(),
                If(s.i_pc_en,
                    o_ibus_adr(Concat(new_pc, s.o_ibus_adr[32:W])) 
                )
            )
        else:
            o_ibus_adr = s._reg("o_ibus_adr", dtype=Bits(32), def_val=s.RESET_PC)
            s.o_ibus_adr(o_ibus_adr)
            If(s.i_pc_en,
                o_ibus_adr(Concat(new_pc, s.o_ibus_adr[32:W]))
            )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_ctrl(), serializer_cls=VerilogSerializer))
    