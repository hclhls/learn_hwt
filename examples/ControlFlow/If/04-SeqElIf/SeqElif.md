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
        self.s  = Signal(Bits(2))
        self.d  = Signal(self.u8)._m()
        addClkRstn(self)

    def _impl(self):
        d_reg = self._reg(name="d_reg", dtype=self.u8, def_val=0)

        If(self.s[0],
            d_reg(self.b)
        ).Elif(self.s[1],
            d_reg(self.c)
        )
        self.d(d_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(SeqElif(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python SeqElif.py

```

The generated Verilog:

```verilog
module SeqElif (
    input wire[7:0] a,
    input wire[7:0] b,
    input wire[7:0] c,
    input wire clk,
    output wire[7:0] d,
    input wire rst_n,
    input wire[1:0] s
);
    reg[7:0] d_reg = 8'h00;
    reg[7:0] d_reg_next;
    assign d = d_reg;
    always @(posedge clk) begin: assig_process_d_reg
        if (rst_n == 1'b0)
            d_reg <= 8'h00;
        else
            d_reg <= d_reg_next;
    end

    always @(b, c, d_reg, s) begin: assig_process_d_reg_next
        if (s[0])
            d_reg_next = b;
        else if (s[1])
            d_reg_next = c;
        else
            d_reg_next = d_reg;
    end

endmodule

```