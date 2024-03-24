# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, VldSynced
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class VldSyncedSrc(Unit):
    def _config(self):
        self.INTERVAL   = Param(8)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = VldSynced()._m()
        
        addClkRstn(self)

    def _impl(self):
        self.cnt_int = self._reg(name="cnt_int", dtype=Bits(4), def_val=self.INTERVAL-1)
        self.cnt_val = self._reg(name="cnt_val", dtype=Bits(4), def_val=0)

        If(self.cnt_int._eq(0),
            self.cnt_int(self.INTERVAL-1),
            self.hs.vld(1),
            self.hs.data(self.cnt_val),
            self.cnt_val(self.cnt_val+1)
        ).Else(
            self.cnt_int(self.cnt_int-1),
            self.hs.vld(0),
            self.hs.data(0)
        )

@serializeParamsUniq
class VldSyncedDst(Unit):
    def _config(self):
        self.INTERVAL   = Param(8)
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = VldSynced()
        self.target_reached = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        self.data_reg = self._reg(name="data_reg", dtype=Bits(4), def_val=0)

        If(self.hs.vld._isOn(),
           self.data_reg(self.hs.data)
        )

        If(self.data_reg._eq(self.TARGET),
            self.target_reached(1)
        ).Else(
            self.target_reached(0)
        )

class VldSyncedDemo(Unit):
    def _config(self):
        self.INTERVAL   = Param(8)
        self.TARGET     = Param(11)
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.target_reached = Signal()._m()

        with self._paramsShared():
            self.src = VldSyncedSrc()
            self.dst = VldSyncedDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.target_reached(self.dst.target_reached)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(VldSyncedDemo(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python VldSyncedDemo.py

```

The generated Verilog:

```verilog
module VldSyncedSrc #(
    parameter DATA_WIDTH = 4,
    parameter INTERVAL = 8
) (
    input wire clk,
    output reg[3:0] hs_data,
    output reg hs_vld,
    input wire rst_n
);
    reg[3:0] cnt_int = 4'h7;
    reg[3:0] cnt_int_next;
    reg[3:0] cnt_val = 4'h0;
    reg[3:0] cnt_val_next;
    always @(cnt_int, cnt_val) begin: assig_process_cnt_int_next
        if (cnt_int == 4'h0) begin
            cnt_int_next = 4'h7;
            hs_vld = 1'b1;
            hs_data = cnt_val;
            cnt_val_next = cnt_val + 4'h1;
        end else begin
            cnt_int_next = cnt_int - 4'h1;
            hs_vld = 1'b0;
            hs_data = 4'h0;
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

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INTERVAL != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module VldSyncedDst #(
    parameter DATA_WIDTH = 4,
    parameter INTERVAL = 8,
    parameter TARGET = 11
) (
    input wire clk,
    input wire[3:0] hs_data,
    input wire hs_vld,
    input wire rst_n,
    output reg target_reached
);
    reg[3:0] data_reg = 4'h0;
    reg[3:0] data_reg_next;
    always @(posedge clk) begin: assig_process_data_reg
        if (rst_n == 1'b0)
            data_reg <= 4'h0;
        else
            data_reg <= data_reg_next;
    end

    always @(data_reg, hs_data, hs_vld) begin: assig_process_data_reg_next
        if (hs_vld == 1'b1)
            data_reg_next = hs_data;
        else
            data_reg_next = data_reg;
    end

    always @(data_reg) begin: assig_process_target_reached
        if (data_reg == 4'hb)
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
module VldSyncedDemo #(
    parameter DATA_WIDTH = 4,
    parameter INTERVAL = 8,
    parameter TARGET = 11
) (
    input wire clk,
    input wire rst_n,
    output wire target_reached
);
    wire sig_dst_clk;
    wire[3:0] sig_dst_hs_data;
    wire sig_dst_hs_vld;
    wire sig_dst_rst_n;
    wire sig_dst_target_reached;
    wire sig_src_clk;
    wire[3:0] sig_src_hs_data;
    wire sig_src_hs_vld;
    wire sig_src_rst_n;
    VldSyncedDst #(
        .DATA_WIDTH(4),
        .INTERVAL(8),
        .TARGET(11)
    ) dst_inst (
        .clk(sig_dst_clk),
        .hs_data(sig_dst_hs_data),
        .hs_vld(sig_dst_hs_vld),
        .rst_n(sig_dst_rst_n),
        .target_reached(sig_dst_target_reached)
    );

    VldSyncedSrc #(
        .DATA_WIDTH(4),
        .INTERVAL(8)
    ) src_inst (
        .clk(sig_src_clk),
        .hs_data(sig_src_hs_data),
        .hs_vld(sig_src_hs_vld),
        .rst_n(sig_src_rst_n)
    );

    assign sig_dst_clk = clk;
    assign sig_dst_hs_data = sig_src_hs_data;
    assign sig_dst_hs_vld = sig_src_hs_vld;
    assign sig_dst_rst_n = rst_n;
    assign sig_src_clk = clk;
    assign sig_src_rst_n = rst_n;
    assign target_reached = sig_dst_target_reached;
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