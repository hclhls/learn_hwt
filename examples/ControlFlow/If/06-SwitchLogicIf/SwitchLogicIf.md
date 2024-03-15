# Arithmetic

HWT python source:

```python

from hwt.code import SwitchLogic
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits
from hwt.interfaces.utils import addClkRstn

class SwitchLogicIf(Unit):
    
    def _declr(self):
        self.a  = Signal(Bits(32))
        self.b  = Signal(Bits(8))._m()
        self.s  = Signal(Bits(2))
        
    def _impl(self):
        
        cases = [(self.s._eq(i), self.b(self.a[8*(i+1):8*i])) for i in range(4)]

        SwitchLogic(cases)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(Mux(), serializer_cls=VerilogSerializer))
   
```

Execute the python script to generate Verilog:

```sh
python SwitchLogicIf.py

```

The generated Verilog:

```verilog
module SwitchLogicIf (
    input wire[31:0] a,
    output reg[7:0] b,
    input wire[1:0] s
);
    always @(a, s) begin: assig_process_b
        if (s == 2'b00)
            b = a[7:0];
        else if (s == 2'b01)
            b = a[15:8];
        else if (s == 2'b10)
            b = a[23:16];
        else if (s == 2'b11)
            b = a[31:24];
    end

endmodule

```