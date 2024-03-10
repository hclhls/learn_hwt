# Arithmetic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpArithmetic(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))
        self.a_add_b = Signal(Bits(self.D_W))._m()
        self.a_sub_b = Signal(Bits(self.D_W))._m()
        self.a_mul_b = Signal(Bits(self.D_W))._m()
        self.a_div_b = Signal(Bits(self.D_W))._m()

    def _impl(self):
        self.a_add_b(self.a +  self.b)
        self.a_sub_b(self.a -  self.b + 1)
        self.a_mul_b(self.a *  self.b + 2)
        self.a_div_b(self.a // self.b + 3)


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(OpArithmetic(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python OpArithmetic.py

```

The generated Verilog:

```verilog
module OpArithmetic #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output reg[7:0] a_add_b,
    output reg[7:0] a_div_b,
    output reg[7:0] a_mul_b,
    output reg[7:0] a_sub_b,
    input wire[7:0] b
);
    always @(a, b) begin: assig_process_a_add_b
        a_add_b = a + b;
    end

    always @(a, b) begin: assig_process_a_div_b
        a_div_b = a / b + 8'h03;
    end

    always @(a, b) begin: assig_process_a_mul_b
        a_mul_b = a * b + 8'h02;
    end

    always @(a, b) begin: assig_process_a_sub_b
        a_sub_b = a - b + 8'h01;
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```