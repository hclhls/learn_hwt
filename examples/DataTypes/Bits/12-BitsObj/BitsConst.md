# Arithmetic

HWT python source:

```python

from hwt.code import Concat, replicate
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class BitsObj(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)._m()
        self.c  = Signal(self.u8)._m()
        
    def _impl(self):
        a, b, c = self.a, self.b, self.c
        one     = self.u8.from_py(1)
        
        b(a + one)
        c(a + one*2)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(BitsObj(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python BitsObj.py

```

The generated Verilog:

```verilog
module BitsObj (
    input wire[7:0] a,
    output reg[7:0] b,
    output reg[7:0] c
);
    always @(a) begin: assig_process_b
        b = a + 8'h01;
    end

    always @(a) begin: assig_process_c
        c = a + 8'h02;
    end

endmodule

```