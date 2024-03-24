// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vservant_sim.h for the primary calling header

#ifndef _VSERVANT_SIM_SERVANT_SIM_H_
#define _VSERVANT_SIM_SERVANT_SIM_H_  // guard

#include "verilated_heavy.h"
#include "Vservant_sim__Dpi.h"

//==========

class Vservant_sim__Syms;
class Vservant_sim_VerilatedVcd;
class Vservant_sim_servant__M0_MB8000_S1_W1_C0_A0;


//----------

VL_MODULE(Vservant_sim_servant_sim) {
  public:
    // CELLS
    Vservant_sim_servant__M0_MB8000_S1_W1_C0_A0* dut;
    
    // PORTS
    VL_IN8(wb_clk,0,0);
    VL_IN8(wb_rst,0,0);
    VL_OUT8(pc_vld,0,0);
    VL_OUT8(q,0,0);
    VL_OUT(pc_adr,31,0);
    
    // LOCAL SIGNALS
    WData/*1023:0*/ __PVT__firmware_file[32];
    
    // INTERNAL VARIABLES
  private:
    Vservant_sim__Syms* __VlSymsp;  // Symbol table
  public:
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vservant_sim_servant_sim);  ///< Copying not allowed
  public:
    Vservant_sim_servant_sim(const char* name = "TOP");
    ~Vservant_sim_servant_sim();
    
    // INTERNAL METHODS
    void __Vconfigure(Vservant_sim__Syms* symsp, bool first);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _initial__TOP__servant_sim__1(Vservant_sim__Syms* __restrict vlSymsp) VL_ATTR_COLD;
  private:
    static void traceInit(void* userp, VerilatedVcd* tracep, uint32_t code) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard
