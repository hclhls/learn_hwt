# BitWiseLogic

HWT python source:

```python
from hwt.hdl.types.union import HUnion
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class HUnionValue(Unit):
    
    def _declr(self):
        self.b = Signal(Bits(2))._m()

    def _impl(self):
        hu_t = HUnion((Bits(2), "a"),
                      (Bits(2), "b"),
                     )
        hu_val = hu_t.from_py(("a",2))

        self.b(hu_val.b)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(HUnionValue(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python HUnionValue.py

```

The generated Verilog:

```verilog
module HUnionValue (
    output wire[1:0] b
);
    assign b = 2'b10;
endmodule

```