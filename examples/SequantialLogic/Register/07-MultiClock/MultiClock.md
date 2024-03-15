# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal,  Clk, Rst
from hwt.hdl.types.bits import Bits

class MultiClock(Unit):
    
    def _declr(self):
        self.a        = Signal()
        self.c        = Signal()._m()
        self.i_clk    = Clk()
        self.i_rst    = Rst()
        self.o_clk    = Clk()
        self.o_rst    = Rst()

    def _impl(self):
        c_reg0 = self._reg(name="c_reg0", def_val=0, clk=self.i_clk, rst=self.i_rst)
        c_reg1 = self._reg(name="c_reg1", def_val=0, clk=self.o_clk, rst=self.o_rst)
        c_reg2 = self._reg(name="c_reg2", def_val=0, clk=self.o_clk, rst=self.o_rst)
        
        c_reg0(self.a)
        c_reg1(c_reg0)
        c_reg2(c_reg1)
        self.c(c_reg2)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(MultiClock(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python MultiClock.py

```

The generated Verilog:

```verilog
module MultiClock (
    input wire a,
    output wire c,
    input wire i_clk,
    input wire i_rst,
    input wire o_clk,
    input wire o_rst
);
    reg c_reg0 = 1'b0;
    wire c_reg0_next;
    reg c_reg1 = 1'b0;
    wire c_reg1_next;
    reg c_reg2 = 1'b0;
    wire c_reg2_next;
    assign c = c_reg2;
    always @(posedge i_clk) begin: assig_process_c_reg0
        if (i_rst == 1'b1)
            c_reg0 <= 1'b0;
        else
            c_reg0 <= c_reg0_next;
    end

    assign c_reg0_next = a;
    assign c_reg1_next = c_reg0;
    always @(posedge o_clk) begin: assig_process_c_reg2
        if (o_rst == 1'b1) begin
            c_reg2 <= 1'b0;
            c_reg1 <= 1'b0;
        end else begin
            c_reg2 <= c_reg2_next;
            c_reg1 <= c_reg1_next;
        end
    end

    assign c_reg2_next = c_reg1;
endmodule

```