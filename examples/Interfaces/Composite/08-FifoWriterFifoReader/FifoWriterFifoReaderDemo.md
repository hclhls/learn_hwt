# Arithmetic

HWT python source:

```python

from hwt.code import FsmBuilder, If, Switch, CodeBlock
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import serializeParamsUniq
from hwt.interfaces.std import Signal, VectSignal, FifoWriter, FifoReader
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn, propagateClkRstn
from hwt.synthesizer.rtlLevel.constants import NOT_SPECIFIED
from hwt.math import log2ceil
from hwtLib.mem.fifo import Fifo

@serializeParamsUniq
class FifoSrc(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        self.DEPTH = Param(0)
        self.EXPORT_SIZE = Param(False)
        self.EXPORT_SPACE = Param(False)
        self.INIT_DATA: tuple = Param(())
        self.INIT_DATA_FIRST_WORD = Param(NOT_SPECIFIED)

        self.DURATION = Param(4)

    def _declr(self):
        
        with self._paramsShared():
            self.hs = FifoWriter()._m()

        addClkRstn(self)

    def _impl(self):
        self.wd_cnt  = self._reg(name="wd_cnt",  dtype=Bits(log2ceil(self.DURATION)), def_val=0)
        self.dat_reg = self._reg(name="dat_reg", dtype=Bits(self.DATA_WIDTH), def_val=0)
        
        CodeBlock(
            self.hs.en(0),
            self.hs.data(0), 
            If(~self.hs.wait._isOn(),
                self.wd_cnt(self.wd_cnt+1),
                If(self.wd_cnt._eq(self.DURATION-1),
                    self.hs.en(1),
                    self.hs.data(self.dat_reg),
                    self.dat_reg(self.dat_reg+1)
                )
            )
        )

@serializeParamsUniq
class FifoDst(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        self.DEPTH = Param(0)
        self.EXPORT_SIZE = Param(False)
        self.EXPORT_SPACE = Param(False)
        self.INIT_DATA: tuple = Param(())
        self.INIT_DATA_FIRST_WORD = Param(NOT_SPECIFIED)

    def _declr(self):
        
        with self._paramsShared():
            self.hs = FifoReader()
        
        self.dout = VectSignal(self.DATA_WIDTH)._m()
        self.vld  = Signal()._m()

        addClkRstn(self)

    def _impl(self):
        
        CodeBlock(
            self.hs.en(0),
            self.vld(0),
            self.dout(0),
            If(~self.hs.wait._isOn(),
                self.hs.en(1),
                self.vld(1),
                self.dout(self.hs.data)
            )
        )
        
class FifiWriterFifoReaderDemo(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        self.DEPTH = Param(8)
        self.EXPORT_SIZE = Param(False)
        self.EXPORT_SPACE = Param(False)
        self.INIT_DATA: tuple = Param(())
        self.INIT_DATA_FIRST_WORD = Param(NOT_SPECIFIED)

    def _declr(self):
        addClkRstn(self)

        self.dout = VectSignal(self.DATA_WIDTH)._m()
        self.vld  = Signal()._m()

        with self._paramsShared():
            self.src  = FifoSrc()
            self.fifo = Fifo()
            self.dst  = FifoDst()

        self.src.DURATION = 4

    def _impl(self):
        
        propagateClkRstn(self)
        
        self.fifo.dataIn(self.src.hs)
        self.dst.hs(self.fifo.dataOut)
        self.vld(self.dst.vld)
        self.dout(self.dst.dout)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(FifiWriterFifoReaderDemo(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python FifiWriterFifoReaderDemo.py

```

The generated Verilog:

