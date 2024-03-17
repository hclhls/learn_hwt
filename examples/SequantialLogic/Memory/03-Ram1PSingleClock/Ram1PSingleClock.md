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

class Ram1PSingleClock(Unit):
    
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(32)
        self.PORT_CNT   = Param(1)
        self.HAS_BE     = Param(False)
        self.MAX_BLOCK_DATA_WIDTH = Param(None)
        self.INIT_DATA = Param(None)

    def _declr(self):
        self.addr    = Signal(Bits(8))
        self.din     = Signal(Bits(32))
        self.dout    = Signal(Bits(32))._m()
        self.en      = Signal()
        self.we      = Signal()
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

        ram.port_0.addr(addr)
        ram.port_0.din(din)
        ram.port_0.en(en)
        ram.port_0.we(we)
        dout(ram.port_0.dout)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Ram1PSingleClock(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python Ram1PSingleClock.py

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
    parameter DATA_WIDTH = 32,
    parameter HAS_BE = 0,
    parameter INIT_DATA = "None",
    parameter MAX_BLOCK_DATA_WIDTH = "None",
    parameter PORT_CNT = 1
) (
    input wire clk,
    input wire[7:0] port_0_addr,
    input wire[31:0] port_0_din,
    output reg[31:0] port_0_dout,
    input wire port_0_en,
    input wire port_0_we
);
    reg[31:0] ram_memory[0:255];
    always @(posedge clk) begin: assig_process_port_0_dout
        if (port_0_en) begin
            if (port_0_we)
                ram_memory[port_0_addr] <= port_0_din;
            port_0_dout <= ram_memory[port_0_addr];
        end else
            port_0_dout <= 32'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    end

    generate if (ADDR_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 32)
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

    generate if (PORT_CNT != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module Ram1PSingleClock #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 32,
    parameter HAS_BE = 0,
    parameter INIT_DATA = "None",
    parameter MAX_BLOCK_DATA_WIDTH = "None",
    parameter PORT_CNT = 1
) (
    input wire[7:0] addr,
    input wire clk,
    input wire[31:0] din,
    output wire[31:0] dout,
    input wire en,
    input wire rst_n,
    input wire we
);
    wire sig_ram_clk;
    wire[7:0] sig_ram_port_0_addr;
    wire[31:0] sig_ram_port_0_din;
    wire[31:0] sig_ram_port_0_dout;
    wire sig_ram_port_0_en;
    wire sig_ram_port_0_we;
    RamSingleClock #(
        .ADDR_WIDTH(8),
        .DATA_WIDTH(32),
        .HAS_BE(0),
        .INIT_DATA("None"),
        .MAX_BLOCK_DATA_WIDTH("None"),
        .PORT_CNT(1)
    ) ram_inst (
        .clk(sig_ram_clk),
        .port_0_addr(sig_ram_port_0_addr),
        .port_0_din(sig_ram_port_0_din),
        .port_0_dout(sig_ram_port_0_dout),
        .port_0_en(sig_ram_port_0_en),
        .port_0_we(sig_ram_port_0_we)
    );

    assign dout = sig_ram_port_0_dout;
    assign sig_ram_clk = clk;
    assign sig_ram_port_0_addr = addr;
    assign sig_ram_port_0_din = din;
    assign sig_ram_port_0_en = en;
    assign sig_ram_port_0_we = we;
    generate if (ADDR_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 32)
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

    generate if (PORT_CNT != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule


```