#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal

class serv_rf_if(Unit):
    def _config(s):
        s.WITH_CSR   = Param(1)
        s.W          = Param(1)
        s.B          = Param(s.W-1)
        s.WITH_CSR_P5= Param(5+s.WITH_CSR)

    def _declr(s):
        W           = s.W
        B           = s.B
        WITH_CSR_P5 = s.WITH_CSR_P5

        # RF Interface
        s.i_cnt_en      = Signal()
        s.o_wreg0       = VectSignal(WITH_CSR_P5)._m()
        s.o_wreg1       = VectSignal(WITH_CSR_P5)._m()
        s.o_wen0        = Signal()._m()
        s.o_wen1        = Signal()._m()
        s.o_wdata0      = VectSignal(W)._m()
        s.o_wdata1      = VectSignal(W)._m()
        s.o_rreg0       = VectSignal(WITH_CSR_P5)._m()
        s.o_rreg1       = VectSignal(WITH_CSR_P5)._m()
        s.i_rdata0      = VectSignal(W)
        s.i_rdata1      = VectSignal(W)

        # Trap interface
        s.i_trap        = Signal()
        s.i_mret        = Signal()
        s.i_mepc        = VectSignal(W)
        s.i_mtval_pc    = Signal()
        s.i_bufreg_q    = VectSignal(W)
        s.i_bad_pc      = VectSignal(W)
        s.o_csr_pc      = VectSignal(W)._m()

        # CSR interface
        s.i_csr_en      = Signal()
        s.i_csr_addr    = VectSignal(2)
        s.i_csr         = VectSignal(W)
        s.o_csr         = VectSignal(W)._m()
   
        # RD write port
        s.i_rd_wen      = Signal()
        s.i_rd_waddr    = VectSignal(5)
        s.i_ctrl_rd     = VectSignal(W)
        s.i_alu_rd      = VectSignal(W)
        s.i_rd_alu_en   = Signal()
        s.i_csr_rd      = VectSignal(W)
        s.i_rd_csr_en   = Signal()
        s.i_mem_rd      = VectSignal(W)
        s.i_rd_mem_en   = Signal()

        # RS1 read port
        s.i_rs1_raddr   = VectSignal(5)
        s.o_rs1         = VectSignal(W)._m()

        # RS2 read port
        s.i_rs2_raddr   = VectSignal(5)
        s.o_rs2         = VectSignal(W)._m()

    def _impl(s):
        W           = s.W
        B           = s.B
        WITH_CSR    = s.WITH_CSR
        WITH_CSR_P5 = s.WITH_CSR_P5
        
        def bv(sz,val,vld_mask=None):
            if vld_mask is None:
                vld_mask = (1<<sz)-1
            return Bits(sz).from_py(val,vld_mask=vld_mask)
        
        """
        ********** Write side ***********
        """
        rd_wen = s._sig("rd_wen")
        rd_wen(s.i_rd_wen & (s.i_rd_waddr!=0))

        if WITH_CSR!=0:
            rd = s._sig("rd", dtype=Bits(W))
            rd(replicate(W,s.i_rd_alu_en) & s.i_alu_rd |
               replicate(W,s.i_rd_csr_en) & s.i_csr_rd |
               replicate(W,s.i_rd_mem_en) & s.i_mem_rd |
               s.i_ctrl_rd)  
       
            mtval = s._sig("mtval", dtype=Bits(W))
            mtval(s.i_mtval_pc._ternary(s.i_bad_pc,s.i_bufreg_q))

            s.o_wdata0(s.i_trap._ternary(mtval,rd))
            s.o_wdata1(s.i_trap._ternary(s.i_mepc,s.i_csr))
  
            """
            Port 0 handles writes to mtval during traps and rd otherwise
            * Port 1 handles writes to mepc during traps and csr accesses otherwise
            *
            * GPR registers are mapped to address 0-31 (bits 0xxxxx).
            * Following that are four CSR registers
            * mscratch 100000
            * mtvec    100001
            * mepc     100010
            * mtval    100011
            """

            s.o_wreg0(s.i_trap._ternary(bv(6,0b100011), Concat(bv(1,0     ),s.i_rd_waddr)))
            s.o_wreg1(s.i_trap._ternary(bv(6,0b100010), Concat(bv(4,0b1000),s.i_csr_addr)))
  
            s.o_wen0(s.i_cnt_en & (s.i_trap | rd_wen))
            s.o_wen1(s.i_cnt_en & (s.i_trap | s.i_csr_en))

            """
            ********** Read side ***********
            """

            # 0 : RS1
            # 1 : RS2 / CSR

            s.o_rreg0(Concat(bv(1,0b0), s.i_rs1_raddr))

            """
            The address of the second read port (o_rreg1) can get assigned from four
            different sources

            Normal operations : i_rs2_raddr
            CSR access        : i_csr_addr
            trap              : MTVEC
            mret              : MEPC

            Address 0-31 in the RF are assigned to the GPRs. After that follows the four
            CSRs on addresses 32-35

            32 MSCRATCH
            33 MTVEC
            34 MEPC
            35 MTVAL

            The expression below is an optimized version of this logic
            """

            sel_rs2 = s._sig("sel_rs2")
            sel_rs2(~(s.i_trap | s.i_mret | s.i_csr_en))

            s.o_rreg1(Concat(~sel_rs2,
		                    s.i_rs2_raddr[5:2] & replicate(3,sel_rs2),
		                    Concat(bv(1,0b0),s.i_trap) | 
                            Concat(s.i_mret,bv(1,0b0)) | 
                            (replicate(2,s.i_csr_en) & s.i_csr_addr) | 
                            (replicate(2,sel_rs2) & s.i_rs2_raddr[2:0])))

            s.o_rs1(s.i_rdata0)
            s.o_rs2(s.i_rdata1)
            s.o_csr(s.i_rdata1 & replicate(W,s.i_csr_en))
            s.o_csr_pc(s.i_rdata1)

        else:
            rd = s._sig("rd", dtype=Bits(W))
            rd( s.i_ctrl_rd |
                s.i_alu_rd  & replicate(W,s.i_rd_alu_en) |
                s.i_mem_rd  & replicate(W,s.i_rd_mem_en))
            
            s.o_wdata0(rd)
            s.o_wdata1(replicate(W, bv(1,0b0)))

            s.o_wreg0(s.i_rd_waddr)
            s.o_wreg1(bv(5,0))
            
            s.o_wen0(s.i_cnt_en & rd_wen)
            s.o_wen1(bv(1,0b0))

            """
            ********** Read side ***********
            """

            s.o_rreg0(s.i_rs1_raddr)
            s.o_rreg1(s.i_rs2_raddr)

            s.o_rs1(s.i_rdata0)
            s.o_rs2(s.i_rdata1)
            s.o_csr(replicate(W,bv(1,0b0)))
            s.o_csr_pc(replicate(W, bv(1,0b0)))

        
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_rf_if(), serializer_cls=VerilogSerializer))
    