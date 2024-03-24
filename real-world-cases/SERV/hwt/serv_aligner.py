#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.code import If, Concat, replicate, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, VectSignal
from hwt.interfaces.utils import addClkRst

class serv_aligner(Unit):
    
    def _declr(self):
        self.DT      = Bits(32)
        self.DT_HALF = Bits(16)

        DT = self.DT
        addClkRst(self)
        # serv_top
        self.i_ibus_adr = Signal(DT)
        self.i_ibus_cyc = Signal()
        self.o_ibus_rdt = Signal(DT)._m()
        self.o_ibus_ack = Signal()._m()
        # serv_rf_top
        self.o_wb_ibus_adr = Signal(DT)._m() 
        self.o_wb_ibus_cyc = Signal()._m()
        self.i_wb_ibus_rdt = Signal(DT)
        self.i_wb_ibus_ack = Signal()

    def _impl(self):
        DT      = self.DT
        DT_HALF = self.DT_HALF

        i_ibus_adr, i_ibus_cyc, o_ibus_rdt, o_ibus_ack, o_wb_ibus_adr, o_wb_ibus_cyc, i_wb_ibus_rdt, i_wb_ibus_ack = \
            self.i_ibus_adr, self.i_ibus_cyc, self.o_ibus_rdt, self.o_ibus_ack,\
            self.o_wb_ibus_adr, self.o_wb_ibus_cyc, self.i_wb_ibus_rdt, self.i_wb_ibus_ack

        ibus_rdt_concat = self._sig("ibus_rdt_concat",dtype=DT)
        ack_en = self._sig("ack_en")

        lower_hw = self._reg("lower_hw",dtype=DT_HALF,def_val=None)
        ctrl_misal = self._reg("ctrl_misal",def_val=0)

        """ 
            From SERV core to Memory

            o_wb_ibus_adr: Carries address of instruction to memory. In case of misaligned access,
            which is caused by pc+2 due to compressed instruction, next instruction is fetched
            by pc+4 and concatenation is done to make the instruction aligned.

            o_wb_ibus_cyc: Simply forwarded from SERV to Memory and is only altered by memory or SERV core.
        """
        o_wb_ibus_adr(ctrl_misal._ternary(i_ibus_adr+0b100,i_ibus_adr))
        o_wb_ibus_cyc(i_ibus_cyc)

        """ 
            From Memory to SERV core

            o_ibus_ack: Instruction bus acknowledge is send to SERV only when the aligned instruction,
            either compressed or un-compressed, is ready to dispatch.

            o_ibus_rdt: Carries the instruction from memory to SERV core. It can be either aligned
            instruction coming from memory or made aligned by two bus transactions and concatenation.
        """

        o_ibus_ack(i_wb_ibus_ack & ack_en)
        o_ibus_rdt(ctrl_misal._ternary(ibus_rdt_concat,i_wb_ibus_rdt))
    
        """ 
            16-bit register used to hold the upper half word of the current instruction in-case
            concatenation will be required with the upper half word of upcoming instruction
        """
        If(i_wb_ibus_ack,
           lower_hw(i_wb_ibus_rdt[i_wb_ibus_rdt._bit_length():i_wb_ibus_rdt._bit_length()//2])
        )

        ibus_rdt_concat(i_wb_ibus_rdt[i_wb_ibus_rdt._bit_length()//2:]._concat(lower_hw))

        """
            Two control signals: ack_en, ctrl_misal are set to control the bus transactions between
            SERV core and the memory
        """
        ack_en(~(i_ibus_adr[1] & ~ctrl_misal))

        If(i_wb_ibus_ack & i_ibus_adr[1],
           ctrl_misal(~ctrl_misal)
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(serv_aligner(), serializer_cls=VerilogSerializer))
    