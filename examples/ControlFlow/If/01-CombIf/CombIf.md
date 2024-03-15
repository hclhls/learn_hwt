# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class CombIf(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.s  = Signal()
        self.c  = Signal(self.u8)._m()
        self.d  = Signal(self.u8)._m()
        
    def _impl(self):
        
        If(self.s,
            self.c(self.b),
            self.d(self.a)
        ).Else(
            self.c(self.a),
            self.d(self.b)
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(CombIf(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python CombIf.py

```

The generated Verilog:

```verilog
module CombIf (
    input wire[7:0] a,
    input wire[7:0] b,
    output reg[7:0] c,
    output reg[7:0] d,
    input wire s
);
    always @(a, b, s) begin: assig_process_c
        if (s) begin
            c = b;
            d = a;
        end else begin
            c = a;
            d = b;
        end
    end

endmodule

```