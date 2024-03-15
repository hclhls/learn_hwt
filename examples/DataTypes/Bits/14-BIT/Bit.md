# Arithmetic

HWT python source:

```python

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.defs import BIT

class Bit(Unit):
    
    def _declr(self):
        self.a        = Signal(BIT)
        self.b        = Signal(BIT)
        self.c        = Signal(BIT)._m()

    def _impl(self):
        self.c(self.a & self.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Bit(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python Bit.py

```

The generated Verilog:

```verilog
module Bit (
    input wire a,
    input wire b,
    output reg c
);
    always @(a, b) begin: assig_process_c
        c = a & b;
    end

endmodule


```