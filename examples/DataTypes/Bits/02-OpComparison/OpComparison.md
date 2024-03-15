# Arithmetic

HWT python source:

```python

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class OpComparison(Unit):
    
    def _declr(self):
        self.a       = Signal(Bits(8))
        self.b       = Signal(Bits(8))
        self.a_eq_b  = Signal()._m()
        self.a_ne_b  = Signal()._m()
        self.a_ge_b  = Signal()._m()
        self.a_gt_b  = Signal()._m()
        self.a_le_b  = Signal()._m()
        self.a_lt_b  = Signal()._m()
        
    def _impl(self):
        self.a_eq_b(self.a._eq(self.b))
        self.a_ne_b(self.a != self.b)
        self.a_ge_b(self.a >= self.b)
        self.a_gt_b(self.a >  self.b)
        self.a_le_b(self.a <= self.b)
        self.a_lt_b(self.a <  self.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(OpComparison(), serializer_cls=VerilogSerializer))
    
    
```

Execute the python script to generate Verilog:

```sh
python OpComparison.py

```

The generated Verilog:

```verilog
module OpComparison (
    input wire[7:0] a,
    output reg a_eq_b,
    output reg a_ge_b,
    output reg a_gt_b,
    output reg a_le_b,
    output reg a_lt_b,
    output reg a_ne_b,
    input wire[7:0] b
);
    always @(a, b) begin: assig_process_a_eq_b
        a_eq_b = a == b;
    end

    always @(a, b) begin: assig_process_a_ge_b
        a_ge_b = a >= b;
    end

    always @(a, b) begin: assig_process_a_gt_b
        a_gt_b = a > b;
    end

    always @(a, b) begin: assig_process_a_le_b
        a_le_b = a <= b;
    end

    always @(a, b) begin: assig_process_a_lt_b
        a_lt_b = a < b;
    end

    always @(a, b) begin: assig_process_a_ne_b
        a_ne_b = a != b;
    end

endmodule


```