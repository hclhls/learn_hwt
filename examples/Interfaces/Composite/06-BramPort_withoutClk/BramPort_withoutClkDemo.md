# Arithmetic

HWT python source:

```python

from hwt.code import FsmBuilder, If, Switch, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, VectSignal, BramPort_withoutClk
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.interfaces.utils import addClkRstn, propagateClkRstn
from hwt.math import log2ceil

@serializeParamsUniq
class BramPort_withoutClkSrc(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)
        self.HAS_R      = Param(True)
        self.HAS_W      = Param(True)
        self.HAS_BE     = Param(True)

    def _declr(self):
        assert self.HAS_R and self.HAS_W, "has to have both read and write part"
        assert self.HAS_BE, "has to have byte-enable"

        with self._paramsShared():
            self.hs = BramPort_withoutClk()._m()
        self.read_phase = Signal()._m()
        self.data = VectSignal(self.DATA_WIDTH)._m()
        addClkRstn(self)

    def _impl(self):
        BYTE_NUM  = self.DATA_WIDTH//8
        BYTE_BITS = log2ceil(BYTE_NUM)

        self.addr_reg = self._reg(name="addr_reg", dtype=Bits(self.ADDR_WIDTH+BYTE_BITS),def_val=0)
        self.data_reg = self._reg(name="data_reg", dtype=Bits(self.DATA_WIDTH),def_val=(1<<self.DATA_WIDTH)-1)
        stT = HEnum("st_t", ["write", "read"])

        st = FsmBuilder(self, stT)\
        .Trans(stT.write,
            (self.addr_reg._eq((1<<self.ADDR_WIDTH)-1), stT.read)
        ).Trans(stT.read,
            (self.addr_reg._eq((1<<self.ADDR_WIDTH)-1), stT.write)
        ).stateReg

        CodeBlock(
            self.hs.we(0),
            self.hs.en(0),
            self.read_phase(0),
            self.data(self.hs.dout),
            Switch(st
            ).Case(stT.write,
                self.hs.en(1),
                self.addr_reg(self.addr_reg+1),
                self.data_reg(self.data_reg-1),
                self.hs.addr(self.addr_reg[:BYTE_BITS]),
                self.hs.din(self.data_reg),
                Switch(self.addr_reg[BYTE_BITS:]).add_cases([(i, self.hs.we(1<<i)) for i in range(BYTE_NUM)])
            ).Case(stT.read,
                self.hs.en(1),
                self.read_phase(1),
                self.addr_reg(self.addr_reg+1),
                self.hs.addr(self.addr_reg[:BYTE_BITS])
            )
        )
@serializeParamsUniq
class BramPort_withoutClkDst(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)
        self.HAS_R      = Param(True)
        self.HAS_W      = Param(True)
        self.HAS_BE     = Param(True)

    def _declr(self):
        assert self.HAS_R and self.HAS_W, "has to have both read and write part"
        assert self.HAS_BE, "has to have byte-enable"
        addClkRstn(self)

        with self._paramsShared():
            self.hs = BramPort_withoutClk()
        
    def _impl(self):
        BYTE_NUM  = self.DATA_WIDTH//8
        
        self.mem = self._sig(name="mem", dtype=Bits(self.DATA_WIDTH)[1<<self.ADDR_WIDTH])
    
        If(self.clk._onRisingEdge(),
            self.hs.dout(Bits(self.DATA_WIDTH).from_py(None)),
            If(self.hs.en._eq(1),
                If(self.hs.we._eq(0),
                    self.hs.dout(self.mem[self.hs.addr])
                ).Else(
                    [If(self.hs.we[i]._eq(1),
                        self.mem[self.hs.addr][8*(i+1):8*i](self.hs.din[8*(i+1):8*i])) for i in range(BYTE_NUM)]
                )
            )
        )
        
class BramPort_withoutClkDemo(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(6)
        self.DATA_WIDTH = Param(32)
        self.HAS_R      = Param(True)
        self.HAS_W      = Param(True)
        self.HAS_BE     = Param(True)

    def _declr(self):
        addClkRstn(self)

        self.read_phase = Signal()._m()
        self.dout = VectSignal(self.DATA_WIDTH)._m()

        with self._paramsShared():
            self.src = BramPort_withoutClkSrc()
            self.dst = BramPort_withoutClkDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.read_phase(self.src.read_phase)
        self.dout(self.src.data)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
   
    print(to_rtl_str(BramPort_withoutClkDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python BramPort_withoutClkDemo.py

```

The generated Verilog:

