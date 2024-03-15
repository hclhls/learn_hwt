# Arithmetic

HWT python source:

```python

from hwt.code import Switch
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class WithDefaultCase(Unit):
    
    def _declr(self):
        self.u8 = Bits(8)
        self.u3 = Bits(3)
        self.a  = Signal(self.u8)
        self.b  = Signal(self.u8)
        self.c  = Signal(self.u8)
        self.s  = Signal(self.u3)
        self.d  = Signal(self.u8)._m()
        
    def _impl(self):
        
        Switch(self.s
        ).Case(0b001,
            self.d  (self.a)
        ).Case(0b010,
            self.d  (self.b)
        ).Case(0b100,
            self.d  (self.c)
        ).Default(
            self.d  (0)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(SwitchCase(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python WithDefaultCase.py

```

The generated Verilog:

```verilog
module SwitcWithDefaultCasehCase (
    input wire[7:0] a,
    input wire[7:0] b,
    input wire[7:0] c,
    output reg[7:0] d,
    input wire[2:0] s
);
    always @(a, b, c, s) begin: assig_process_d
        case(s)
            3'b001:
                d = a;
            3'b010:
                d = b;
            3'b100:
                d = c;
            default:
                d = 8'h00;
        endcase
    end

endmodule

```