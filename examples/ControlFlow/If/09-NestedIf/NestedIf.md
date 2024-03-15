# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class NestedIf(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.d  = Signal(self.u8)
        self.s  = Signal(Bits(2))
        self.e  = Signal(self.u8)._m()
        self.f  = Signal(self.u8)._m()

    def _impl(self):
        
        If(self.s[0],
            self.e(self.b),
            If(self.s[1],
                self.f(self.c)
            ).Else(
                self.f(self.d)
            )
        ).Else(
            self.e(self.a),
            If(self.s[1],
                self.f(self.d)
            ).Else(
                self.f(self.e)
            )
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(NestedIf(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python NestedIf.py

```

The generated Verilog:

```verilog
module NestedIf (
    input wire[7:0] a,
    input wire[7:0] b,
    input wire[7:0] c,
    input wire[7:0] d,
    output reg[7:0] e,
    output reg[7:0] f,
    input wire[1:0] s
);
    always @(a, b, s) begin: assig_process_e
        if (s[0])
            e = b;
        else
            e = a;
    end

    always @(c, d, e, s) begin: assig_process_f
        if (s[0])
            if (s[1])
                f = c;
            else
                f = d;
        else if (s[1])
            f = d;
        else
            f = e;
    end

endmodule


```