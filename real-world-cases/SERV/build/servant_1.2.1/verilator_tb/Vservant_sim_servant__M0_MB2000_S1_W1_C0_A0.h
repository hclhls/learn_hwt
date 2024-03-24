// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vservant_sim.h for the primary calling header

#ifndef _VSERVANT_SIM_SERVANT__M0_MB2000_S1_W1_C0_A0_H_
#define _VSERVANT_SIM_SERVANT__M0_MB2000_S1_W1_C0_A0_H_  // guard

#include "verilated_heavy.h"
#include "Vservant_sim__Dpi.h"

//==========

class Vservant_sim__Syms;
class Vservant_sim_VerilatedVcd;
class Vservant_sim_servant_ram__pi1;


//----------

VL_MODULE(Vservant_sim_servant__M0_MB2000_S1_W1_C0_A0) {
  public:
    // CELLS
    Vservant_sim_servant_ram__pi1* ram;
    
    // PORTS
    VL_IN8(__PVT__wb_clk,0,0);
    VL_IN8(__PVT__wb_rst,0,0);
    VL_OUT8(__PVT__q,0,0);
    
    // LOCAL SIGNALS
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ __PVT__timer_irq;
        CData/*0:0*/ __PVT__wb_mem_stb;
        CData/*0:0*/ __PVT__wb_gpio_rdt;
        CData/*0:0*/ __PVT__wb_ext_stb;
        CData/*0:0*/ __PVT__wb_ext_ack;
        CData/*1:0*/ __PVT__rf_rdata;
        CData/*1:0*/ __PVT__rf_ram__DOT__rdata;
        CData/*0:0*/ __PVT__rf_ram__DOT__regzero;
        CData/*0:0*/ __PVT__cpu__DOT__wb_ibus_ack;
        CData/*3:0*/ __PVT__cpu__DOT__wb_dbus_sel;
        CData/*0:0*/ __PVT__cpu__DOT__wb_dbus_stb;
        CData/*0:0*/ __PVT__cpu__DOT__wb_dbus_ack;
        CData/*0:0*/ __PVT__cpu__DOT__rf_wreq;
        CData/*0:0*/ __PVT__cpu__DOT__rf_rreq;
        CData/*0:0*/ __PVT__cpu__DOT__rdata1;
        CData/*0:0*/ __PVT__cpu__DOT__mux__DOT__sig_en;
        CData/*0:0*/ __PVT__cpu__DOT__mux__DOT__halt_en;
        CData/*0:0*/ __PVT__cpu__DOT__mux__DOT__sim_ack;
        CData/*0:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__rgnt;
        CData/*4:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__rcnt;
        CData/*0:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__rtrig1;
        CData/*1:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__wdata0_r;
        CData/*2:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__wdata1_r;
        CData/*0:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__wen0_r;
        CData/*0:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__wen1_r;
        CData/*1:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__rdata0;
        CData/*0:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__rdata1;
        CData/*0:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__rgate;
        CData/*0:0*/ __PVT__cpu__DOT__rf_ram_if__DOT__rreq_r;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl_pc_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__jump;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__imm;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__trap;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__init;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__cnt_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__cnt0;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__cnt1;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__cnt2;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__cnt3;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__cnt_done;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg_q;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg2_q;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__alu_cmp;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__op_b;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__mem_misalign;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__new_irq;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__wb_ibus_cyc;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__state__DOT__stage_two_req;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__state__DOT__init_done;
        CData/*2:0*/ __PVT__cpu__DOT__cpu__DOT__state__DOT__o_cnt;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__state__DOT__ibus_cyc;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__state__DOT__take_branch;
        CData/*3:0*/ __PVT__cpu__DOT__cpu__DOT__state__DOT__gen_cnt_w_eq_1__DOT__cnt_lsb;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__state__DOT__gen_csr__DOT__misalign_trap_sync_r;
        CData/*4:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__opcode;
        CData/*2:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__funct3;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__op20;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__op21;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__op22;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__op26;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__imm25;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__imm30;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_two_stage_op;
    };
    struct {
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_shift_op;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_dbus_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_bufreg_rs1_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_ctrl_utype;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_rd_op;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__csr_op;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_ctrl_mret;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_e_op;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_alu_sub;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_csr_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_csr_mstatus_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_csr_mcause_en;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_csr_imm_en;
        CData/*1:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_csr_addr;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_alu_cmp_sig;
        CData/*3:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_immdec_ctrl;
        CData/*3:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_immdec_en;
        CData/*2:0*/ __PVT__cpu__DOT__cpu__DOT__decode__DOT__co_alu_rd_sel;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__immdec__DOT__imm31;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__immdec__DOT__imm7;
        CData/*5:0*/ __PVT__cpu__DOT__cpu__DOT__immdec__DOT__imm30_25;
        CData/*4:0*/ __PVT__cpu__DOT__cpu__DOT__immdec__DOT__imm24_20;
        CData/*4:0*/ __PVT__cpu__DOT__cpu__DOT__immdec__DOT__imm11_7;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__immdec__DOT__signbit;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg__DOT__c;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg__DOT__q;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg__DOT__c_r;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg__DOT__clr_lsb;
        CData/*5:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg2__DOT__dat_shamt;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__pc_plus_4;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__pc_plus_4_cy;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__pc_plus_4_cy_r;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__pc_plus_offset_cy;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__pc_plus_offset_cy_r;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__pc_plus_offset_aligned;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__offset_a;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__ctrl__DOT__offset_b;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__alu__DOT__result_add;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__alu__DOT__cmp_r;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__alu__DOT__add_cy;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__alu__DOT__add_cy_r;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__alu__DOT__add_b;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__rf_if__DOT__gen_csr__DOT__rd;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__rf_if__DOT__gen_csr__DOT__sel_rs2;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__mem_if__DOT__signbit;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__mem_if__DOT__dat_valid;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__mstatus_mie;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__mstatus_mpie;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__mie_mtie;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__mcause31;
        CData/*3:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__mcause3_0;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__csr_in;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__csr_out;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__timer_irq_r;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__d;
        CData/*0:0*/ __PVT__cpu__DOT__cpu__DOT__gen_csr__DOT__csr__DOT__timer_irq;
        SData/*9:0*/ __PVT__rf_waddr;
        SData/*9:0*/ __PVT__rf_raddr;
        SData/*8:0*/ __PVT__cpu__DOT__cpu__DOT__immdec__DOT__imm19_12_20;
        IData/*31:0*/ __PVT__wb_mem_adr;
        IData/*31:0*/ __PVT__timer__DOT__mtime;
        IData/*31:0*/ __PVT__timer__DOT__mtimecmp;
        WData/*1023:0*/ __PVT__cpu__DOT__mux__DOT__genblk1__DOT__signature_file[32];
        IData/*31:0*/ __PVT__cpu__DOT__mux__DOT__genblk1__DOT__f;
    };
    struct {
        IData/*31:0*/ __PVT__cpu__DOT__cpu__DOT__wb_ibus_adr;
        IData/*31:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg__DOT__data;
        IData/*31:0*/ __PVT__cpu__DOT__cpu__DOT__bufreg2__DOT__dat;
        CData/*1:0*/ __PVT__rf_ram__DOT__memory[576];
    };
    
    // LOCAL VARIABLES
    CData/*1:0*/ rf_ram__DOT____Vlvbound1;
    IData/*31:0*/ __Vdly__cpu__DOT__cpu__DOT__bufreg2__DOT__dat;
    
    // INTERNAL VARIABLES
  private:
    Vservant_sim__Syms* __VlSymsp;  // Symbol table
  public:
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(Vservant_sim_servant__M0_MB2000_S1_W1_C0_A0);  ///< Copying not allowed
  public:
    Vservant_sim_servant__M0_MB2000_S1_W1_C0_A0(const char* name = "TOP");
    ~Vservant_sim_servant__M0_MB2000_S1_W1_C0_A0();
    
    // INTERNAL METHODS
    void __Vconfigure(Vservant_sim__Syms* symsp, bool first);
    static void _combo__TOP__servant_sim__dut__5(Vservant_sim__Syms* __restrict vlSymsp);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _initial__TOP__servant_sim__dut__3(Vservant_sim__Syms* __restrict vlSymsp) VL_ATTR_COLD;
    static void _sequent__TOP__servant_sim__dut__1(Vservant_sim__Syms* __restrict vlSymsp);
    static void _sequent__TOP__servant_sim__dut__2(Vservant_sim__Syms* __restrict vlSymsp);
    static void _settle__TOP__servant_sim__dut__4(Vservant_sim__Syms* __restrict vlSymsp) VL_ATTR_COLD;
  private:
    static void traceInit(void* userp, VerilatedVcd* tracep, uint32_t code) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

//----------


#endif  // guard
