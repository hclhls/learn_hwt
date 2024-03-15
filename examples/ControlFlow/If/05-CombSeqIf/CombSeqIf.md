# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn

class CombSeqIf(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.s  = Signal()
        self.c  = Signal(self.u8)._m()
        self.d  = Signal(self.u8)._m()
        addClkRstn(self)

    def _impl(self):
        c_reg = self._reg(name="c_reg", dtype=self.u8, def_val=0)

        If(self.s,
            c_reg(self.b),
            self.d(self.a)
        ).Else(
            self.d(self.b)
        )
        self.c(c_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
   
    print(to_rtl_str(CombSeqIf(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python CombSeqIf.py

```

The generated Verilog:

```verilog
module CombSeqIf (
    input wire[7:0] a,
    input wire[7:0] b,
    output wire[7:0] c,
    input wire clk,
    output reg[7:0] d,
    input wire rst_n,
    input wire s
);
    reg[7:0] c_reg = 8'h00;
    reg[7:0] c_reg_next;
    assign c = c_reg;
    always @(posedge clk) begin: assig_process_c_reg
        if (rst_n == 1'b0)
            c_reg <= 8'h00;
        else
            c_reg <= c_reg_next;
    end

    always @(a, b, c_reg, s) begin: assig_process_c_reg_next
        if (s) begin
            c_reg_next = b;
            d = a;
        end else begin
            d = b;
            c_reg_next = c_reg;
        end
    end

endmodule

```