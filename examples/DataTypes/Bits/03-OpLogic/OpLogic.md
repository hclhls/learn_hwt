# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal

class OpLogic(Unit):

    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()
        self.a_and_b = Signal()._m()
        self.a_or_b  = Signal()._m()
        self.a_xor_b = Signal()._m()
        self.not_a   = Signal()._m()

    def _impl(self):
        
        self.a_and_b(self.a & self.b)
        self.a_or_b (self.a | self.b)
        self.a_xor_b(self.a ^ self.b)
        self.not_a  (~self.a)


if __name__ == "__main__":  # alias python main function
    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(OpLogic(), serializer_cls=VerilogSerializer))
```

Execute the python script to generate Verilog:

```sh
python OpLogic.py

```

The generated Verilog:

```verilog
module OpLogic (
    input wire a,
    output reg a_and_b,
    output reg a_or_b,
    output reg a_xor_b,
    input wire b,
    output reg not_a
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

endmodule


```