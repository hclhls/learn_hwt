# Arithmetic

HWT python source:

```python

ffrom hwt.code import Switch
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class WithoutDefaultCase(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.u2 = Bits(2)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.d  = Signal(self.u8)
        self.s  = Signal(self.u2)
        self.e  = Signal(self.u8)._m()
        
    def _impl(self):
        
        Switch(self.s
        ).Case(0b00,
            self.e  (self.a)
        ).Case(0b01,
            self.e  (self.b)
        ).Case(0b10,
            self.e  (self.c)
        ).Case(0b11,
            self.e  (self.d)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(WithoutDefaultCase(), serializer_cls=VerilogSerializer))
   
```

Execute the python script to generate Verilog:

```sh
python WithoutDefaultCase.py

```

The generated Verilog:

```verilog
module WoDefaultCase (
    input wire[7:0] a,
    input wire[7:0] b,
    input wire[7:0] c,
    input wire[7:0] d,
    output reg[7:0] e,
    input wire[1:0] s
);
    always @(a, b, c, d, s) begin: assig_process_e
        case(s)
            2'b00:
                e = a;
            2'b01:
                e = b;
            2'b10:
                e = c;
            2'b11:
                e = d;
        endcase
    end

endmodule

```