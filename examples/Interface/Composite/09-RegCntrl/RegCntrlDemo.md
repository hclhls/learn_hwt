# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, VldSynced, RegCntrl
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class RegCntrlSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        self.INTERVAL   = Param(8)
        self.TARGET     = Param(11)

    def _declr(self):
        with self._paramsShared():
            self.hs = RegCntrl()._m()
        
        self.target_reached = Signal()._m()

        addClkRstn(self)

    def _impl(self):
        self.cnt_int = self._reg(name="cnt_int", dtype=Bits(4), def_val=self.INTERVAL-1)
        self.cnt_val = self._reg(name="cnt_val", dtype=Bits(4), def_val=0)
        
        If(self.hs.din._eq(self.TARGET),
            self.target_reached(1)
        ).Else(
            self.target_reached(0)
        )

        If(self.cnt_int._eq(0),
            self.cnt_int(self.INTERVAL-1),
            self.hs.dout.vld(1),
            self.hs.dout.data(self.cnt_val),
            self.cnt_val(self.cnt_val+1)
        ).Else(
            self.cnt_int(self.cnt_int-1),
            self.hs.dout.vld(0),
            self.hs.dout.data(0)
        )

@serializeParamsUniq
class RegCntrlDst(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)
        

    def _declr(self):
        with self._paramsShared():
            self.hs = RegCntrl()

        addClkRstn(self)

    def _impl(self):
        
        If(self.hs.dout.vld._isOn(),
            self.hs.din(self.hs.dout.data)
        ).Else(
            self.hs.din(0)
        )


class RegCntrlDemo(Unit):
    def _config(self):
        self.INTERVAL   = Param(8)
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.target_reached = Signal()._m()

        with self._paramsShared():
            self.src = RegCntrlSrc()
            self.dst = RegCntrlDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.target_reached(self.src.target_reached)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(RegCntrlDemo(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python RegCntrlDemo.py

```

The generated Verilog:

```verilog
module RegCntrlSrc #(
    parameter DATA_WIDTH = 4,
    parameter INTERVAL = 8,
    parameter TARGET = 11
) (
    input wire clk,
    input wire[3:0] hs_din,
    output reg[3:0] hs_dout_data,
    output reg hs_dout_vld,
    input wire rst_n,
    output reg target_reached
);
    reg[3:0] cnt_int = 4'h7;
    reg[3:0] cnt_int_next;
    reg[3:0] cnt_val = 4'h0;
    reg[3:0] cnt_val_next;
    always @(cnt_int, cnt_val) begin: assig_process_cnt_int_next
        if (cnt_int == 4'h0) begin
            cnt_int_next = 4'h7;
            hs_dout_vld = 1'b1;
            hs_dout_data = cnt_val;
            cnt_val_next = cnt_val + 4'h1;
        end else begin
            cnt_int_next = cnt_int - 4'h1;
            hs_dout_vld = 1'b0;
            hs_dout_data = 4'h0;
            cnt_val_next = cnt_val;
        end
    end

    always @(posedge clk) begin: assig_process_cnt_val
        if (rst_n == 1'b0) begin
            cnt_val <= 4'h0;
            cnt_int <= 4'h7;
        end else begin
            cnt_val <= cnt_val_next;
            cnt_int <= cnt_int_next;
        end
    end

    always @(hs_din) begin: assig_process_target_reached
        if (hs_din == 4'hb)
            target_reached = 1'b1;
        else
            target_reached = 1'b0;
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INTERVAL != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (TARGET != 11)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module RegCntrlDst #(
    parameter DATA_WIDTH = 4
) (
    input wire clk,
    output reg[3:0] hs_din,
    input wire[3:0] hs_dout_data,
    input wire hs_dout_vld,
    input wire rst_n
);
    always @(hs_dout_data, hs_dout_vld) begin: assig_process_hs_din
        if (hs_dout_vld == 1'b1)
            hs_din = hs_dout_data;
        else
            hs_din = 4'h0;
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module RegCntrlDemo #(
    parameter DATA_WIDTH = 4,
    parameter INTERVAL = 8,
    parameter TARGET = 11
) (
    input wire clk,
    input wire rst_n,
    output wire target_reached
);
    wire sig_dst_clk;
    wire[3:0] sig_dst_hs_din;
    wire[3:0] sig_dst_hs_dout_data;
    wire sig_dst_hs_dout_vld;
    wire sig_dst_rst_n;
    wire sig_src_clk;
    wire[3:0] sig_src_hs_din;
    wire[3:0] sig_src_hs_dout_data;
    wire sig_src_hs_dout_vld;
    wire sig_src_rst_n;
    wire sig_src_target_reached;
    RegCntrlDst #(
        .DATA_WIDTH(4)
    ) dst_inst (
        .clk(sig_dst_clk),
        .hs_din(sig_dst_hs_din),
        .hs_dout_data(sig_dst_hs_dout_data),
        .hs_dout_vld(sig_dst_hs_dout_vld),
        .rst_n(sig_dst_rst_n)
    );

    RegCntrlSrc #(
        .DATA_WIDTH(4),
        .INTERVAL(8),
        .TARGET(11)
    ) src_inst (
        .clk(sig_src_clk),
        .hs_din(sig_src_hs_din),
        .hs_dout_data(sig_src_hs_dout_data),
        .hs_dout_vld(sig_src_hs_dout_vld),
        .rst_n(sig_src_rst_n),
        .target_reached(sig_src_target_reached)
    );

    assign sig_dst_clk = clk;
    assign sig_dst_hs_dout_data = sig_src_hs_dout_data;
    assign sig_dst_hs_dout_vld = sig_src_hs_dout_vld;
    assign sig_dst_rst_n = rst_n;
    assign sig_src_clk = clk;
    assign sig_src_hs_din = sig_dst_hs_din;
    assign sig_src_rst_n = rst_n;
    assign target_reached = sig_src_target_reached;
    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INTERVAL != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (TARGET != 11)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```