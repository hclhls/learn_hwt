# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class CombElif(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.s  = Signal(Bits(2))
        self.d  = Signal(self.u8)._m()
        
    def _impl(self):
        
        If(self.s[0]&(~self.s[1]),
            self.d(self.b)
        ).Elif(self.s[1]&(~self.s[0]),
            self.d(self.c)
        ).Else(
            self.d(self.a)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(CombElif(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python CombElif.py

```

The generated Verilog:

```verilog
module CombElif (
    input wire[7:0] a,
    input wire[7:0] b,
    input wire[7:0] c,
    output reg[7:0] d,
    input wire[1:0] s
);
    always @(a, b, c, s) begin: assig_process_d
        if (s[0] & ~s[1])
            d = b;
        else if (s[1] & ~s[0])
            d = c;
        else
            d = a;
    end

endmodule

```