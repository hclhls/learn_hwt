// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vservant_sim.h for the primary calling header

#ifndef _VSERVANT_SIM_SERVANT_RAM__PI1_H_
#define _VSERVANT_SIM_SERVANT_RAM__PI1_H_  // guard

#include "verilated_heavy.h"
#include "Vservant_sim__Dpi.h"

//==========

class Vservant_sim__Syms;
class Vservant_sim_VerilatedVcd;


//----------

VL_MODULE(Vservant_sim_servant_ram__pi1) {
  public:
    
    // PORTS
    VL_IN8(__PVT__i_wb_clk,0,0);
    VL_IN8(__PVT__i_wb_rst,0,0);
    VL_IN8(__PVT__i_wb_sel,3,0);
    VL_IN8(__PVT__i_wb_we,0,0);
    VL_IN8(__PVT__i_wb_cyc,0,0);
    VL_OUT8(__PVT__o_wb_ack,0,0);
    VL_IN16(__PVT__i_wb_adr,14,2);
    VL_IN(__PVT__i_wb_dat,31,0);
    VL_OUT(__PVT__o_wb_rdt,31,0);
    
    // LOCAL SIGNALS
    CData/*3:0*/ __PVT__we;
    IData/*31:0*/ mem[8192];
    
    // INTERNAL VARIABLES
  private:
    Vservant_sim__Syms* __VlSymsp;  // Symbol table
  public:
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vservant_sim_servant_ram__pi1);  ///< Copying not allowed
  public:
    Vservant_sim_servant_ram__pi1(const char* name = "TOP");
    ~Vservant_sim_servant_ram__pi1();
    
    // INTERNAL METHODS
    void __Vconfigure(Vservant_sim__Syms* symsp, bool first);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _sequent__TOP__servant_sim__dut__ram__1(Vservant_sim__Syms* __restrict vlSymsp);
    static void _settle__TOP__servant_sim__dut__ram__2(Vservant_sim__Syms* __restrict vlSymsp);
  private:
    static void traceInit(void* userp, VerilatedVcd* tracep, uint32_t code) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard
