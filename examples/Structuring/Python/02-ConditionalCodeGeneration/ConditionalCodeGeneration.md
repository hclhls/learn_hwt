# BitWiseLogic

HWT python source:

```python
import sys
from hwt.code import If, Switch
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.hdl.types.bits import Bits

class ConditionalCodeGeneration(Unit):

    def _config(self):
        self.D_W     = Param(int(sys.argv[1]))

    def _declr(self):
        
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))
        self.s       = Signal(Bits(2))
        self.c       = Signal(Bits(self.D_W))._m()        

    def _impl(self):
        
        SWAP_AB = True if int(sys.argv[1])==1 else False

        if SWAP_AB:
            If(self.s._eq(0b01),
                self.c(self.b)
            ).Elif(self.s._eq(0b10),
                self.c(self.a)
            ).Else(
                self.c(0)
            )
        else:
            If(self.s._eq(0b01),
                self.c(self.a)
            ).Elif(self.s._eq(0b10),
                self.c(self.b)
            ).Else(
                self.c(0)
            )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(ConditionalCodeGeneration(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python ConditionalCodeGeneration.py 8 0

```

The generated Verilog:

```verilog
module ConditionalCodeGeneration #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    input wire[7:0] b,
    output reg[7:0] c,
    input wire[1:0] s
);
    always @(a, b, s) begin: assig_process_c
        if (s == 2'b01)
            c = a;
        else if (s == 2'b10)
            c = b;
        else
            c = 8'h00;
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```

Execute the python script to generate Verilog:

```sh
python ConditionalCodeGeneration.py 16 1

```

The generated Verilog:

```verilog
module ConditionalCodeGeneration #(
    parameter D_W = 16
) (
    input wire[15:0] a,
    input wire[15:0] b,
    output reg[15:0] c,
    input wire[1:0] s
);
    always @(a, b, s) begin: assig_process_c
        if (s == 2'b01)
            c = a;
        else if (s == 2'b10)
            c = b;
        else
            c = 16'h0000;
    end

    generate if (D_W != 16)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```
