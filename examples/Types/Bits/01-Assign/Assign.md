# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal

class Assign(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()._m()
        self.c       = Signal()._m()        

    def _impl(self):
        
        self.b(self.a)
        self.c(0)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(Assign(), serializer_cls=VerilogSerializer))
```

Execute the python script to generate Verilog:

```sh
python Assign.py

```

The generated Verilog:

```verilog
module Assign #(
    parameter D_W = 8
) (
    input wire a,
    output wire b,
    output wire c
);
    assign b = a;
    assign c = 1'b1;
    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```