# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal,  Clk, Rst
from hwt.hdl.types.bits import Bits

class NoRst(Unit):
    
    def _declr(self):
        self.u8       = Bits(8)
        self.a        = Signal(self.u8)
        self.c        = Signal(self.u8)._m()
        self.clk      = Clk()

    def _impl(self):
        c_reg = self._reg(name="c_reg", dtype=self.u8, clk=self.clk)
        
        c_reg(self.a)
        self.c(c_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(NoRst(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python NoRst.py

```

The generated Verilog:

```verilog
module NoRst (
    input wire[7:0] a,
    output wire[7:0] c,
    input wire clk
);
    reg[7:0] c_reg;
    wire[7:0] c_reg_next;
    assign c = c_reg;
    always @(posedge clk) begin: assig_process_c_reg
        c_reg <= c_reg_next;
    end

    assign c_reg_next = a;
endmodule


```