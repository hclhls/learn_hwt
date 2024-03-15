# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.param import Param
from hwt.interfaces.std import Signal,  Clk, Rst_n
from hwt.hdl.types.bits import Bits
from hwtLib.clocking.cdc import SignalCdcBuilder

class CdcBuilder(Unit):
    def _config(self):
        self.NO_CDC_STAGES = Param(2)

    def _declr(self):
        
        self.i_clk    = Clk()
        self.o_clk    = Clk()

        with self._paramsShared():
            with self._associated(clk=self.i_clk):
                self.i_rstn = Rst_n()
                with self._associated(rst=self.i_rstn):
                    self.a  = Signal()

            with self._associated(clk=self.o_clk):
                self.o_rstn = Rst_n()
                with self._associated(rst=self.o_rstn):
                    self.c  = Signal()._m()

    def _impl(self):
        c_reg = self._reg(name="c_reg", def_val=0, clk=self.i_clk, rst=self.i_rstn)
        c_reg(self.a)
        
        i_domain={"clk":self.i_clk, "rst": self.i_rstn}
        o_domain={"clk":self.o_clk, "rst": self.o_rstn}

        cdc_builder = SignalCdcBuilder(
            c_reg,
            (i_domain["clk"], i_domain["rst"]),
            (o_domain["clk"], o_domain["rst"]),
            reg_init_val=0)
        
        for _ in range(self.NO_CDC_STAGES):
            cdc_builder.add_out_reg()
        
        self.c(cdc_builder.path[-1])

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(CdcBuilder(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
HWT_USE_ASYNC_RESET=True;python CdcBuilder.py;unset HWT_USE_ASYNC_RESET

```

The generated Verilog:

```verilog
module CdcBuilder #(
    parameter NO_CDC_STAGES = 2
) (
    input wire a,
    output wire c,
    input wire i_clk,
    input wire i_rstn,
    input wire o_clk,
    input wire o_rstn
);
    reg c_reg = 1'b0;
    wire c_reg_next;
    reg c_reg_out_reg0 = 1'b0;
    wire c_reg_out_reg0_next;
    reg c_reg_out_reg1 = 1'b0;
    wire c_reg_out_reg1_next;
    assign c = c_reg_out_reg1;
    always @(c_reg_next) begin: assig_process_c_reg
        c_reg <= c_reg_next;
    end

    always @(posedge i_clk, negedge i_rstn) begin: assig_process_c_reg_0
        if (i_rstn == 1'b0)
            c_reg <= 1'b0;
        else
            c_reg <= c_reg_next;
    end

    assign c_reg_next = a;
    always @(c_reg_out_reg0_next) begin: assig_process_c_reg_out_reg0
        c_reg_out_reg0 <= c_reg_out_reg0_next;
    end

    assign c_reg_out_reg0_next = c_reg;
    always @(c_reg_out_reg1_next) begin: assig_process_c_reg_out_reg1
        c_reg_out_reg1 <= c_reg_out_reg1_next;
    end

    always @(posedge o_clk, negedge o_rstn) begin: assig_process_c_reg_out_reg1_0
        if (o_rstn == 1'b0) begin
            c_reg_out_reg1 <= 1'b0;
            c_reg_out_reg0 <= 1'b0;
        end else begin
            c_reg_out_reg1 <= c_reg_out_reg1_next;
            c_reg_out_reg0 <= c_reg_out_reg0_next;
        end
    end

    assign c_reg_out_reg1_next = c_reg_out_reg0;
    generate if (NO_CDC_STAGES != 2)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
set_max_delay -from [get_cells -hier -filter {NAME =~ */c_reg_reg}] -to [get_cells -hier -filter {NAME =~ */c_reg_out_reg0_reg}] -datapath_only 5.000000
set_property ASYNC_REG TRUE [get_cells -hier -filter {NAME =~ */c_reg_out_reg0_reg}]
set_max_delay -from [get_cells -hier -filter {NAME =~ */c_reg_out_reg0_reg}] -to [get_cells -hier -filter {NAME =~ */c_reg_out_reg1_reg}] -datapath_only 5.000000
set_property ASYNC_REG TRUE [get_cells -hier -filter {NAME =~ */c_reg_out_reg1_reg}]


```