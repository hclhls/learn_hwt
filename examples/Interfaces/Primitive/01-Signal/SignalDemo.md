# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal

class SignalSubmodule(Unit):
    
    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()._m()
        self.c       = Signal()._m()        

    def _impl(self):
        
        self.b(self.a)
        self.c(0)

class SignalDemo(Unit):
    
    def _declr(self):
        self.a       = Signal()
        self.b       = Signal()._m()
        self.c       = Signal()._m()        

        self.sub = SignalSubmodule()

    def _impl(self):
        
        self.sub.a(self.a)
        self.b(self.sub.b)
        self.c(self.sub.c)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(SignalDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python SignalDemo.py

```

The generated Verilog:

```verilog
module SignalSubmodule (
    input wire a,
    output wire b,
    output wire c
);
    assign b = a;
    assign c = 1'b0;
endmodule
module SignalDemo (
    input wire a,
    output wire b,
    output wire c
);
    wire sig_sub_a;
    wire sig_sub_b;
    wire sig_sub_c;
    SignalSubmodule sub_inst (
        .a(sig_sub_a),
        .b(sig_sub_b),
        .c(sig_sub_c)
    );

    assign b = sig_sub_b;
    assign c = sig_sub_c;
    assign sig_sub_a = a;
endmodule

```