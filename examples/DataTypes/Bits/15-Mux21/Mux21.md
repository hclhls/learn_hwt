# Arithmetic

HWT python source:

```python

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.defs import BIT

class Mux21(Unit):
    
    def _declr(self):
        self.a        = VectSignal(8)
        self.b        = VectSignal(8)
        self.s        = Signal()
        self.c        = VectSignal(8)._m()

    def _impl(self):
        self.c(self.s._ternary(self.a, self.b))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Mux21(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python Mux21.py

```

The generated Verilog:

```verilog
module Mux21 (
    input wire[7:0] a,
    input wire[7:0] b,
    output reg[7:0] c,
    input wire s
);
    always @(a, b, s) begin: assig_process_c
        c = s ? a : b;
    end

endmodule

```