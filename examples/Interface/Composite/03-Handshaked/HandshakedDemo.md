# Arithmetic

HWT python source:

```python

from hwt.code import If, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, Handshaked
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class HandshakedSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = Handshaked()._m()
        
        addClkRstn(self)

    def _impl(self):
        self.vld_reg  = self._reg(name="vld_reg", dtype=Bits(1), def_val=0)
        self.cnt_val  = self._reg(name="cnt_val", dtype=Bits(4), def_val=0)

        self.hs.data(self.cnt_val)
        self.hs.vld(self.vld_reg)

        If(self.hs.rd._isOn(),
            self.cnt_val(self.cnt_val+1),
            self.vld_reg(0)
        ).Else(
            self.vld_reg(1)
        )

@serializeParamsUniq
class HandshakedDst(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = Handshaked()
        self.target_reached = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        self.target_reg = self._reg(name="target_reg", dtype=Bits(1), def_val=0)

        self.target_reached(self.target_reg)

        CodeBlock(
            self.target_reg(0),
            If(self.hs.vld._isOn(),
                self.hs.rd(1),
                If(self.hs.data._eq(self.TARGET),
                    self.target_reg(1)
                )
            ).Else(
                self.hs.rd(0)
            )
        )


class HandshakedDemo(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.target_reached = Signal()._m()

        with self._paramsShared():
            self.src = HandshakedSrc()
            self.dst = HandshakedDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.target_reached(self.dst.target_reached)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(HandshakedDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python HandshakedDemo.py

```

The generated Verilog:

```verilog
module HandshakedSrc #(
    parameter DATA_WIDTH = 4
) (
    input wire clk,
    output wire[3:0] hs_data,
    input wire hs_rd,
    output wire hs_vld,
    input wire rst_n
);
    reg[3:0] cnt_val = 4'h0;
    reg[3:0] cnt_val_next;
    reg vld_reg = 1'b0;
    reg vld_reg_next;
    always @(cnt_val, hs_rd) begin: assig_process_cnt_val_next
        if (hs_rd == 1'b1) begin
            cnt_val_next = cnt_val + 4'h1;
            vld_reg_next = 1'b0;
        end else begin
            vld_reg_next = 1'b1;
            cnt_val_next = cnt_val;
        end
    end

    assign hs_data = cnt_val;
    assign hs_vld = vld_reg;
    always @(posedge clk) begin: assig_process_vld_reg
        if (rst_n == 1'b0) begin
            vld_reg <= 1'b0;
            cnt_val <= 4'h0;
        end else begin
            vld_reg <= vld_reg_next;
            cnt_val <= cnt_val_next;
        end
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module HandshakedDst #(
    parameter DATA_WIDTH = 4,
    parameter TARGET = 11
) (
    input wire clk,
    input wire[3:0] hs_data,
    output reg hs_rd,
    input wire hs_vld,
    input wire rst_n,
    output wire target_reached
);
    reg target_reg = 1'b0;
    reg target_reg_next;
    always @(hs_data, hs_vld) begin: assig_process_hs_rd
        target_reg_next = 1'b0;
        if (hs_vld == 1'b1) begin
            hs_rd = 1'b1;
            if (hs_data == 4'hb)
                target_reg_next = 1'b1;
        end else
            hs_rd = 1'b0;
    end

    assign target_reached = target_reg;
    always @(posedge clk) begin: assig_process_target_reg
        if (rst_n == 1'b0)
            target_reg <= 1'b0;
        else
            target_reg <= target_reg_next;
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (TARGET != 11)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module HandshakedDemo #(
    parameter DATA_WIDTH = 4,
    parameter TARGET = 11
) (
    input wire clk,
    input wire rst_n,
    output wire target_reached
);
    wire sig_dst_clk;
    wire[3:0] sig_dst_hs_data;
    wire sig_dst_hs_rd;
    wire sig_dst_hs_vld;
    wire sig_dst_rst_n;
    wire sig_dst_target_reached;
    wire sig_src_clk;
    wire[3:0] sig_src_hs_data;
    wire sig_src_hs_rd;
    wire sig_src_hs_vld;
    wire sig_src_rst_n;
    HandshakedDst #(
        .DATA_WIDTH(4),
        .TARGET(11)
    ) dst_inst (
        .clk(sig_dst_clk),
        .hs_data(sig_dst_hs_data),
        .hs_rd(sig_dst_hs_rd),
        .hs_vld(sig_dst_hs_vld),
        .rst_n(sig_dst_rst_n),
        .target_reached(sig_dst_target_reached)
    );

    HandshakedSrc #(
        .DATA_WIDTH(4)
    ) src_inst (
        .clk(sig_src_clk),
        .hs_data(sig_src_hs_data),
        .hs_rd(sig_src_hs_rd),
        .hs_vld(sig_src_hs_vld),
        .rst_n(sig_src_rst_n)
    );

    assign sig_dst_clk = clk;
    assign sig_dst_hs_data = sig_src_hs_data;
    assign sig_dst_hs_vld = sig_src_hs_vld;
    assign sig_dst_rst_n = rst_n;
    assign sig_src_clk = clk;
    assign sig_src_hs_rd = sig_dst_hs_rd;
    assign sig_src_rst_n = rst_n;
    assign target_reached = sig_dst_target_reached;
    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (TARGET != 11)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```