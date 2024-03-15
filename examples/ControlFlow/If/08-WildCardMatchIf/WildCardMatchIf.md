# Arithmetic

HWT python source:

```python

from hwt.code import Switch,SwitchLogic,If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.hdl.valueUtils import isSameHVal, areSameHVals

class WildCardMatchIf(Unit):
    
    def _declr(self):
        self.a  = Signal(Bits(32))
        self.s  = Signal(Bits(3))
        self.b  = Signal(Bits(8))._m()
        
    def _impl(self):
        u3 = Bits(3)
        SwitchLogic(
            [(self.s._eq(u3.from_py(0b001, vld_mask=0b001)), self.b(self.a[8:0])),
             (self.s._eq(u3.from_py(0b010, vld_mask=0b010)), self.b(self.a[16:8])),
             (self.s._eq(u3.from_py(0b100, vld_mask=0b100)), self.b(self.a[24:16])),
             ],
             self.b(self.a[32:24])
        )
     

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(WildCardMatchIf(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python WildCardMatchIf.py

```

The generated Verilog:

```verilog
module WildCardMatchIf (
    input wire[31:0] a,
    output reg[7:0] b,
    input wire[2:0] s
);
    always @(a, s) begin: assig_process_b
        if (s == 3'bxx1)
            b = a[7:0];
        else if (s == 3'bx1x)
            b = a[15:8];
        else if (s == 3'b1xx)
            b = a[23:16];
        else
            b = a[31:24];
    end

endmodule

```