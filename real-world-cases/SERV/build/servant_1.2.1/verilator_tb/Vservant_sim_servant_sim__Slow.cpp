// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vservant_sim.h for the primary calling header

#include "Vservant_sim_servant_sim.h"
#include "Vservant_sim__Syms.h"

#include "verilated_dpi.h"

//==========

VL_CTOR_IMP(Vservant_sim_servant_sim) {
    VL_CELL(dut, Vservant_sim_servant__M0_MB8000_S1_W1_C0_A0);
    // Reset internal values
    // Reset structure values
    _ctor_var_reset();
}

void Vservant_sim_servant_sim::__Vconfigure(Vservant_sim__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
}

Vservant_sim_servant_sim::~Vservant_sim_servant_sim() {
}

void Vservant_sim_servant_sim::_initial__TOP__servant_sim__1(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vservant_sim_servant_sim::_initial__TOP__servant_sim__1\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Variables
    WData/*95:0*/ __Vtemp1[3];
    // Body
    __Vtemp1[0U] = 0x653d2573U;
    __Vtemp1[1U] = 0x6d776172U;
    __Vtemp1[2U] = 0x666972U;
    if (VL_UNLIKELY(VL_VALUEPLUSARGS_INW(1024,VL_CVT_PACK_STR_NW(3, __Vtemp1),
                                         vlSymsp->TOP__servant_sim.__PVT__firmware_file))) {
        VL_WRITEF("Loading RAM from %0s\n",1024,vlSymsp->TOP__servant_sim.__PVT__firmware_file);
        VL_READMEM_N(true, 32, 8192, 0, VL_CVT_PACK_STR_NW(32, vlSymsp->TOP__servant_sim.__PVT__firmware_file)
                     , vlSymsp->TOP__servant_sim__dut__ram.mem
                     , 0, ~0ULL);
    }
}

void Vservant_sim_servant_sim::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vservant_sim_servant_sim::_ctor_var_reset\n"); );
    // Body
    wb_clk = VL_RAND_RESET_I(1);
    wb_rst = VL_RAND_RESET_I(1);
    pc_adr = VL_RAND_RESET_I(32);
    pc_vld = VL_RAND_RESET_I(1);
    q = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(1024, __PVT__firmware_file);
}
