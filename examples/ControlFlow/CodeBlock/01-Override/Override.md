# Arithmetic

HWT python source:

```python

from hwt.code import If, CodeBlock
from hwt.interfaces.std import Signal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class Override(Unit):

    def _declr(self):
        self.a = Signal()
        self.b = Signal()
        self.c = Signal()._m()

    def _impl(self):
        # results in c = b
        CodeBlock(
            self.c(self.a),
            self.c(self.b),
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(Override(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python Override.py

```

The generated Verilog:

```verilog
module Override (
    input wire a,
    input wire b,
    output reg c
);
    always @(b) begin: assig_process_c
        c = b;
    end

endmodule

```