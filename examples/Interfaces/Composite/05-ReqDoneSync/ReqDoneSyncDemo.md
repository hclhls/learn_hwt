# Arithmetic

HWT python source:

```python

from hwt.code import If, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, ReqDoneSync
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn

@serializeParamsUniq
class ReqDoneSyncSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = ReqDoneSync()._m()
        
        self.done = Signal()._m()

        addClkRstn(self)

    def _impl(self):
        self.req_reg  = self._reg(name="reg_reg",  dtype=Bits(1), def_val=0)
        self.req_wait = self._reg(name="req_wait", dtype=Bits(self.DATA_WIDTH), def_val=(1<<self.DATA_WIDTH)-1)

        self.done(self.hs.done)
        self.hs.req(self.req_reg)

        If(self.hs.done._isOn(),
            self.req_wait((1<<self.DATA_WIDTH)-1),
            self.req_reg(0)
        ).Elif(self.req_wait._eq(0),
            self.req_reg(1)
        ).Else(
            self.req_wait(self.req_wait-1)
        )

@serializeParamsUniq
class ReqDoneSyncDst(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        with self._paramsShared():
            self.hs = ReqDoneSync()
        addClkRstn(self)

    def _impl(self):
        self.done_cnt = self._reg(name="done_cnt", dtype=Bits(self.DATA_WIDTH), def_val=(1<<self.DATA_WIDTH)-1)

        CodeBlock(
            self.hs.done(0),
            If(self.hs.req._isOn(),
                If(self.done_cnt._eq(0),
                    self.hs.done(1)
                ).Else(
                    self.done_cnt(self.done_cnt-1)
                )   
            )
        )

class ReqDoneSyncDemo(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(4)

    def _declr(self):
        addClkRstn(self)
        self.done = Signal()._m()

        with self._paramsShared():
            self.src = ReqDoneSyncSrc()
            self.dst = ReqDoneSyncDst()

    def _impl(self):
        
        propagateClkRstn(self)

        self.dst.hs(self.src.hs)
        self.done(self.src.done)
       
if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(ReqDoneSyncDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python ReqDoneSyncDemo.py

```

The generated Verilog:

```verilog
module ReqDoneSyncSrc #(
    parameter DATA_WIDTH = 4
) (
    input wire clk,
    output wire done,
    input wire hs_done,
    output wire hs_req,
    input wire rst_n
);
    reg reg_reg = 1'b0;
    reg reg_reg_next;
    reg[3:0] req_wait = 4'hf;
    reg[3:0] req_wait_next;
    assign done = hs_done;
    assign hs_req = reg_reg;
    always @(hs_done, reg_reg, req_wait) begin: assig_process_reg_reg_next
        if (hs_done == 1'b1) begin
            req_wait_next = 4'hf;
            reg_reg_next = 1'b0;
        end else if (req_wait == 4'h0) begin
            reg_reg_next = 1'b1;
            req_wait_next = req_wait;
        end else begin
            req_wait_next = req_wait - 4'h1;
            reg_reg_next = reg_reg;
        end
    end

    always @(posedge clk) begin: assig_process_req_wait
        if (rst_n == 1'b0) begin
            req_wait <= 4'hf;
            reg_reg <= 1'b0;
        end else begin
            req_wait <= req_wait_next;
            reg_reg <= reg_reg_next;
        end
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module ReqDoneSyncDst #(
    parameter DATA_WIDTH = 4
) (
    input wire clk,
    output reg hs_done,
    input wire hs_req,
    input wire rst_n
);
    reg[3:0] done_cnt = 4'hf;
    reg[3:0] done_cnt_next;
    always @(posedge clk) begin: assig_process_done_cnt
        if (rst_n == 1'b0)
            done_cnt <= 4'hf;
        else
            done_cnt <= done_cnt_next;
    end

    always @(done_cnt, hs_req) begin: assig_process_done_cnt_next
        hs_done = 1'b0;
        if (hs_req == 1'b1)
            if (done_cnt == 4'h0) begin
                hs_done = 1'b1;
                done_cnt_next = done_cnt;
            end else
                done_cnt_next = done_cnt - 4'h1;
        else
            done_cnt_next = done_cnt;
    end

    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module ReqDoneSyncDemo #(
    parameter DATA_WIDTH = 4
) (
    input wire clk,
    output wire done,
    input wire rst_n
);
    wire sig_dst_clk;
    wire sig_dst_hs_done;
    wire sig_dst_hs_req;
    wire sig_dst_rst_n;
    wire sig_src_clk;
    wire sig_src_done;
    wire sig_src_hs_done;
    wire sig_src_hs_req;
    wire sig_src_rst_n;
    ReqDoneSyncDst #(
        .DATA_WIDTH(4)
    ) dst_inst (
        .clk(sig_dst_clk),
        .hs_done(sig_dst_hs_done),
        .hs_req(sig_dst_hs_req),
        .rst_n(sig_dst_rst_n)
    );

    ReqDoneSyncSrc #(
        .DATA_WIDTH(4)
    ) src_inst (
        .clk(sig_src_clk),
        .done(sig_src_done),
        .hs_done(sig_src_hs_done),
        .hs_req(sig_src_hs_req),
        .rst_n(sig_src_rst_n)
    );

    assign done = sig_src_done;
    assign sig_dst_clk = clk;
    assign sig_dst_hs_req = sig_src_hs_req;
    assign sig_dst_rst_n = rst_n;
    assign sig_src_clk = clk;
    assign sig_src_hs_done = sig_dst_hs_done;
    assign sig_src_rst_n = rst_n;
    generate if (DATA_WIDTH != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```