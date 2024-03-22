# BitWiseLogic

HWT python source:

```python
from hwt.hdl.types.struct import HStruct
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal
from hwt.hdl.types.defs import BIT

class HStructSignal(Unit):
    
    def _declr(self):
        self.a = Signal(Bits(2))
        self.b = Signal(Bits(2))._m()

    def _impl(self):
        c = self._sig(dtype=HStruct((BIT,"b0"), (BIT,"b1"),), 
                      name="temp") 
        
        c.b0(self.a[0])
        c.b1(self.a[1])
        
        self.b[0](c.b0 & c.b1)
        self.b[1](c.b0 | c.b1)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(HStructSignal(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python HStructSignal.py

```

The generated Verilog:

```verilog
module HStructSignal (
    input wire[1:0] a,
    output reg[1:0] b
);
    reg temp_b0;
    reg temp_b1;
    always @(temp_b0, temp_b1) begin: assig_process_b
        b = {temp_b0 | temp_b1, temp_b0 & temp_b1};
    end

    always @(a) begin: assig_process_temp_b0
        temp_b0 = a[0];
    end

    always @(a) begin: assig_process_temp_b1
        temp_b1 = a[1];
    end

endmodule

```