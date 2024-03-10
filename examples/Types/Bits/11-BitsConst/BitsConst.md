# Arithmetic

HWT python source:

```python

from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class BitsConst(Unit):
    
    def _declr(self):
        self.a        = Signal(Bits(8))
        self.b        = Signal(Bits(8))._m()
        
    def _impl(self):
        one   = Bits(8).from_py(1)
        two   = Bits(8).from_py(0b00000010)
        three = Bits(8).from_py(0o003)
        four  = Bits(8).from_py(0x04)
        self.b(self.a + one + two + three + four)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(BitsConst(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python BitsConst.py

```

The generated Verilog:

```verilog
module BitsConst (
    input wire[7:0] a,
    output reg[7:0] b
);
    always @(a) begin: assig_process_b
        b = a + 8'h01 + 8'h02 + 8'h03 + 8'h04;
    end

endmodule

```