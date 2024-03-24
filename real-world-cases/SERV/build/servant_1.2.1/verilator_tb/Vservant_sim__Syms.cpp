// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vservant_sim__Syms.h"
#include "Vservant_sim.h"
#include "Vservant_sim_servant_sim.h"
#include "Vservant_sim_servant__M0_MB8000_S1_W1_C0_A0.h"
#include "Vservant_sim_servant_ram__pi1.h"



// FUNCTIONS
Vservant_sim__Syms::Vservant_sim__Syms(Vservant_sim* topp, const char* namep)
    // Setup locals
    : __Vm_namep(namep)
    , __Vm_activity(false)
    , __Vm_baseCode(0)
    , __Vm_didInit(false)
    // Setup submodule names
    , TOP__servant_sim(Verilated::catName(topp->name(), "servant_sim"))
    , TOP__servant_sim__dut(Verilated::catName(topp->name(), "servant_sim.dut"))
    , TOP__servant_sim__dut__ram(Verilated::catName(topp->name(), "servant_sim.dut.ram"))
{
    // Pointer to top level
    TOPp = topp;
    // Setup each module's pointers to their submodules
    TOPp->servant_sim = &TOP__servant_sim;
    TOPp->servant_sim->dut = &TOP__servant_sim__dut;
    TOPp->servant_sim->dut->ram = &TOP__servant_sim__dut__ram;
    // Setup each module's pointer back to symbol table (for public functions)
    TOPp->__Vconfigure(this, true);
    TOP__servant_sim.__Vconfigure(this, true);
    TOP__servant_sim__dut.__Vconfigure(this, true);
    TOP__servant_sim__dut__ram.__Vconfigure(this, true);
    // Setup scopes
    __Vscope_servant_sim__dut__ram.configure(this, name(), "servant_sim.dut.ram", "ram", 0, VerilatedScope::SCOPE_OTHER);
    // Setup export functions
    for (int __Vfinal=0; __Vfinal<2; __Vfinal++) {
        __Vscope_servant_sim__dut__ram.varInsert(__Vfinal,"mem", &(TOP__servant_sim__dut__ram.mem), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,2 ,31,0 ,8191,0);
    }
}