```verilog
module FifoSrc #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH = 8,
    parameter DURATION = 4,
    parameter EXPORT_SIZE = 0,
    parameter EXPORT_SPACE = 0,
    parameter INIT_DATA = "()",
    parameter INIT_DATA_FIRST_WORD = "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>"
) (
    input wire clk,
    output reg[7:0] hs_data,
    output reg hs_en,
    input wire hs_wait,
    input wire rst_n
);
    reg[7:0] dat_reg = 8'h00;
    reg[7:0] dat_reg_next;
    reg[1:0] wd_cnt = 2'b00;
    reg[1:0] wd_cnt_next;
    always @(dat_reg, hs_wait, wd_cnt) begin: assig_process_dat_reg_next
        hs_en = 1'b0;
        hs_data = 8'h00;
        if (~(hs_wait == 1'b1)) begin
            wd_cnt_next = wd_cnt + 2'b01;
            if (wd_cnt == 2'b11) begin
                hs_en = 1'b1;
                hs_data = dat_reg;
                dat_reg_next = dat_reg + 8'h01;
            end else
                dat_reg_next = dat_reg;
        end else begin
            dat_reg_next = dat_reg;
            wd_cnt_next = wd_cnt;
        end
    end

    always @(posedge clk) begin: assig_process_wd_cnt
        if (rst_n == 1'b0) begin
            wd_cnt <= 2'b00;
            dat_reg <= 8'h00;
        end else begin
            wd_cnt <= wd_cnt_next;
            dat_reg <= dat_reg_next;
        end
    end

    generate if (DATA_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DEPTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DURATION != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SIZE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SPACE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA != "()")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA_FIRST_WORD != "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>")
        $error("%m Generated only for this param value");
    endgenerate

endmodule
//
//    Generic FIFO usually mapped to BRAM.
//
//    :ivar ~.EXPORT_SIZE: parameter, if true "size" signal will be exported
//    :ivar ~.size: optional signal with count of items stored in this fifo
//    :ivar ~.EXPORT_SPACE: parameter, if true "space" signal is exported
//    :ivar ~.space: optional signal with count of items which can be added to this fifo
//
//    .. hwt-autodoc:: _example_Fifo
//
module Fifo #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH = 8,
    parameter EXPORT_SIZE = 0,
    parameter EXPORT_SPACE = 0,
    parameter INIT_DATA = "()",
    parameter INIT_DATA_FIRST_WORD = "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>"
) (
    input wire clk,
    input wire[7:0] dataIn_data,
    input wire dataIn_en,
    output reg dataIn_wait,
    output reg[7:0] dataOut_data,
    input wire dataOut_en,
    output reg dataOut_wait,
    input wire rst_n
);
    reg fifo_read0;
    reg fifo_write;
    reg looped0 = 1'b0;
    reg looped0_next;
    reg[7:0] memory[0:7];
    reg[2:0] read_ptr0 = 3'b000;
    reg[2:0] read_ptr0_next;
    reg[2:0] write_ptr = 3'b000;
    reg[2:0] write_ptr_next;
    always @(looped0, read_ptr0, write_ptr) begin: assig_process_dataIn_wait
        dataIn_wait = write_ptr == read_ptr0 & looped0 == 1'b1;
    end

    always @(posedge clk) begin: assig_process_dataOut_data
        if (fifo_read0)
            dataOut_data <= memory[read_ptr0];
    end

    always @(looped0, read_ptr0, write_ptr) begin: assig_process_dataOut_wait
        dataOut_wait = write_ptr == read_ptr0 & looped0 == 1'b0;
    end

    always @(dataOut_en, looped0, read_ptr0, write_ptr) begin: assig_process_fifo_read0
        fifo_read0 = dataOut_en == 1'b1 & (looped0 == 1'b1 | write_ptr != read_ptr0);
    end

    always @(dataIn_en, looped0, read_ptr0, write_ptr) begin: assig_process_fifo_write
        fifo_write = dataIn_en == 1'b1 & (looped0 == 1'b0 | write_ptr != read_ptr0);
    end

    always @(dataIn_en, dataOut_en, looped0, read_ptr0, write_ptr) begin: assig_process_looped0_next
        if (dataIn_en == 1'b1 & write_ptr == 3'b111)
            looped0_next = 1'b1;
        else if (dataOut_en == 1'b1 & read_ptr0 == 3'b111)
            looped0_next = 1'b0;
        else
            looped0_next = looped0;
    end

    always @(posedge clk) begin: assig_process_memory
        if (fifo_write)
            memory[write_ptr] <= dataIn_data;
    end

    always @(fifo_read0, read_ptr0) begin: assig_process_read_ptr0_next
        if (fifo_read0)
            if (read_ptr0 == 3'b111)
                read_ptr0_next = 3'b000;
            else
                read_ptr0_next = read_ptr0 + 3'b001;
        else
            read_ptr0_next = read_ptr0;
    end

    always @(posedge clk) begin: assig_process_write_ptr
        if (rst_n == 1'b0) begin
            write_ptr <= 3'b000;
            read_ptr0 <= 3'b000;
            looped0 <= 1'b0;
        end else begin
            write_ptr <= write_ptr_next;
            read_ptr0 <= read_ptr0_next;
            looped0 <= looped0_next;
        end
    end

    always @(fifo_write, write_ptr) begin: assig_process_write_ptr_next
        if (fifo_write)
            if (write_ptr == 3'b111)
                write_ptr_next = 3'b000;
            else
                write_ptr_next = write_ptr + 3'b001;
        else
            write_ptr_next = write_ptr;
    end

    generate if (DATA_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DEPTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SIZE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SPACE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA != "()")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA_FIRST_WORD != "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>")
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module FifoDst #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH = 8,
    parameter EXPORT_SIZE = 0,
    parameter EXPORT_SPACE = 0,
    parameter INIT_DATA = "()",
    parameter INIT_DATA_FIRST_WORD = "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>"
) (
    input wire clk,
    output reg[7:0] dout,
    input wire[7:0] hs_data,
    output reg hs_en,
    input wire hs_wait,
    input wire rst_n,
    output reg vld
);
    always @(hs_data, hs_wait) begin: assig_process_dout
        hs_en = 1'b0;
        vld = 1'b0;
        dout = 8'h00;
        if (~(hs_wait == 1'b1)) begin
            hs_en = 1'b1;
            vld = 1'b1;
            dout = hs_data;
        end
    end

    generate if (DATA_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DEPTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SIZE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SPACE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA != "()")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA_FIRST_WORD != "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>")
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module FifiWriterFifoReaderDemo #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH = 8,
    parameter EXPORT_SIZE = 0,
    parameter EXPORT_SPACE = 0,
    parameter INIT_DATA = "()",
    parameter INIT_DATA_FIRST_WORD = "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>"
) (
    input wire clk,
    output wire[7:0] dout,
    input wire rst_n,
    output wire vld
);
    wire sig_dst_clk;
    wire[7:0] sig_dst_dout;
    wire[7:0] sig_dst_hs_data;
    wire sig_dst_hs_en;
    wire sig_dst_hs_wait;
    wire sig_dst_rst_n;
    wire sig_dst_vld;
    wire sig_fifo_clk;
    wire[7:0] sig_fifo_dataIn_data;
    wire sig_fifo_dataIn_en;
    wire sig_fifo_dataIn_wait;
    wire[7:0] sig_fifo_dataOut_data;
    wire sig_fifo_dataOut_en;
    wire sig_fifo_dataOut_wait;
    wire sig_fifo_rst_n;
    wire sig_src_clk;
    wire[7:0] sig_src_hs_data;
    wire sig_src_hs_en;
    wire sig_src_hs_wait;
    wire sig_src_rst_n;
    FifoDst #(
        .DATA_WIDTH(8),
        .DEPTH(8),
        .EXPORT_SIZE(0),
        .EXPORT_SPACE(0),
        .INIT_DATA("()"),
        .INIT_DATA_FIRST_WORD("<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>")
    ) dst_inst (
        .clk(sig_dst_clk),
        .dout(sig_dst_dout),
        .hs_data(sig_dst_hs_data),
        .hs_en(sig_dst_hs_en),
        .hs_wait(sig_dst_hs_wait),
        .rst_n(sig_dst_rst_n),
        .vld(sig_dst_vld)
    );

    Fifo #(
        .DATA_WIDTH(8),
        .DEPTH(8),
        .EXPORT_SIZE(0),
        .EXPORT_SPACE(0),
        .INIT_DATA("()"),
        .INIT_DATA_FIRST_WORD("<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>")
    ) fifo_inst (
        .clk(sig_fifo_clk),
        .dataIn_data(sig_fifo_dataIn_data),
        .dataIn_en(sig_fifo_dataIn_en),
        .dataIn_wait(sig_fifo_dataIn_wait),
        .dataOut_data(sig_fifo_dataOut_data),
        .dataOut_en(sig_fifo_dataOut_en),
        .dataOut_wait(sig_fifo_dataOut_wait),
        .rst_n(sig_fifo_rst_n)
    );

    FifoSrc #(
        .DATA_WIDTH(8),
        .DEPTH(8),
        .DURATION(4),
        .EXPORT_SIZE(0),
        .EXPORT_SPACE(0),
        .INIT_DATA("()"),
        .INIT_DATA_FIRST_WORD("<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>")
    ) src_inst (
        .clk(sig_src_clk),
        .hs_data(sig_src_hs_data),
        .hs_en(sig_src_hs_en),
        .hs_wait(sig_src_hs_wait),
        .rst_n(sig_src_rst_n)
    );

    assign dout = sig_dst_dout;
    assign sig_dst_clk = clk;
    assign sig_dst_hs_data = sig_fifo_dataOut_data;
    assign sig_dst_hs_wait = sig_fifo_dataOut_wait;
    assign sig_dst_rst_n = rst_n;
    assign sig_fifo_clk = clk;
    assign sig_fifo_dataIn_data = sig_src_hs_data;
    assign sig_fifo_dataIn_en = sig_src_hs_en;
    assign sig_fifo_dataOut_en = sig_dst_hs_en;
    assign sig_fifo_rst_n = rst_n;
    assign sig_src_clk = clk;
    assign sig_src_hs_wait = sig_fifo_dataIn_wait;
    assign sig_src_rst_n = rst_n;
    assign vld = sig_dst_vld;
    generate if (DATA_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DEPTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SIZE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (EXPORT_SPACE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA != "()")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA_FIRST_WORD != "<class 'hwt.synthesizer.rtlLevel.constants.NOT_SPECIFIED'>")
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```