```verilog
module BramPort_withoutClkSrc #(
    parameter ADDR_WIDTH = 6,
    parameter DATA_WIDTH = 32,
    parameter HAS_BE = 1,
    parameter HAS_R = 1,
    parameter HAS_W = 1
) (
    input wire clk,
    output reg[31:0] data,
    output reg[5:0] hs_addr,
    output reg[31:0] hs_din,
    input wire[31:0] hs_dout,
    output reg hs_en,
    output reg[3:0] hs_we,
    output reg read_phase,
    input wire rst_n
);
    reg[7:0] addr_reg = 8'h00;
    reg[7:0] addr_reg_next;
    reg[31:0] data_reg = 32'hffffffff;
    reg[31:0] data_reg_next;
    reg[1:0] st = 0;
    reg[1:0] st_next;
    always @(addr_reg, data_reg, hs_dout, st) begin: assig_process_addr_reg_next
        hs_we = 4'h0;
        hs_en = 1'b0;
        read_phase = 1'b0;
        data = hs_dout;
        case(st)
            0: begin
                hs_en = 1'b1;
                addr_reg_next = addr_reg + 8'h01;
                data_reg_next = data_reg - 32'h00000001;
                hs_addr = addr_reg[7:2];
                hs_din = data_reg;
                case(addr_reg[1:0])
                    2'b00:
                        hs_we = 4'h1;
                    2'b01:
                        hs_we = 4'h2;
                    2'b10:
                        hs_we = 4'h4;
                    2'b11:
                        hs_we = 4'h8;
                endcase
            end
            default: begin
                hs_en = 1'b1;
                read_phase = 1'b1;
                addr_reg_next = addr_reg + 8'h01;
                hs_addr = addr_reg[7:2];
                data_reg_next = data_reg;
            end
        endcase
    end

    always @(posedge clk) begin: assig_process_st
        if (rst_n == 1'b0) begin
            st <= 0;
            data_reg <= 32'hffffffff;
            addr_reg <= 8'h00;
        end else begin
            st <= st_next;
            data_reg <= data_reg_next;
            addr_reg <= addr_reg_next;
        end
    end

    always @(addr_reg, st) begin: assig_process_st_next
        case(st)
            0:
                if (addr_reg == 8'h3f)
                    st_next = 1;
                else
                    st_next = st;
            default:
                if (addr_reg == 8'h3f)
                    st_next = 0;
                else
                    st_next = st;
        endcase
    end

    generate if (ADDR_WIDTH != 6)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 32)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_BE != 1)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_R != 1)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_W != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module BramPort_withoutClkDst #(
    parameter ADDR_WIDTH = 6,
    parameter DATA_WIDTH = 32,
    parameter HAS_BE = 1,
    parameter HAS_R = 1,
    parameter HAS_W = 1
) (
    input wire clk,
    input wire[5:0] hs_addr,
    input wire[31:0] hs_din,
    output reg[31:0] hs_dout,
    input wire hs_en,
    input wire[3:0] hs_we,
    input wire rst_n
);
    reg[31:0] mem[0:63];
    always @(posedge clk) begin: assig_process_hs_dout
        hs_dout <= 32'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
        if (hs_en == 1'b1)
            if (hs_we == 4'h0)
                hs_dout <= mem[hs_addr];
            else begin
                if (hs_we[0] == 1'b1)
                    mem[hs_addr][7:0] <= hs_din[7:0];
                if (hs_we[1] == 1'b1)
                    mem[hs_addr][15:8] <= hs_din[15:8];
                if (hs_we[2] == 1'b1)
                    mem[hs_addr][23:16] <= hs_din[23:16];
                if (hs_we[3] == 1'b1)
                    mem[hs_addr][31:24] <= hs_din[31:24];
            end
    end

    generate if (ADDR_WIDTH != 6)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 32)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_BE != 1)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_R != 1)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_W != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module BramPort_withoutClkDemo #(
    parameter ADDR_WIDTH = 6,
    parameter DATA_WIDTH = 32,
    parameter HAS_BE = 1,
    parameter HAS_R = 1,
    parameter HAS_W = 1
) (
    input wire clk,
    output wire[31:0] dout,
    output wire read_phase,
    input wire rst_n
);
    wire sig_dst_clk;
    wire[5:0] sig_dst_hs_addr;
    wire[31:0] sig_dst_hs_din;
    wire[31:0] sig_dst_hs_dout;
    wire sig_dst_hs_en;
    wire[3:0] sig_dst_hs_we;
    wire sig_dst_rst_n;
    wire sig_src_clk;
    wire[31:0] sig_src_data;
    wire[5:0] sig_src_hs_addr;
    wire[31:0] sig_src_hs_din;
    wire[31:0] sig_src_hs_dout;
    wire sig_src_hs_en;
    wire[3:0] sig_src_hs_we;
    wire sig_src_read_phase;
    wire sig_src_rst_n;
    BramPort_withoutClkDst #(
        .ADDR_WIDTH(6),
        .DATA_WIDTH(32),
        .HAS_BE(1),
        .HAS_R(1),
        .HAS_W(1)
    ) dst_inst (
        .clk(sig_dst_clk),
        .hs_addr(sig_dst_hs_addr),
        .hs_din(sig_dst_hs_din),
        .hs_dout(sig_dst_hs_dout),
        .hs_en(sig_dst_hs_en),
        .hs_we(sig_dst_hs_we),
        .rst_n(sig_dst_rst_n)
    );

    BramPort_withoutClkSrc #(
        .ADDR_WIDTH(6),
        .DATA_WIDTH(32),
        .HAS_BE(1),
        .HAS_R(1),
        .HAS_W(1)
    ) src_inst (
        .clk(sig_src_clk),
        .data(sig_src_data),
        .hs_addr(sig_src_hs_addr),
        .hs_din(sig_src_hs_din),
        .hs_dout(sig_src_hs_dout),
        .hs_en(sig_src_hs_en),
        .hs_we(sig_src_hs_we),
        .read_phase(sig_src_read_phase),
        .rst_n(sig_src_rst_n)
    );

    assign dout = sig_src_data;
    assign read_phase = sig_src_read_phase;
    assign sig_dst_clk = clk;
    assign sig_dst_hs_addr = sig_src_hs_addr;
    assign sig_dst_hs_din = sig_src_hs_din;
    assign sig_dst_hs_en = sig_src_hs_en;
    assign sig_dst_hs_we = sig_src_hs_we;
    assign sig_dst_rst_n = rst_n;
    assign sig_src_clk = clk;
    assign sig_src_hs_dout = sig_dst_hs_dout;
    assign sig_src_rst_n = rst_n;
    generate if (ADDR_WIDTH != 6)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 32)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_BE != 1)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_R != 1)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_W != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```