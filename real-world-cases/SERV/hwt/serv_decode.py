#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal
from hwt.synthesizer.hObjList import HObjList

class serv_decode(Unit):
    def _config(s):
        s.PRE_REGISTER   = Param(1)
        s.MDU            = Param(0)
        
    def _declr(s):

        s.clk = Clk()
        
        with s._associated(clk=s.clk):
            # Input
            s.i_wb_rdt      = VectSignal(30)    # 31:2
            s.i_wb_en       = Signal()
            
            # To state
            s.o_sh_right            = Signal()._m()
            s.o_bne_or_bge          = Signal()._m()
            s.o_cond_branch         = Signal()._m()
            s.o_e_op                = Signal()._m()
            s.o_ebreak              = Signal()._m()
            s.o_branch_op           = Signal()._m()
            s.o_shift_op            = Signal()._m()
            s.o_slt_or_branch       = Signal()._m()
            s.o_rd_op               = Signal()._m()
            s.o_two_stage_op        = Signal()._m()
            s.o_dbus_en             = Signal()._m()
            # MDU
            s.o_mdu_op              = Signal()._m()
            # Extension
            s.o_ext_funct3          = VectSignal(3)._m()
            # To bufreg
            s.o_bufreg_rs1_en       = Signal()._m()
            s.o_bufreg_imm_en       = Signal()._m()
            s.o_bufreg_clr_lsb      = Signal()._m()
            s.o_bufreg_sh_signed    = Signal()._m()
            # To ctrl
            s.o_ctrl_jal_or_jalr    = Signal()._m()
            s.o_ctrl_utype          = Signal()._m()
            s.o_ctrl_pc_rel         = Signal()._m()
            s.o_ctrl_mret           = Signal()._m()
            # To alu
            s.o_alu_sub             = Signal()._m()
            s.o_alu_bool_op         = VectSignal(2)._m()
            s.o_alu_cmp_eq          = Signal()._m()
            s.o_alu_cmp_sig         = Signal()._m()
            s.o_alu_rd_sel          = VectSignal(3)._m()
            # To mem IF
            s.o_mem_signed          = Signal()._m()
            s.o_mem_word            = Signal()._m()
            s.o_mem_half            = Signal()._m()
            s.o_mem_cmd             = Signal()._m()
            # To CSR
            s.o_csr_en              = Signal()._m()
            s.o_csr_addr            = VectSignal(2)._m()
            s.o_csr_mstatus_en      = Signal()._m()
            s.o_csr_mie_en          = Signal()._m()
            s.o_csr_mcause_en       = Signal()._m()
            s.o_csr_source          = VectSignal(2)._m()
            s.o_csr_d_sel           = Signal()._m()
            s.o_csr_imm_en          = Signal()._m()
            s.o_mtval_pc            = Signal()._m()
            # To top
            s.o_immdec_ctrl         = VectSignal(4)._m()
            s.o_immdec_en           = VectSignal(4)._m()
            s.o_op_b_source         = Signal()._m()
            # To RF IF
            s.o_rd_mem_en           = Signal()._m()
            s.o_rd_csr_en           = Signal()._m()
            s.o_rd_alu_en           = Signal()._m()
   
        s._make_association()

    def _impl(s):
        
        def make_sig(name, sz, dst):
            sig = s._sig(name=name, dtype=Bits(sz))
            dst(sig)
            return sig
        
        def bv(sz,val,vld_mask=None):
            if vld_mask is None:
                vld_mask = (1<<sz)-1
            return Bits(sz).from_py(val,vld_mask=vld_mask)
        
        opcode  = s._sig("opcode",dtype=Bits(5))
        funct3  = s._sig("funct3",dtype=Bits(3))
        op20    = s._sig("op20")
        op21    = s._sig("op21")
        op22    = s._sig("op22")
        op26    = s._sig("op26")

        imm25   = s._sig("imm25")
        imm30   = s._sig("imm30")
        
        mdu = s._sig("mdu")
        mdu(s.MDU)

        co_mdu_op = s._sig("co_mdu_op")
        co_mdu_op(mdu & opcode._eq(bv(5,0b01100)) & imm25)

        co_two_stage_op = s._sig("co_two_stage_op")
        co_two_stage_op(~opcode[2] | (funct3[0] & ~funct3[1] & ~opcode[0] & ~opcode[4]) |
	                    (funct3[1] & ~funct3[2] & ~opcode[0] & ~opcode[4]) | co_mdu_op  )
        
        co_shift_op = s._sig("co_shift_op")
        co_shift_op((opcode[2] & ~funct3[1]) & ~co_mdu_op)

        co_slt_or_branch = s._sig("co_slt_or_branch")
        co_slt_or_branch((opcode[4] | (funct3[1] & opcode[2]) | (imm30 & opcode[2] & opcode[3] & ~funct3[2])) & ~co_mdu_op)
   
        co_branch_op = s._sig("co_branch_op")
        co_branch_op(opcode[4])

        co_dbus_en = s._sig("co_dbus_en")
        co_dbus_en(~opcode[2] & ~opcode[4])

        co_mtval_pc = s._sig("co_mtval_pc")
        co_mtval_pc(opcode[4])

        co_mem_word = s._sig("co_mem_word")
        co_mem_word(funct3[1])

        co_rd_alu_en = s._sig("co_rd_alu_en")
        co_rd_alu_en(~opcode[0] & opcode[2] & ~opcode[4] & ~co_mdu_op)

        co_rd_mem_en = s._sig("co_rd_mem_en")
        co_rd_mem_en((~opcode[2] & ~opcode[0]) | co_mdu_op)

        co_ext_funct3 = s._sig("co_ext_funct3",dtype=Bits(3))
        co_ext_funct3(funct3)                 
   
        # jal,branch =     imm
        # jalr       = rs1+imm
        # mem        = rs1+imm
        # shift      = rs1
        co_bufreg_rs1_en = s._sig("co_bufreg_rs1_en")
        co_bufreg_rs1_en(~opcode[4] | (~opcode[1] & opcode[0]))
   
        co_bufreg_imm_en = s._sig("co_bufreg_imm_en")
        co_bufreg_imm_en(~opcode[2])

        # Clear LSB of immediate for BRANCH and JAL ops
        # True for BRANCH and JAL
        # False for JALR/LOAD/STORE/OP/OPIMM?
        co_bufreg_clr_lsb = s._sig("co_bufreg_clr_lsb")
        co_bufreg_clr_lsb(opcode[4] & opcode[2:0]._eq(bv(2,0b00)) | opcode[2:0]._eq(bv(2,0b11)))

        # Conditional branch
        # True for BRANCH
        # False for JAL/JALR
        co_cond_branch = s._sig("co_cond_branch")
        co_cond_branch(~opcode[0])
   
        co_ctrl_utype = s._sig("co_ctrl_utype")
        co_ctrl_utype(~opcode[4] & opcode[2] & opcode[0])

        co_ctrl_jal_or_jalr = s._sig("co_ctrl_jal_or_jalr")
        co_ctrl_jal_or_jalr(opcode[4] & opcode[0])

        # PC-relative operations
        # True for jal, b* auipc, ebreak
        # False for jalr, lui
        co_ctrl_pc_rel = s._sig("co_ctrl_pc_rel")
        co_ctrl_pc_rel( (opcode[3:0]._eq(bv(3,0b000)))  |
                        (opcode[2:0]._eq(bv(2,0b11)))   |
                        (opcode[4] & opcode[2]) & op20  |
                        (opcode[5:3]._eq(bv(2,0b00)))   )
        
   
        # Write to RD
        # True for OP-IMM, AUIPC, OP, LUI, SYSTEM, JALR, JAL, LOAD
        # False for STORE, BRANCH, MISC-MEM
        co_rd_op = s._sig("co_rd_op")
        co_rd_op((opcode[2] |
                 (~opcode[2] & opcode[4] & opcode[0]) |
                 (~opcode[2] & ~opcode[3] & ~opcode[0])))
    
        #
        # funct3
        #
        co_sh_right = s._sig("co_sh_right")
        co_sh_right(funct3[2])

        co_bne_or_bge = s._sig("co_bne_or_bge")
        co_bne_or_bge(funct3[0])

        # Matches system ops except eceall/ebreak/mret
        csr_op = s._sig("csr_op")
        csr_op(opcode[4] & opcode[2] & (funct3!=0))

        # op20
        co_ebreak = s._sig("co_ebreak")
        co_ebreak(op20)

        # opcode & funct3 & op21
        co_ctrl_mret = s._sig("co_ctrl_mret")
        co_ctrl_mret(opcode[4] & opcode[2] & op21 & ~(funct3!=0))

        # Matches system opcodes except CSR accesses (funct3 == 0)
        # and mret (!op21)
        co_e_op = s._sig("co_e_op")
        co_e_op(opcode[4] & opcode[2] & ~op21 & ~(funct3!=0))
        
        # opcode & funct3 & imm30
        co_bufreg_sh_signed = s._sig("co_bufreg_sh_signed")
        co_bufreg_sh_signed(imm30)

        """
        True for sub, b*, slt*
        False for add*
        op    opcode f3  i30
        b*    11000  xxx x   t
        addi  00100  000 x   f
        slt*  0x100  01x x   t
        add   01100  000 0   f
        sub   01100  000 1   t
        """
        co_alu_sub = s._sig("co_alu_sub")
        co_alu_sub(funct3[1] | funct3[0] | (opcode[3] & imm30) | opcode[4])

        """
        Bits 26, 22, 21 and 20 are enough to uniquely identify the eight supported CSR regs
        mtvec, mscratch, mepc and mtval are stored externally (normally in the RF) and are
        treated differently from mstatus, mie and mcause which are stored in serv_csr.

        The former get a 2-bit address as seen below while the latter get a
        one-hot enable signal each.

        Hex|2 222|Reg     |csr
        adr|6 210|name    |addr
        ---|-----|--------|----
        300|0_000|mstatus | xx
        304|0_100|mie     | xx
        305|0_101|mtvec   | 01
        340|1_000|mscratch| 00
        341|1_001|mepc    | 10
        342|1_010|mcause  | xx
        343|1_011|mtval   | 11

        """

        # true  for mtvec,mscratch,mepc and mtval
        # false for mstatus, mie, mcause
        csr_valid = s._sig("csr_valid")
        csr_valid(op20 | (op26 & ~op21))

        co_rd_csr_en = s._sig("co_rd_csr_en")
        co_rd_csr_en(csr_op)

        co_csr_en = s._sig("co_csr_en")
        co_csr_en(csr_op & csr_valid)

        co_csr_mstatus_en = s._sig("co_csr_mstatus_en")
        co_csr_mstatus_en(csr_op & ~op26 & ~op22)

        co_csr_mie_en = s._sig("co_csr_mie_en")
        co_csr_mie_en(csr_op & ~op26 &  op22 & ~op20)

        co_csr_mcause_en = s._sig("co_csr_mcause_en")
        co_csr_mcause_en(csr_op & op21 & ~op20)

        co_csr_source = s._sig("co_csr_source", dtype=Bits(2))
        co_csr_source(funct3[2:0])

        co_csr_d_sel = s._sig("co_csr_d_sel")
        co_csr_d_sel(funct3[2])

        co_csr_imm_en = s._sig("co_csr_imm_en")
        co_csr_imm_en(opcode[4] & opcode[2] & funct3[2])

        co_csr_addr = s._sig("co_csr_addr", dtype=Bits(2))
        co_csr_addr(Concat(op26 & op20, ~op26 | op21))

        co_alu_cmp_eq = s._sig("co_alu_cmp_eq")
        co_alu_cmp_eq(funct3[3:1]._eq(bv(2,0b00)))

        co_alu_cmp_sig = s._sig("co_alu_cmp_sig")
        co_alu_cmp_sig(~((funct3[0] & funct3[1]) | (funct3[1] & funct3[2])))

        co_mem_cmd = s._sig("co_mem_cmd")
        co_mem_cmd(opcode[3])

        co_mem_signed = s._sig("co_mem_signed")
        co_mem_signed(~funct3[2])

        co_mem_half = s._sig("co_mem_half")
        co_mem_half(funct3[0])

        co_alu_bool_op = s._sig("co_alu_bool_op", dtype=Bits(2))
        co_alu_bool_op(funct3[2:0])

        co_immdec_ctrl = s._sig("co_immdec_ctrl", dtype=Bits(4))
        # True for S (STORE) or B (BRANCH) type instructions
        # False for J type instructions
        co_immdec_ctrl[0](opcode[4:0]._eq(bv(4,0b1000)))
        # True for OP-IMM, LOAD, STORE, JALR  (I S)
        # False for LUI, AUIPC, JAL           (U J)
        co_immdec_ctrl[1]((opcode[2:0]._eq(bv(2,0b00))) | 
                          (opcode[3:1]._eq(bv(2,0b00))) )
        co_immdec_ctrl[2](opcode[4] & ~opcode[0])
        co_immdec_ctrl[3](opcode[4])
 
        co_immdec_en = s._sig("co_immdec_en", dtype=Bits(4))
        co_immdec_en[3](opcode[4] | opcode[3] | opcode[2] | ~opcode[0])                             # B I J S U
        co_immdec_en[2]((opcode[4] & opcode[2]) | ~opcode[3] | opcode[0])                           #   I J   U
        co_immdec_en[1]((opcode[3:1]._eq(bv(2,0b01))) | (opcode[2] & opcode[0]) | co_csr_imm_en)    #     J   U
        co_immdec_en[0](~co_rd_op)                                                                  # B     S
   
        co_alu_rd_sel = s._sig("co_alu_rd_sel", dtype=Bits(3))
        co_alu_rd_sel[0](funct3._eq(bv(3,0b000)))       # Add/sub
        co_alu_rd_sel[1](funct3[3:1]._eq(bv(2,0b01)))   # SLT*
        co_alu_rd_sel[2](funct3[2])                     # Bool
   
        # 0 (OP_B_SOURCE_IMM) when OPIMM
        # 1 (OP_B_SOURCE_RS2) when BRANCH or OP
        co_op_b_source = s._sig("co_op_b_source")
        co_op_b_source(opcode[3])

        def assign_imm():
            return CodeBlock(
                funct3(s.i_wb_rdt[14-1:12-2]),
                imm30(s.i_wb_rdt[30-2]),
                imm25(s.i_wb_rdt[25-2]),
                opcode(s.i_wb_rdt[6-1:2-2]),
                op20(s.i_wb_rdt[20-2]),
                op21(s.i_wb_rdt[21-2]),
                op22(s.i_wb_rdt[22-2]),
                op26(s.i_wb_rdt[26-2])
            )
        def assign_output():
            return CodeBlock(
                s.o_sh_right(co_sh_right),
                s.o_bne_or_bge(co_bne_or_bge),
                s.o_cond_branch(co_cond_branch),
                s.o_dbus_en(co_dbus_en),
                s.o_mtval_pc(co_mtval_pc),
                s.o_two_stage_op(co_two_stage_op),
                s.o_e_op(co_e_op),
                s.o_ebreak(co_ebreak),
                s.o_branch_op(co_branch_op),
                s.o_shift_op(co_shift_op),
                s.o_slt_or_branch(co_slt_or_branch),
                s.o_rd_op(co_rd_op),
                s.o_mdu_op(co_mdu_op),
                s.o_ext_funct3(co_ext_funct3),
                s.o_bufreg_rs1_en(co_bufreg_rs1_en),
                s.o_bufreg_imm_en(co_bufreg_imm_en),
                s.o_bufreg_clr_lsb(co_bufreg_clr_lsb),
                s.o_bufreg_sh_signed(co_bufreg_sh_signed),
                s.o_ctrl_jal_or_jalr(co_ctrl_jal_or_jalr),
                s.o_ctrl_utype(co_ctrl_utype),
                s.o_ctrl_pc_rel(co_ctrl_pc_rel),
                s.o_ctrl_mret(co_ctrl_mret),
                s.o_alu_sub(co_alu_sub),
                s.o_alu_bool_op(co_alu_bool_op),
                s.o_alu_cmp_eq(co_alu_cmp_eq),
                s.o_alu_cmp_sig(co_alu_cmp_sig),
                s.o_alu_rd_sel(co_alu_rd_sel),
                s.o_mem_signed(co_mem_signed),
                s.o_mem_word(co_mem_word),
                s.o_mem_half(co_mem_half),
                s.o_mem_cmd(co_mem_cmd),
                s.o_csr_en(co_csr_en),
                s.o_csr_addr(co_csr_addr),
                s.o_csr_mstatus_en(co_csr_mstatus_en),
                s.o_csr_mie_en(co_csr_mie_en),
                s.o_csr_mcause_en(co_csr_mcause_en),
                s.o_csr_source(co_csr_source),
                s.o_csr_d_sel(co_csr_d_sel),
                s.o_csr_imm_en(co_csr_imm_en),
                s.o_immdec_ctrl(co_immdec_ctrl),
                s.o_immdec_en(co_immdec_en),
                s.o_op_b_source(co_op_b_source),
                s.o_rd_csr_en(co_rd_csr_en),
                s.o_rd_alu_en(co_rd_alu_en),
                s.o_rd_mem_en(co_rd_mem_en)
            )

        if s.PRE_REGISTER != 0:
            If(s.clk._onRisingEdge(),
                If(s.i_wb_en,
                    assign_imm()
                )
            )
            assign_output()
        else:
            assign_imm()
            If(s.clk._onRisingEdge(),
                If(s.i_wb_en,
                    assign_output()
                )
            )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_decode(), serializer_cls=VerilogSerializer))
    