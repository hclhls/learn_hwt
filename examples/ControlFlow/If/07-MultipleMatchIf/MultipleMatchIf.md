# Arithmetic

HWT python source:

```python

from hwt.code import SwitchLogic, Switch, In
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.bits import Bits

class MultipleMatch(Unit):

    def _declr(self):
        self.s  = Signal(Bits(4))
        self.a  = Signal(Bits(8))
        self.b  = Signal(Bits(8))
        self.c  = Signal(Bits(8))
        self.d  = Signal(Bits(8))._m()
    
    def _impl(self):

        SwitchLogic(
            [(In(self.s,[0b0010, 0b0001]), self.d(self.b)),
             (In(self.s,[0b0100, 0b1000]), self.d(self.c))
             ],
             self.d(self.a)
        )
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(MultipleMatch(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python MultipleMatch.py

```

The generated Verilog:

```verilog
module MultipleMatch (
    input wire[7:0] a,
    input wire[7:0] b,
    input wire[7:0] c,
    output reg[7:0] d,
    input wire[3:0] s
);
    always @(a, b, c, s) begin: assig_process_d
        if (s == 4'h2 | s == 4'h1)
            d = b;
        else if (s == 4'h4 | s == 4'h8)
            d = c;
        else
            d = a;
    end

endmodule

```