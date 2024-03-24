// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vservant_sim.h for the primary calling header

#include "Vservant_sim.h"
#include "Vservant_sim__Syms.h"

#include "verilated_dpi.h"

//==========

VL_CTOR_IMP(Vservant_sim) {
    Vservant_sim__Syms* __restrict vlSymsp = __VlSymsp = new Vservant_sim__Syms(this, name());
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    VL_CELL(servant_sim, Vservant_sim_servant_sim);
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void Vservant_sim::__Vconfigure(Vservant_sim__Syms* vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
    if (false && this->__VlSymsp) {}  // Prevent unused
    Verilated::timeunit(-12);
    Verilated::timeprecision(-12);
}

Vservant_sim::~Vservant_sim() {
    VL_DO_CLEAR(delete __VlSymsp, __VlSymsp = NULL);
}

void Vservant_sim::_settle__TOP__2(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_settle__TOP__2\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->pc_vld = vlSymsp->TOP__servant_sim__dut__ram.__PVT__o_wb_ack;
    vlTOPp->q = vlSymsp->TOP__servant_sim__dut.__PVT__q;
}

void Vservant_sim::_eval_initial(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_eval_initial\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->__Vclklast__TOP__wb_clk = vlTOPp->wb_clk;
    vlSymsp->TOP__servant_sim__dut._initial__TOP__servant_sim__dut__3(vlSymsp);
    vlTOPp->__Vm_traceActivity[2U] = 1U;
    vlTOPp->__Vm_traceActivity[1U] = 1U;
    vlTOPp->__Vm_traceActivity[0U] = 1U;
    vlSymsp->TOP__servant_sim._initial__TOP__servant_sim__1(vlSymsp);
}

void Vservant_sim::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::final\n"); );
    // Variables
    Vservant_sim__Syms* __restrict vlSymsp = this->__VlSymsp;
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void Vservant_sim::_eval_settle(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_eval_settle\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_settle__TOP__2(vlSymsp);
    vlTOPp->__Vm_traceActivity[2U] = 1U;
    vlTOPp->__Vm_traceActivity[1U] = 1U;
    vlTOPp->__Vm_traceActivity[0U] = 1U;
    vlSymsp->TOP__servant_sim__dut._settle__TOP__servant_sim__dut__4(vlSymsp);
    vlTOPp->_settle__TOP__3(vlSymsp);
    vlSymsp->TOP__servant_sim__dut__ram._settle__TOP__servant_sim__dut__ram__2(vlSymsp);
}

void Vservant_sim::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_ctor_var_reset\n"); );
    // Body
    wb_clk = VL_RAND_RESET_I(1);
    wb_rst = VL_RAND_RESET_I(1);
    pc_adr = VL_RAND_RESET_I(32);
    pc_vld = VL_RAND_RESET_I(1);
    q = VL_RAND_RESET_I(1);
    { int __Vi0=0; for (; __Vi0<3; ++__Vi0) {
            __Vm_traceActivity[__Vi0] = VL_RAND_RESET_I(1);
    }}
}
