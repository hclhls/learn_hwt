# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, VectSignal

class Assignment(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = VectSignal(self.D_W)._m()
        self.c       = VectSignal(self.D_W//2)._m()

    def _impl(self):
        
        self.b(self.a)
        for idx, item in enumerate(self.c):
            item(~(self.a[idx*2] & self.a[idx*2+1]))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(Assignment(), serializer_cls=VerilogSerializer))
```

Execute the python script to generate Verilog:

```sh
python Assignment.py

```

The generated Verilog:

```verilog
module Assignment #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output wire[7:0] b,
    output reg[3:0] c
);
    assign b = a;
    always @(a) begin: assig_process_c
        c = {{{~(a[6] & a[7]), ~(a[4] & a[5])}, ~(a[2] & a[3])}, ~(a[0] & a[1])};
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule


```