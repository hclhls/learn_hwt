# Arithmetic

HWT python source:

```python

from hwt.code import Switch
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class AddCases(Unit):
    
    def _declr(self):
        self.a  = Signal(Bits(24))
        self.s  = Signal(Bits(3))
        self.b  = Signal(Bits(8))._m()
        
    def _impl(self):
        
        sel_cases = [(0b001<<i, self.b(self.a[8*(i+1):8*i])) for i in range(3)]
        
        Switch(self.s
        ).add_cases(sel_cases
        ).Default(
            self.b  (0)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(AddCases(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python AddCases.py

```

The generated Verilog:

```verilog
module AddCases (
    input wire[23:0] a,
    output reg[7:0] b,
    input wire[2:0] s
);
    always @(a, s) begin: assig_process_b
        case(s)
            3'b001:
                b = a[7:0];
            3'b010:
                b = a[15:8];
            3'b100:
                b = a[23:16];
            default:
                b = 8'h00;
        endcase
    end

endmodule

```