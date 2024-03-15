# BitWiseLogic

HWT python source:

```python
from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

def IfElifElse(condition0, statements, condition1, fallback0, fallback1):
    return If(condition0,
        statements
    ).Elif(condition1,
        fallback0,
    ).Else(
        fallback1
    )

class FunctionInline(Unit):
    
    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()
        self.s       = Signal(Bits(2))
        self.c       = Signal()._m()        

    def _impl(self):
        
        IfElifElse(self.s._eq(0b01), self.c(self.a),
               self.s._eq(0b01), self.c(self.b),
               self.c(0))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(FunctionInline(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python FunctionInline.py

```

The generated Verilog:

```verilog
module FunctionInline (
    input wire a,
    input wire b,
    output reg c,
    input wire[1:0] s
);
    always @(a, b, s) begin: assig_process_c
        if (s == 2'b01)
            c = a;
        else if (s == 2'b01)
            c = b;
        else
            c = 1'b0;
    end

endmodule

```