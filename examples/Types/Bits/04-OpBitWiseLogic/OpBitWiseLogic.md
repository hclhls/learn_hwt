# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpBitWiseLogic(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W))
        self.a_and_b = Signal(Bits(self.D_W))._m()
        self.a_or_b  = Signal(Bits(self.D_W))._m()
        self.a_xor_b = Signal(Bits(self.D_W))._m()
        self.not_a   = Signal(Bits(self.D_W))._m()

    def _impl(self):
        
        self.a_and_b(self.a & self.b)
        self.a_or_b (self.a | self.b)
        self.a_xor_b(self.a ^ self.b)
        self.not_a  (~self.a)


if __name__ == "__main__":  # alias python main function
    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(OpBitWiseLogic(), serializer_cls=VerilogSerializer))
```

Execute the python script to generate Verilog:

```sh
python OpBitWiseLogic.py

```

The generated Verilog:

```verilog
module OpBitWiseLogic #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output reg[7:0] a_and_b,
    output reg[7:0] a_or_b,
    output reg[7:0] a_xor_b,
    input wire[7:0] b,
    output reg[7:0] not_a
);
    always @(a, b) begin: assig_process_a_and_b
        a_and_b = a & b;
    end

    always @(a, b) begin: assig_process_a_or_b
        a_or_b = a | b;
    end

    always @(a, b) begin: assig_process_a_xor_b
        a_xor_b = a ^ b;
    end

    always @(a) begin: assig_process_not_a
        not_a = ~a;
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule



```