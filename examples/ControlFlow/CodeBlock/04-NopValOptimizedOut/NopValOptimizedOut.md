# Arithmetic

HWT python source:

```python

from hwt.code import If, CodeBlock
from hwt.interfaces.std import Signal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class NopValOptimizedOut(Unit):

    def _declr(self):
        self.a = Signal()
        self.b = Signal()
        self.c = Signal()._m()
        addClkRstn(self)

    def _impl(self):
        r = self._reg("r")
        CodeBlock(
            If(self.b,
               r(self.a),
            ),
            self.c(self.a),
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(NopValOptimizedOut(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python module NopValOptimizedOut.py

```

The generated Verilog:

```verilog
module NopValOptimizedOut (
    input wire a,
    input wire b,
    output reg c,
    input wire clk,
    input wire rst_n
);
    always @(a) begin: assig_process_c
        c = a;
    end

endmodule

```