# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn

class SeqElif(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.s  = Signal(Bits[2])
        self.d  = Signal(self.u8)._m()
        addClkRstn(self)

    def _impl(self):
        d_reg = self._reg(name="c_reg", dtype=self.u8, def_val=0)

        If(self.s[0],
            d_reg(self.b)
        ).Elif(self.s[1],
            d_reg(self.c)
        )
        self.d(d_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(SeqIf(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python SeqIf.py

```

The generated Verilog:

```verilog
module SeqIf (
    input wire[7:0] a,
    input wire[7:0] b,
    output wire[7:0] c,
    input wire clk,
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

    always @(b, c_reg, s) begin: assig_process_c_reg_next
        if (s)
            c_reg_next = b;
        else
            c_reg_next = c_reg;
    end

endmodule

```