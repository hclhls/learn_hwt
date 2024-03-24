#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal

class serv_alu(Unit):
    def _config(self):
        self.W = Param(1)
        self.B = Param(self.W-1)

    def _declr(self):
        self.clk    = Clk()
   
        with self._associated(clk=self.clk):
            # State
            self.i_en   = Signal()
            self.i_cnt0 = Signal()
            self.o_cmp  = Signal()._m()
            # Control
            self.i_sub      = Signal()
            self.i_bool_op  = VectSignal(2)
            self.i_cmp_eq   = Signal()
            self.i_cmp_sig  = Signal()
            self.i_rd_sel   = VectSignal(3)
            #Data
            self.i_rs1      = VectSignal(self.W)
            self.i_op_b     = VectSignal(self.W)
            self.i_buf      = VectSignal(self.W)
            self.o_rd       = VectSignal(self.W)._m()

        self._make_association()

    def _impl(self):
        B = self.B
        W = self.W
        
        i_en, i_cnt0, o_cmp, i_sub, i_bool_op, i_cmp_eq, i_cmp_sig, i_rd_sel, i_rs1, i_op_b, i_buf, o_rd = \
            self.i_en, self.i_cnt0, self.o_cmp, self.i_sub, self.i_bool_op, self.i_cmp_eq, self.i_cmp_sig,\
            self.i_rd_sel, self.i_rs1, self.i_op_b, self.i_buf, self.o_rd 
        
        result_add = self._sig("result_add",dtype=Bits(W))
        result_slt = self._sig("result_slt",dtype=Bits(W))

        cmp_r = self._reg("cmp_r")

        add_cy   = self._sig("add_cy",)
        add_cy_r = self._reg("add_cy_r",dtype=Bits(W))

        #Sign-extended operands
        rs1_sx  = self._sig("rs1_sx" )
        rs1_sx(i_rs1[B]  & i_cmp_sig)
        op_b_sx = self._sig("op_b_sx")
        op_b_sx(i_op_b[B] & i_cmp_sig)

        add_b = self._sig("add_b", dtype=Bits(W))
        add_b(i_op_b^replicate(W,i_sub))

        add_cy_result_add = add_cy._concat(result_add)
        add_cy_result_add_type = add_cy_result_add._dtype
        add_cy_result_add(i_rs1._reinterpret_cast(add_cy_result_add_type)+
                          add_b._reinterpret_cast(add_cy_result_add_type)+
                          add_cy_r._reinterpret_cast(add_cy_result_add_type))

        result_lt = self._sig("result_lt")
        result_lt(rs1_sx + (~op_b_sx) + add_cy)

        result_eq = self._sig("result_eq")
        result_eq((result_add._eq(0)) & (cmp_r | i_cnt0))

        o_cmp(i_cmp_eq._ternary(result_eq,result_lt))
        
        """
        The result_bool expression implements the following operations between
        i_rs1 and i_op_b depending on the value of i_bool_op

        00 xor
        01 0
        10 or
        11 and

        i_bool_op will be 01 during shift operations, so by outputting zero under
        this condition we can safely or result_bool with i_buf
        """
        result_bool = self._sig("result_bool", dtype=Bits(W))
        result_bool((i_rs1 ^ i_op_b) & (~replicate(W,i_bool_op[0])) | (replicate(W,i_bool_op[1]) & i_op_b & i_rs1))

        result_slt[0](cmp_r & i_cnt0)

        if W>1:
            result_slt[W:1](replicate(B,0))
   

        o_rd(i_buf | (replicate(W,i_rd_sel[0]) & result_add) |  
                     (replicate(W,i_rd_sel[1]) & result_slt) | 
                     (replicate(W,i_rd_sel[2]) & result_bool))

        CodeBlock(
            add_cy_r(replicate(W,0)),
            If(i_en._isOn(),
                add_cy_r[0](add_cy),
                cmp_r(o_cmp)
            ).Else(
                add_cy_r[0](i_sub)
            ) 
        )
             

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_alu(), serializer_cls=VerilogSerializer))
    