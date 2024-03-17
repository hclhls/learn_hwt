# Arithmetic

HWT python source:

```python

from hwt.synthesizer.param import Param
from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClk
from hwtLib.mem.ram import RamSingleClock

class Ram2PSingleClock(Unit):
    
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(16)
        self.PORT_CNT   = Param(2)
        self.HAS_BE     = Param(False)
        self.MAX_BLOCK_DATA_WIDTH = Param(None)
        self.INIT_DATA = Param(None)

    def _declr(self):
        self.addr    = HObjList([Signal(Bits(8)) for _ in range(2)])
        self.din     = HObjList([Signal(Bits(16)) for _ in range(2)])
        self.dout    = HObjList([Signal(Bits(16))._m() for _ in range(2)])
        self.en      = HObjList([Signal() for _ in range(2)])
        self.we      = HObjList([Signal() for _ in range(2)])
        addClkRstn(self)

        with self._paramsShared():
            self.ram = RamSingleClock()

    def _impl(self):
        
        addr, din, dout, en, we, ram =  self.addr, \
                                        self.din, \
                                        self.dout, \
                                        self.en, \
                                        self.we, \
                                        self.ram
        
        propagateClk(self)

        for i, port in enumerate(ram.port):
            port.addr(addr[i])
            port.din(din[i])
            port.en(en[i])
            port.we(we[i])
            dout[i](port.dout)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Ram2PSingleClock(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python Ram2PSingleClock.py

```

The generated Verilog:

```verilog
//
//    RAM/ROM with only one clock signal.
//    It can be configured to have arbitrary number of ports.
//    It can also be configured to have write mask or to be composed from multiple smaller memories.
//
//
//    :note: This memory may not be mapped to RAM
//        if synthesis tool consider it to be too small.
//
//    :ivar PORT_CNT: Param which specifies number of ram ports,
//        it can be int or tuple of READ_WRITE, WRITE, READ
//        to specify rw access for each port separately
//    :ivar HAS_BE: Param, if True the write ports will have byte enable signal
//
//    .. hwt-autodoc::
//    
module RamSingleClock #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 16,
    parameter HAS_BE = 0,
    parameter INIT_DATA = "None",
    parameter MAX_BLOCK_DATA_WIDTH = "None",
    parameter PORT_CNT = 2
) (
    input wire clk,
    input wire[7:0] port_0_addr,
    input wire[15:0] port_0_din,
    output reg[15:0] port_0_dout,
    input wire port_0_en,
    input wire port_0_we,
    input wire[7:0] port_1_addr,
    input wire[15:0] port_1_din,
    output reg[15:0] port_1_dout,
    input wire port_1_en,
    input wire port_1_we
);
    reg[15:0] ram_memory[0:255];
    always @(posedge clk) begin: assig_process_port_0_dout
        if (port_0_en) begin
            if (port_0_we)
                ram_memory[port_0_addr] <= port_0_din;
            port_0_dout <= ram_memory[port_0_addr];
        end else
            port_0_dout <= 16'bxxxxxxxxxxxxxxxx;
    end

    always @(posedge clk) begin: assig_process_port_1_dout
        if (port_1_en) begin
            if (port_1_we)
                ram_memory[port_1_addr] <= port_1_din;
            port_1_dout <= ram_memory[port_1_addr];
        end else
            port_1_dout <= 16'bxxxxxxxxxxxxxxxx;
    end

    generate if (ADDR_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 16)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_BE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA != "None")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (MAX_BLOCK_DATA_WIDTH != "None")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (PORT_CNT != 2)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module Ram2PSingleClock #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 16,
    parameter HAS_BE = 0,
    parameter INIT_DATA = "None",
    parameter MAX_BLOCK_DATA_WIDTH = "None",
    parameter PORT_CNT = 2
) (
    input wire[7:0] addr_0,
    input wire[7:0] addr_1,
    input wire clk,
    input wire[15:0] din_0,
    input wire[15:0] din_1,
    output wire[15:0] dout_0,
    output wire[15:0] dout_1,
    input wire en_0,
    input wire en_1,
    input wire rst_n,
    input wire we_0,
    input wire we_1
);
    wire sig_ram_clk;
    wire[7:0] sig_ram_port_0_addr;
    wire[15:0] sig_ram_port_0_din;
    wire[15:0] sig_ram_port_0_dout;
    wire sig_ram_port_0_en;
    wire sig_ram_port_0_we;
    wire[7:0] sig_ram_port_1_addr;
    wire[15:0] sig_ram_port_1_din;
    wire[15:0] sig_ram_port_1_dout;
    wire sig_ram_port_1_en;
    wire sig_ram_port_1_we;
    RamSingleClock #(
        .ADDR_WIDTH(8),
        .DATA_WIDTH(16),
        .HAS_BE(0),
        .INIT_DATA("None"),
        .MAX_BLOCK_DATA_WIDTH("None"),
        .PORT_CNT(2)
    ) ram_inst (
        .clk(sig_ram_clk),
        .port_0_addr(sig_ram_port_0_addr),
        .port_0_din(sig_ram_port_0_din),
        .port_0_dout(sig_ram_port_0_dout),
        .port_0_en(sig_ram_port_0_en),
        .port_0_we(sig_ram_port_0_we),
        .port_1_addr(sig_ram_port_1_addr),
        .port_1_din(sig_ram_port_1_din),
        .port_1_dout(sig_ram_port_1_dout),
        .port_1_en(sig_ram_port_1_en),
        .port_1_we(sig_ram_port_1_we)
    );

    assign dout_0 = sig_ram_port_0_dout;
    assign dout_1 = sig_ram_port_1_dout;
    assign sig_ram_clk = clk;
    assign sig_ram_port_0_addr = addr_0;
    assign sig_ram_port_0_din = din_0;
    assign sig_ram_port_0_en = en_0;
    assign sig_ram_port_0_we = we_0;
    assign sig_ram_port_1_addr = addr_1;
    assign sig_ram_port_1_din = din_1;
    assign sig_ram_port_1_en = en_1;
    assign sig_ram_port_1_we = we_1;
    generate if (ADDR_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 16)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_BE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA != "None")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (MAX_BLOCK_DATA_WIDTH != "None")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (PORT_CNT != 2)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```