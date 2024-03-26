#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal
from hwt.interfaces.utils import propagateClk

class serv_immdec(Unit):
    def _config(s):
        s.SHARED_RFADDR_IMM_REGS = Param(1)
        
    def _declr(s):
        
        s.i_clk = Clk()

        with s._associated(clk=s.i_clk):
            # State
            s.i_cnt_en      = Signal()
            s.i_cnt_done    = Signal()
            # Control
            s.i_immdec_en   = Signal(Bits(4))
            s.i_csr_imm_en  = Signal()
            s.i_ctrl        = Signal(Bits(4))
            s.o_rd_addr     = Signal(Bits(5))._m()
            s.o_rs1_addr    = Signal(Bits(5))._m()
            s.o_rs2_addr    = Signal(Bits(5))._m()
            # Data
            s.o_csr_imm     = Signal()._m()
            s.o_imm         = Signal()._m()
            # External
            s.i_wb_en       = Signal()
            s.i_wb_rdt      = Signal(Bits(32-7))

        s._make_association()

    def _impl(s):
        
        s.clk = s.i_clk

        propagateClk(s)

        imm31 = s._reg("imm31")

        imm19_12_20 = s._reg("imm19_12_20", dtype=Bits(9))
        imm7        = s._reg("imm7")
        imm30_25    = s._reg("imm30_25", dtype=Bits(6))
        imm24_20    = s._reg("imm24_20", dtype=Bits(5))
        imm11_7     = s._reg("imm11_7", dtype=Bits(5))

        s.o_csr_imm(imm19_12_20[4])

        signbit = s._sig("signbit")
        signbit(imm31 & ~s.i_csr_imm_en)
		
        if s.SHARED_RFADDR_IMM_REGS !=0 :
            s.o_rs1_addr(imm19_12_20[9:4])
            s.o_rs2_addr(imm24_20)
            s.o_rd_addr(imm11_7)
			
            # CSR immediates are always zero-extended, hence clear the signbit
            If(s.i_wb_en,
			   imm31(s.i_wb_rdt[31-7])
			)

            If(s.i_wb_en | (s.i_cnt_en & s.i_immdec_en[1]),
			    imm19_12_20(s.i_wb_en._ternary(Concat(s.i_wb_rdt[19-6:12-7],s.i_wb_rdt[20-7]) , 
									           Concat(s.i_ctrl[3]._ternary(signbit,imm24_20[0]), imm19_12_20[9:1])))

			)
			
            If(s.i_wb_en | (s.i_cnt_en),
                imm7(s.i_wb_en._ternary(s.i_wb_rdt[7-7],signbit))
            )

            If(s.i_wb_en | (s.i_cnt_en & s.i_immdec_en[3]),
               imm30_25(s.i_wb_en._ternary(s.i_wb_rdt[30-6:25-7], 
                                           Concat(s.i_ctrl[2]._ternary(imm7, s.i_ctrl[1]._ternary(signbit,imm19_12_20[0])), imm30_25[6:1])))
            )

            If(s.i_wb_en | (s.i_cnt_en & s.i_immdec_en[2]),
               imm24_20(s.i_wb_en._ternary(s.i_wb_rdt[24-6:20-7], Concat(imm30_25[0], imm24_20[5:1])))
            )
	      
            If(s.i_wb_en | (s.i_cnt_en & s.i_immdec_en[0]),
               imm11_7(s.i_wb_en._ternary(s.i_wb_rdt[11-6:7-7], Concat(imm30_25[0], imm11_7[5:1])))
            )
            
        else:

            rd_addr  = s._reg("rd_addr", Bits(5))
            rs1_addr = s._reg("rs1_addr", Bits(5))
            rs2_addr = s._reg("rs2_addr", Bits(5))

            s.o_rd_addr(rd_addr)
            s.o_rs1_addr(rs1_addr)
            s.o_rs2_addr(rs2_addr)

            # CSR immediates are always zero-extended, hence clear the signbit
            If(s.i_wb_en,
                imm31(s.i_wb_rdt[31-7]),
	            imm19_12_20(Concat(s.i_wb_rdt[19-6:12-7],s.i_wb_rdt[20-7])),
	            imm7(s.i_wb_rdt[7-7]),
	            imm30_25(s.i_wb_rdt[30-6:25-7]),
	            imm24_20(s.i_wb_rdt[24-6:20-7]),
	            imm11_7(s.i_wb_rdt[11-6:7-7]),

                rd_addr(s.i_wb_rdt[11-6:7-7]),
                rs1_addr(s.i_wb_rdt[19-6:15-7]),
                rs2_addr(s.i_wb_rdt[24-6:20-7])
            )

            If(s.i_cnt_en,
               imm19_12_20(Concat(s.i_ctrl[3]._ternary(signbit,imm24_20[0]), imm19_12_20[9:1])),
               imm7(signbit),
               imm30_25(Concat(s.i_ctrl[2]._ternary(imm7, s.i_ctrl[1]._ternary(signbit,imm19_12_20[0])), imm30_25[6:1])),
               imm24_20(Concat(imm30_25[0], imm24_20[4:1])),
               imm11_7(Concat(imm30_25[0], imm11_7[4:1]))
            )

        s.o_imm(s.i_cnt_done._ternary(signbit, s.i_ctrl[0]._ternary(imm11_7[0],imm24_20[0])))
      

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_immdec(), serializer_cls=VerilogSerializer))
    