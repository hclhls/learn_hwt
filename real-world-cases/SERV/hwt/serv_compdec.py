#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import Switch, SwitchLogic, If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal

class serv_compdec(Unit):
    
    def _declr(s):
        s.i_clk = Clk()
        with s._associated(clk=s.i_clk):  
            s.i_instr = VectSignal(32)
            s.i_ack = Signal()
            s.o_instr = VectSignal(32)._m()
            s.o_iscomp = Signal()._m()
   
        s._make_association()

    def _impl(s):
        
        def bv(sz,val,vld_mask=None):
            if vld_mask is None:
                vld_mask = (1<<sz)-1
            return Bits(sz).from_py(val,vld_mask=vld_mask)
        
        OPCODE_LOAD     = bv(7,0x03)
        OPCODE_OP_IMM   = bv(7,0x13)
        OPCODE_STORE    = bv(7,0x23)
        OPCODE_OP       = bv(7,0x33)
        OPCODE_LUI      = bv(7,0x37)
        OPCODE_BRANCH   = bv(7,0x63)
        OPCODE_JALR     = bv(7,0x67)
        OPCODE_JAL      = bv(7,0x6f)

        # C0
        def c_addi4spn(comp_instr):
            # c.addi4spn -> addi rd', x2, imm
            return comp_instr(Concat(   bv(2,0b00),
                                        s.i_instr[11:7],
                                        s.i_instr[13:11],
                                        s.i_instr[5],
                                        s.i_instr[6],
                                        bv(2,0b00),
                                        bv(5,0x02),
                                        bv(3,0b000),
                                        bv(2,0b01),
                                        s.i_instr[5:2],
                                        OPCODE_OP_IMM))
        
        def c_lw(comp_instr):
            # c.lw -> lw rd', imm(rs1')
            return comp_instr(Concat(   bv(5,0b0),
                                        s.i_instr[5],
                                        s.i_instr[13:10],
                                        s.i_instr[6],
                                        bv(2,0b00),
                                        bv(2,0b01),
                                        s.i_instr[10:7],
                                        bv(3,0b010),
                                        bv(2,0b01),
                                        s.i_instr[5:2],
                                        OPCODE_LOAD))
        
        def c_sw(comp_instr):
            # c.sw -> sw rs2', imm(rs1')
            return comp_instr(Concat(   bv(5,0b0),
                                        s.i_instr[5],
                                        s.i_instr[12],
                                        bv(2,0b01),
                                        s.i_instr[5:2],
                                        bv(2,0b01),
                                        s.i_instr[10:7],
                                        bv(3,0b010),
                                        s.i_instr[12:10],
                                        s.i_instr[6],
                                        bv(2,0b00),
                                        OPCODE_STORE))
        
        # C1
        # Register address checks for RV32E are performed in the regular instruction decoder.
        # If this check fails, an illegal instruction exception is triggered and the controller
        # writes the actual faulting instruction to mtval.
        def c_addi_nop(comp_instr):
            # c.addi -> addi rd, rd, nzimm
            # c.nop
            return comp_instr(Concat(   replicate(6,s.i_instr[12]),
                                        s.i_instr[12],
                                        s.i_instr[7:2],
                                        s.i_instr[12:7],
                                        bv(3,0),
                                        s.i_instr[12:7],
                                        OPCODE_OP_IMM))
        
        def c_jal_j(comp_instr):
            # 001: c.jal -> jal x1, imm
            # 101: c.j   -> jal x0, imm
            return comp_instr(Concat(   s.i_instr[12],
                                        s.i_instr[8],
                                        s.i_instr[11:9],
                                        s.i_instr[6],
                                        s.i_instr[7], 
                                        s.i_instr[2], 
                                        s.i_instr[11], 
                                        s.i_instr[6:3],
                                        replicate(9,s.i_instr[12]),
                                        bv(4,0),
                                        ~s.i_instr[15],
                                        OPCODE_JAL))

        def c_li(comp_instr):
            # c.li -> addi rd, x0, nzimm
            # (c.li hints are translated into an addi hint)
            return comp_instr(Concat(   replicate(6,s.i_instr[12]),
                                        s.i_instr[12], 
                                        s.i_instr[7:2],
                                        bv(5,0),
                                        bv(3,0),
                                        s.i_instr[12:7],
                                        OPCODE_OP_IMM))
        
        def c_lui(comp_instr):
            # c.lui -> lui rd, imm
            # (c.lui hints are translated into a lui hint)
            return comp_instr(Concat(   replicate(15,s.i_instr[12]),
                                        s.i_instr[7:2], 
                                        s.i_instr[12:7], 
                                        OPCODE_LUI))
        
        def c_addi16sp(comp_instr):
            # c.addi16sp -> addi x2, x2, nzimm
            return comp_instr(Concat(   replicate(3,s.i_instr[12]),
                                        s.i_instr[5:3], 
                                        s.i_instr[5], 
                                        s.i_instr[2],
                                        s.i_instr[6], 
                                        bv(4,0), 
                                        bv(5,0x02), 
                                        bv(3,0b000), 
                                        bv(5,0x02),
                                        OPCODE_OP_IMM))
        
        def c_srli_srai(comp_instr):
            # 00: c.srli -> srli rd, rd, shamt
            # 01: c.srai -> srai rd, rd, shamt
            # (c.srli/c.srai hints are translated into a srli/srai hint)
            return comp_instr(Concat(   bv(1,0),
                                        s.i_instr[10], 
                                        bv(5,0), 
                                        s.i_instr[7:2], 
                                        bv(2,0b01), 
                                        s.i_instr[10:7],
                                        bv(3,0b101), 
                                        bv(2,0b01), 
                                        s.i_instr[10:7], 
                                        OPCODE_OP_IMM))

        def c_andi(comp_instr):
            # c.andi -> andi rd, rd, imm
            return comp_instr(Concat(   replicate(6,s.i_instr[12]),
                                        s.i_instr[12], 
                                        s.i_instr[7:2], 
                                        bv(2,0b01), 
                                        s.i_instr[10:7],
                                        bv(3,0b111), 
                                        bv(2,0b01), 
                                        s.i_instr[10:7], 
                                        OPCODE_OP_IMM)) 
           
        def c_sub(comp_instr):
            # c.sub -> sub rd', rd', rs2'
            return comp_instr(Concat(   bv(2,0b01), 
                                        bv(5,0b0), 
                                        bv(2,0b01), 
                                        s.i_instr[5:2], 
                                        bv(2,0b01), 
                                        s.i_instr[10:7],
                                        bv(3,0b000), 
                                        bv(2,0b01), 
                                        s.i_instr[10:7],
                                        OPCODE_OP))
        
        def c_xor(comp_instr):
            # c.xor -> xor rd', rd', rs2'
            return comp_instr(Concat(   bv(7,0b0), 
                                        bv(2,0b01), 
                                        s.i_instr[5:2], 
                                        bv(2,0b01), 
                                        s.i_instr[10:7], 
                                        bv(3,0b100),
                                        bv(2,0b01), 
                                        s.i_instr[10:7], 
                                        OPCODE_OP))

        def c_or(comp_instr):
            # c.or  -> or  rd', rd', rs2'
            return comp_instr(Concat(   bv(7,0b0), 
                                        bv(2,0b01), 
                                        s.i_instr[5:2], 
                                        bv(2,0b01), 
                                        s.i_instr[10:7], 
                                        bv(3,0b110),
                                        bv(2,0b01), 
                                        s.i_instr[10:7], 
                                        OPCODE_OP))

        def c_and(comp_instr):
            # c.and -> and rd', rd', rs2'
            return comp_instr(Concat(   bv(7,0b0), 
                                        bv(2,0b01), 
                                        s.i_instr[5:2], 
                                        bv(2,0b01), 
                                        s.i_instr[10:7], 
                                        bv(3,0b111),
                                        bv(2,0b01), 
                                        s.i_instr[10:7],
                                        OPCODE_OP))                                        
        
        def c_beqz_bnez(comp_instr):
            # 0: c.beqz -> beq rs1', x0, imm
            # 1: c.bnez -> bne rs1', x0, imm
            return comp_instr(Concat(   replicate(4,s.i_instr[12]),
                                        s.i_instr[7:5], 
                                        s.i_instr[2], 
                                        bv(5,0b0), 
                                        bv(2,0b01),
                                        s.i_instr[10:7], 
                                        bv(2,0b00), 
                                        s.i_instr[13], 
                                        s.i_instr[12:10], 
                                        s.i_instr[5:3],
                                        s.i_instr[12],
                                        OPCODE_BRANCH))
        
        # C2
        # Register address checks for RV32E are performed in the regular instruction decoder.
        # If this check fails, an illegal instruction exception is triggered and the controller
        # writes the actual faulting instruction to mtval.
        def c_slli(comp_instr):
            # c.slli -> slli rd, rd, shamt
            # (c.ssli hints are translated into a slli hint)
            return comp_instr(Concat(   bv(7,0b0), 
                                        s.i_instr[7:2], 
                                        s.i_instr[12:7], 
                                        bv(3,0b001), 
                                        s.i_instr[12:7], 
                                        OPCODE_OP_IMM))   

        def c_lwsp(comp_instr):
            # c.lwsp -> lw rd, imm(x2)
            return comp_instr(Concat(   bv(4,0b0), 
                                        s.i_instr[4:2], 
                                        s.i_instr[12], 
                                        s.i_instr[7:4], 
                                        bv(2,0b00), 
                                        bv(5,0x02),
                                        bv(3,0b010), 
                                        s.i_instr[12:7], 
                                        OPCODE_LOAD))
        
        def c_mv(comp_instr):
            # c.mv -> add rd/rs1, x0, rs2
            # (c.mv hints are translated into an add hint)
            return  comp_instr(Concat(  bv(7,0b0), 
                                        s.i_instr[7:2], 
                                        bv(5,0b0), 
                                        bv(3,0b0), 
                                        s.i_instr[12:7], 
                                        OPCODE_OP))
        
        def c_jr(comp_instr):
            # c.jr -> jalr x0, rd/rs1, 0
            return comp_instr(Concat(   bv(12,0b0), 
                                        s.i_instr[12:7], 
                                        bv(3,0b0), 
                                        bv(5,0b0),
                                        OPCODE_JALR))
        
        def c_add(comp_instr):
            # c.add -> add rd, rd, rs2
            # (c.add hints are translated into an add hint)
            return comp_instr(Concat(   bv(7,0b0), 
                                        s.i_instr[7:2], 
                                        s.i_instr[12:7], 
                                        bv(3,0b0), 
                                        s.i_instr[12:7], 
                                        OPCODE_OP))
        
        def c_ebreak(comp_instr):
            # c.ebreak -> ebreak
            return comp_instr(bv(32,0x00100073))
        
        def c_jalr(comp_instr):
            # c.jalr -> jalr x1, rs1, 0
            return comp_instr(Concat(   bv(12,0b0), 
                                        s.i_instr[12:7], 
                                        bv(3,0b000), 
                                        bv(5,0b00001),
                                        OPCODE_JALR))

        def c_swsp(comp_instr):
            # c.swsp -> sw rs2, imm(x2)
            return comp_instr(Concat(   bv(4,0b0), 
                                        s.i_instr[9:7], 
                                        s.i_instr[12], 
                                        s.i_instr[7:2], 
                                        bv(5,0x02), 
                                        bv(3,0b010),
                                        s.i_instr[12:9], 
                                        bv(2,0b00), 
                                        OPCODE_STORE))
        
        s.clk = s.i_clk
        
        iscomp_reg    = s._reg("iscomp_reg")
        s.o_iscomp(iscomp_reg)

        comp_instr      = s._reg("comp_instr", dtype=Bits(32))
        illegal_instr   = s._reg("illegal_instr")

        s.o_instr(illegal_instr._ternary(s.i_instr, comp_instr))

        If(s.i_ack,
           iscomp_reg(~illegal_instr)
        )
        
        CodeBlock(
            # By default, forward incoming instruction, mark it as legal.
            comp_instr(s.i_instr),
            illegal_instr(0),
            
            # Check if incoming instruction is compressed.
            Switch(s.i_instr[2:0]
            ).Case(0b00, # C0
                SwitchLogic([
                    (s.i_instr[16:14]._eq(0b00), c_addi4spn(comp_instr) ),
                    (s.i_instr[16:14]._eq(0b01), c_lw(comp_instr)       ),
                    (s.i_instr[16:14]._eq(0b11), c_sw(comp_instr)       ),
                    (s.i_instr[16:14]._eq(0b10), illegal_instr(1)       ),
                ])
            ).Case(0b01,    # C1
                SwitchLogic([
                    (s.i_instr[16:13]._eq(0b000),            c_addi_nop(comp_instr)), 
                    (s.i_instr[16:13]._eq(bv(3,0b001,0b011)),c_jal_j(comp_instr)),
                    (s.i_instr[16:13]._eq(0b010),            c_li(comp_instr)),
                    (s.i_instr[16:13]._eq(0b011),            If(s.i_instr[12:7]._eq(bv(5,0x02)),
                                                                c_addi16sp(comp_instr)
                                                              ).Else(
                                                                c_lui(comp_instr)
                                                              )),
                    (s.i_instr[16:13]._eq(0b100),           If(s.i_instr[12:10]._eq(bv(2,0b00,0b10)),
                                                               c_srli_srai(comp_instr)
                                                            ).Elif(s.i_instr[12:10]._eq(0b10),
                                                                c_andi(comp_instr)
                                                            ).Elif(s.i_instr[12:10]._eq(0b11),
                                                                Switch(s.i_instr[7:5]
                                                                ).Case(0b00,
                                                                    c_sub(comp_instr)
                                                                ).Case(0b01,
                                                                    c_xor(comp_instr)
                                                                ).Case(0b10,
                                                                    c_or(comp_instr)
                                                                ).Case(0b11,
                                                                    c_and(comp_instr)
                                                                )
                                                            )),
                    (s.i_instr[16:13]._eq(bv(3,0b110,0b110)), c_beqz_bnez(comp_instr))
                ])
            ).Case(0b10,    # C2
                Switch(s.i_instr[16:14]
                ).Case(0b00,
                    c_slli(comp_instr)
                ).Case(0b01,
                    c_lwsp(comp_instr)
                ).Case(0b10,
                    If(s.i_instr[12]._eq(bv(1,0b0)),
                        If(s.i_instr[7:2] != bv(5,0b0),
                           c_mv(comp_instr)
                        ).Else(
                            c_jr(comp_instr)
                        )
                    ).Else(
                        If(s.i_instr[7:2] != bv(5,0b0),
                            c_add(comp_instr)
                        ).Else(
                            If(s.i_instr[12:7]._eq(bv(5,0b0)),
                                c_ebreak(comp_instr)
                            ).Else(
                                c_jalr(comp_instr)
                            )
                        )
                    )
                ).Case(0b11,
                    c_swsp(comp_instr)
                )
            ).Case(0b11,
                # Incoming instruction is not compressed.
                illegal_instr(1)
            )
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_compdec(), serializer_cls=VerilogSerializer))
    