# Arithmetic

HWT python source:

```python

from hwt.code import Concat
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpSlice(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))._m()
        self.b       = Signal(Bits(self.D_W))._m()
        self.c       = Signal(Bits(self.D_W*2))


    def _impl(self):
        self.a(self.c[self.D_W*2:self.D_W])
        self.b(self.c[self.D_W:])
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(OpSlice(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python OpSlice.py

```

The generated Verilog:

```verilog
module OpSlice #(
    parameter D_W = 8
) (
    output reg[7:0] a,
    output reg[7:0] b,
    input wire[15:0] c
);
    always @(c) begin: assig_process_a
        a = c[15:8];
    end

    always @(c) begin: assig_process_b
        b = c[7:0];
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```