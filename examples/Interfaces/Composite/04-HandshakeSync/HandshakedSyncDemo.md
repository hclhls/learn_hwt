# Arithmetic

HWT python source:

```python

from hwt.code import If, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, HandshakeSync
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class HandshakeSyncSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = HandshakeSync()._m()
        
        addClkRstn(self)

    def _impl(self):
        self.vld_reg  = self._reg(name="vld_reg", dtype=Bits(1), def_val=0)

        self.hs.vld(self.vld_reg)

        If(self.hs.rd._isOn(),
            self.vld_reg(0)
        ).Else(
            self.vld_reg(1)
        )

@serializeParamsUniq
class HandshakeSyncDst(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = HandshakeSync()
        self.target_reached = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        self.rev_cnt    = self._reg(name="rev_cnt", dtype=Bits(self.DATA_WIDTH), def_val=0)
        self.target_reg = self._reg(name="target_reg", dtype=Bits(1), def_val=0)

        self.target_reached(self.target_reg)

        CodeBlock(
            self.target_reg(0),
            If(self.hs.vld._isOn(),
                self.hs.rd(1),
                self.rev_cnt(self.rev_cnt+1),
                If(self.rev_cnt._eq(self.TARGET),
                    self.target_reg(1)
                )
            ).Else(
                self.hs.rd(0)
            )
        )


class HandshakeSyncDemo(Unit):
    def _config(self):
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.target_reached = Signal()._m()

        with self._paramsShared():
            self.src = HandshakeSyncSrc()
            self.dst = HandshakeSyncDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.target_reached(self.dst.target_reached)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(HandshakeSyncDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python HandshakeSyncDemo.py

```

The generated Verilog:

```verilog
module HandshakeSyncSrc #(
    parameter DATA_WIDTH = 4
) (
    input wire clk,
    input wire hs_rd,
    output wire hs_vld,
    input wire rst_n
);
    reg vld_reg = 1'b0;
    reg vld_reg_next;
    assign hs_vld = vld_reg;
    always @(posedge clk) begin: assig_process_vld_reg
        if (rst_n == 1'b0)
            vld_reg <= 1'b0;
        else
            vld_reg <= vld_reg_next;
    end

    always @(hs_rd) begin: assig_process_vld_reg_next
        if (hs_rd == 1'b1)
            vld_reg_next = 1'b0;
        else
            vld_reg_next = 1'b1;
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module HandshakeSyncDst #(
    parameter DATA_WIDTH = 4,
    parameter TARGET = 11
) (
    input wire clk,
    output reg hs_rd,
    input wire hs_vld,
    input wire rst_n,
    output wire target_reached
);
    reg[3:0] rev_cnt = 4'h0;
    reg[3:0] rev_cnt_next;
    reg target_reg = 1'b0;
    reg target_reg_next;
    always @(hs_vld, rev_cnt) begin: assig_process_hs_rd
        target_reg_next = 1'b0;
        if (hs_vld == 1'b1) begin
            hs_rd = 1'b1;
            rev_cnt_next = rev_cnt + 4'h1;
            if (rev_cnt == 4'hb)
                target_reg_next = 1'b1;
        end else begin
            hs_rd = 1'b0;
            rev_cnt_next = rev_cnt;
        end
    end

    assign target_reached = target_reg;
    always @(posedge clk) begin: assig_process_target_reg
        if (rst_n == 1'b0) begin
            target_reg <= 1'b0;
            rev_cnt <= 4'h0;
        end else begin
            target_reg <= target_reg_next;
            rev_cnt <= rev_cnt_next;
        end
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (TARGET != 11)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module HandshakeSyncDemo #(
    parameter DATA_WIDTH = 4,
    parameter TARGET = 11
) (
    input wire clk,
    input wire rst_n,
    output wire target_reached
);
    wire sig_dst_clk;
    wire sig_dst_hs_rd;
    wire sig_dst_hs_vld;
    wire sig_dst_rst_n;
    wire sig_dst_target_reached;
    wire sig_src_clk;
    wire sig_src_hs_rd;
    wire sig_src_hs_vld;
    wire sig_src_rst_n;
    HandshakeSyncDst #(
        .DATA_WIDTH(4),
        .TARGET(11)
    ) dst_inst (
        .clk(sig_dst_clk),
        .hs_rd(sig_dst_hs_rd),
        .hs_vld(sig_dst_hs_vld),
        .rst_n(sig_dst_rst_n),
        .target_reached(sig_dst_target_reached)
    );

    HandshakeSyncSrc #(
        .DATA_WIDTH(4)
    ) src_inst (
        .clk(sig_src_clk),
        .hs_rd(sig_src_hs_rd),
        .hs_vld(sig_src_hs_vld),
        .rst_n(sig_src_rst_n)
    );

    assign sig_dst_clk = clk;
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