// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vservant_sim.h for the primary calling header

#include "Vservant_sim_servant_ram__pi1.h"
#include "Vservant_sim__Syms.h"

#include "verilated_dpi.h"

//==========

VL_CTOR_IMP(Vservant_sim_servant_ram__pi1) {
    // Reset internal values
    // Reset structure values
    _ctor_var_reset();
}

void Vservant_sim_servant_ram__pi1::__Vconfigure(Vservant_sim__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
}

Vservant_sim_servant_ram__pi1::~Vservant_sim_servant_ram__pi1() {
}

void Vservant_sim_servant_ram__pi1::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vservant_sim_servant_ram__pi1::_ctor_var_reset\n"); );
    // Body
    __PVT__i_wb_clk = VL_RAND_RESET_I(1);
    __PVT__i_wb_rst = VL_RAND_RESET_I(1);
    __PVT__i_wb_adr = VL_RAND_RESET_I(13);
    __PVT__i_wb_dat = VL_RAND_RESET_I(32);
    __PVT__i_wb_sel = VL_RAND_RESET_I(4);
    __PVT__i_wb_we = VL_RAND_RESET_I(1);
    __PVT__i_wb_cyc = VL_RAND_RESET_I(1);
    __PVT__o_wb_rdt = VL_RAND_RESET_I(32);
    __PVT__o_wb_ack = VL_RAND_RESET_I(1);
    __PVT__we = VL_RAND_RESET_I(4);
    { int __Vi0=0; for (; __Vi0<8192; ++__Vi0) {
            mem[__Vi0] = VL_RAND_RESET_I(32);
    }}
}
