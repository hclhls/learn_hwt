# Arithmetic

HWT python source:

```python

from hwt.code import Concat, replicate
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpReplicate(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W+2))._m()


    def _impl(self):
        self.b(Concat(replicate(2, self.a[self.D_W-1]),self.a))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(OpReplicate(), serializer_cls=VerilogSerializer))
```

Execute the python script to generate Verilog:

```sh
python OpReplicate.py

```

The generated Verilog:

```verilog
module OpReplicate #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output reg[9:0] b
);
    always @(a) begin: assig_process_b
        b = {{a[7], a[7]}, a};
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule


```