# Arithmetic

HWT python source:

```python

from hwt.code import If, CodeBlock
from hwt.interfaces.std import Signal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class NopVal(Unit):

    def _declr(self):
        self.a = Signal()
        self.b = Signal()
        self.c = Signal()._m()
        self.c1 = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        r = self._reg("r")
        CodeBlock(
            If(self.b,
               r(self.a),
            ),
            self.c(self.a),
        )
        self.c1(r)


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(NopVal(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python module NopVal.py

```

The generated Verilog:

```verilog
module NopVal (
    input wire a,
    input wire b,
    output reg c,
    output wire c1,
    input wire clk,
    input wire rst_n
);
    reg r;
    reg r_next;
    always @(a, b, r) begin: assig_process_c
        if (b)
            r_next = a;
        else
            r_next = r;
        c = a;
    end

    assign c1 = r;
    always @(posedge clk) begin: assig_process_r
        r <= r_next;
    end

endmodule

```