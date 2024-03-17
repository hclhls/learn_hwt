# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal,  Clk, Rst
from hwt.hdl.types.bits import Bits

class SyncRomInferred(Unit):
    
    def _declr(self):
        self.a        = Signal(Bits(2))
        self.d        = Signal(Bits(8))._m()
        self.clk      = Clk()

    def _impl(self):
        rom = self._sig("rom", Bits(8)[4], def_val=[i for i in range(4)])

        If(self.clk._onRisingEdge(),
           self.d(rom[self.a])
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(SyncRomInferred(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python SyncRomInferred.py

```

The generated Verilog:

```verilog
module SyncRomInferred (
    input wire[1:0] a,
    input wire clk,
    output reg[7:0] d
);
    reg[7:0] rom[0:3];
    always @(posedge clk) begin: assig_process_d
        d <= rom[a];
    end

    initial begin
        rom[0] = 0;
        rom[1] = 1;
        rom[2] = 2;
        rom[3] = 3;
    end

endmodule

```