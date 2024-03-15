# Arithmetic

HWT python source:

```python

from hwt.code import rol, ror
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpRotate(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))._m()
        self.c       = Signal(Bits(self.D_W))._m()

    def _impl(self):
        self.b(rol(self.a, 1))
        self.c(ror(self.a, 2))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(OpRotate(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python OpRotate.py

```

The generated Verilog:

```verilog
module OpRotate #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output reg[7:0] b,
    output reg[7:0] c
);
    always @(a) begin: assig_process_b
        b = {a[6:0], a[7:7]};
    end

    always @(a) begin: assig_process_c
        c = {a[1:0], a[7:2]};
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule



```