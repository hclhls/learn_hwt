# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.interfaces.utils import addClkRst, propagateClkRst
from hwt.hdl.types.bits import Bits

class addClkAsyncRst(Unit):
    def _declr(self):
        self.u8       = Bits(8)
        self.a        = Signal(self.u8)
        self.c        = Signal(self.u8)._m()
        addClkRst(self)

    def _impl(self):
        c_reg = self._sig(name="c_reg", dtype=self.u8, def_val=False)
        
        If(self.rst._isOn(),
            c_reg(0)
        ).Elif(self.clk._onRisingEdge(),
            c_reg(self.a)
        )
        self.c(c_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(addClkAsyncRst(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python addClkAsyncRst.py

```

The generated Verilog:

```verilog
module addClkAsyncRst (
    input wire[7:0] a,
    output wire[7:0] c,
    input wire clk,
    input wire rst
);
    reg[7:0] c_reg = 8'h00;
    assign c = c_reg;
    always @(posedge clk, posedge rst) begin: assig_process_c_reg
        if (rst == 1'b1)
            c_reg <= 8'h00;
        else
            c_reg <= a;
    end

endmodule

```