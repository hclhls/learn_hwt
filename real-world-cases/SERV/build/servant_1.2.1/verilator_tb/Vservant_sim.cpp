// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vservant_sim.h for the primary calling header

#include "Vservant_sim.h"
#include "Vservant_sim__Syms.h"

#include "verilated_dpi.h"

//==========

void Vservant_sim::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vservant_sim::eval\n"); );
    Vservant_sim__Syms* __restrict vlSymsp = this->__VlSymsp;  // Setup global symbol table
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
#ifdef VL_DEBUG
    // Debug assertions
    _eval_debug_assertions();
#endif  // VL_DEBUG
    // Initialize
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) _eval_initial_loop(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Clock loop\n"););
        vlSymsp->__Vm_activity = true;
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("src/servant_1.2.1/bench/servant_sim.v", 2, "",
                "Verilated model didn't converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

void Vservant_sim::_eval_initial_loop(Vservant_sim__Syms* __restrict vlSymsp) {
    vlSymsp->__Vm_didInit = true;
    _eval_initial(vlSymsp);
    vlSymsp->__Vm_activity = true;
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        _eval_settle(vlSymsp);
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("src/servant_1.2.1/bench/servant_sim.v", 2, "",
                "Verilated model didn't DC converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

VL_INLINE_OPT void Vservant_sim::_sequent__TOP__1(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_sequent__TOP__1\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->q = vlSymsp->TOP__servant_sim__dut.__PVT__q;
    vlTOPp->pc_vld = vlSymsp->TOP__servant_sim__dut__ram.__PVT__o_wb_ack;
}

VL_INLINE_OPT void Vservant_sim::_settle__TOP__3(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_settle__TOP__3\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->pc_adr = vlSymsp->TOP__servant_sim__dut.__PVT__wb_mem_adr;
}

void Vservant_sim::_eval(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_eval\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    if (((IData)(vlTOPp->wb_clk) & (~ (IData)(vlTOPp->__Vclklast__TOP__wb_clk)))) {
        vlSymsp->TOP__servant_sim__dut._sequent__TOP__servant_sim__dut__1(vlSymsp);
        vlTOPp->__Vm_traceActivity[1U] = 1U;
        vlSymsp->TOP__servant_sim__dut__ram._sequent__TOP__servant_sim__dut__ram__1(vlSymsp);
        vlTOPp->_sequent__TOP__1(vlSymsp);
        vlSymsp->TOP__servant_sim__dut._sequent__TOP__servant_sim__dut__2(vlSymsp);
    }
    vlSymsp->TOP__servant_sim__dut._combo__TOP__servant_sim__dut__5(vlSymsp);
    vlTOPp->__Vm_traceActivity[2U] = 1U;
    vlTOPp->_settle__TOP__3(vlSymsp);
    vlSymsp->TOP__servant_sim__dut__ram._settle__TOP__servant_sim__dut__ram__2(vlSymsp);
    // Final
    vlTOPp->__Vclklast__TOP__wb_clk = vlTOPp->wb_clk;
}

VL_INLINE_OPT QData Vservant_sim::_change_request(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_change_request\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    return (vlTOPp->_change_request_1(vlSymsp));
}

VL_INLINE_OPT QData Vservant_sim::_change_request_1(Vservant_sim__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_change_request_1\n"); );
    Vservant_sim* const __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    // Change detection
    QData __req = false;  // Logically a bool
    return __req;
}

#ifdef VL_DEBUG
void Vservant_sim::_eval_debug_assertions() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vservant_sim::_eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((wb_clk & 0xfeU))) {
        Verilated::overWidthError("wb_clk");}
    if (VL_UNLIKELY((wb_rst & 0xfeU))) {
        Verilated::overWidthError("wb_rst");}
}
#endif  // VL_DEBUG
