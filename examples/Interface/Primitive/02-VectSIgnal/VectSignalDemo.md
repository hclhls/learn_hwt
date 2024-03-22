# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.bits import Bits

class VectSignalSubmodule(Unit):
    def _config(self):
        self.D_W     = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = VectSignal(self.D_W)._m()
        self.c       = Signal(Bits(self.D_W))._m()        

    def _impl(self):
        
        self.b(self.a)
        self.c(Bits(self.D_W).from_py(0))

class VectSignalDemo(Unit):
    def _config(self):
        self.D_W     = Param(8)

    def _declr(self):
        self.a       = VectSignal(self.D_W)
        self.b       = Signal(Bits(self.D_W))._m()
        self.c       = VectSignal(self.D_W)._m()        

        with self._paramsShared():
            self.sub = VectSignalSubmodule()

    def _impl(self):
        
        self.sub.a(self.a)
        self.b(self.sub.b)
        self.c(self.sub.c)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(VectSignalDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python VectSignalDemo.py

```

The generated Verilog:

```verilog
module VectSignalSubmodule #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output wire[7:0] b,
    output wire[7:0] c
);
    assign b = a;
    assign c = 8'h00;
    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module VectSignalDemo #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output wire[7:0] b,
    output wire[7:0] c
);
    wire[7:0] sig_sub_a;
    wire[7:0] sig_sub_b;
    wire[7:0] sig_sub_c;
    VectSignalSubmodule #(
        .D_W(8)
    ) sub_inst (
        .a(sig_sub_a),
        .b(sig_sub_b),
        .c(sig_sub_c)
    );

    assign b = sig_sub_b;
    assign c = sig_sub_c;
    assign sig_sub_a = a;
    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```