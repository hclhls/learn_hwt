# BitWiseLogic

HWT python source:

```python
import math
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal
from hwt.hdl.types.array import HArray

class LUTSin(Unit):
    def _config(self):
        self.W_IDX  = Param(5)
        self.W_DATA = Param(8)

    def _declr(self):
        self.idx  = Signal(Bits(self.W_IDX))
        self.data = Signal(Bits(self.W_DATA))._m()

    def _impl(self):
        numEntries = 1<<self.W_IDX
        scaling    = (1<<(self.W_DATA-1))-1

        lut = self._sig(name="lut", dtype=HArray(Bits(self.W_DATA,signed=True),numEntries), 
                                    def_val=[int(math.sin(i*math.pi*2/numEntries)*scaling+0.5) for i in range(numEntries)])

        self.data(lut[self.idx])


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(LUTSin(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python LUTSin.py

```

The generated Verilog:

```verilog
module LUTSin (
    output reg[7:0] data,
    input wire[3:0] idx
);
    reg signed[7:0] lut[0:15];
    always @(idx) begin: assig_process_data
        data = $signed(lut[idx]);
    end

    initial begin
        lut[0] = 0;
        lut[1] = 49;
        lut[2] = 90;
        lut[3] = 117;
        lut[4] = 127;
        lut[5] = 117;
        lut[6] = 90;
        lut[7] = 49;
        lut[8] = 0;
        lut[9] = -48;
        lut[10] = -89;
        lut[11] = -116;
        lut[12] = -126;
        lut[13] = -116;
        lut[14] = -89;
        lut[15] = -48;
    end

endmodule

```