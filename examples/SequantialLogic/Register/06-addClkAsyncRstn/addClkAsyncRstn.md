# Arithmetic

HWT python source:

```python

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwt.interfaces.utils import addClkRstn, propagateClkRst
from hwt.hdl.types.bits import Bits

from hwt.code import If
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk, Rst_n
from hwt.interfaces.utils import addClkRstn, propagateClkRst
from hwt.hdl.types.bits import Bits

def add_domain(domain, reg, in_statement, def_val=0):
    return If(domain["rst"]._isOn(),
        reg(def_val)
    ).Elif(domain["rst"]._onRisingEdge(),
        reg(in_statement)
    )

class addClkAsyncRstn(Unit):
    def _declr(self):
        self.u8       = Bits(8)
        self.a        = Signal(self.u8)
        self.c        = Signal(self.u8)._m()
        self.clk      = Clk()
        self.rst_n    = Rst_n()

    def _impl(self):
        clk_domain = {"clk": self.clk, "rst": self.rst_n}
        
        c_reg = self._sig(name="c_reg", dtype=self.u8, def_val=False)
        add_domain(clk_domain, c_reg, self.a, 0)
        
        self.c(c_reg)

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(addClkAsyncRstn(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python addClkAsyncRstn.py

```

The generated Verilog:

```verilog
module addClkAsyncRstn (
    input wire[7:0] a,
    output wire[7:0] c,
    input wire clk,
    input wire rst_n
);
    reg[7:0] c_reg = 8'h00;
    assign c = c_reg;
    always @(posedge clk, negedge rst_n) begin: assig_process_c_reg
        if (rst_n == 1'b0)
            c_reg <= 8'h00;
        else
            c_reg <= a;
    end

endmodule

```