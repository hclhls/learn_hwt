# Arithmetic

HWT python source:

```python

from hwt.code import Concat
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpConcat(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))
        self.c       = Signal(Bits(self.D_W*2))._m()


    def _impl(self):
        self.c(Concat(self.a,self.b))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(OpConcat(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python OpConcat.py

```

The generated Verilog:

```verilog
module OpConcat #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    input wire[7:0] b,
    output reg[15:0] c
);
    always @(a, b) begin: assig_process_c
        c = {a, b};
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
```