# BitWiseLogic

HWT python source:

```python
from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk, Rst
from hwt.interfaces.utils import propagateClkRst

class RstSubmodule(Unit):
    
    def _declr(self):
        self.clk     = Clk()
    
        with self._associated(clk=self.clk):
            self.rst     = Rst()
            with self._associated(rst=self.rst):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self._make_association()

    def _impl(self):
        b_reg = self._reg(name="b_reg", clk=self.clk, def_val=0)

        b_reg(self.a)
        self.b(b_reg)
        

class RstDemo(Unit):
    
    def _declr(self):
        self.clk = Clk()

        with self._associated(clk=self.clk):
            self.rst     = Rst()
            with self._associated(rst=self.rst):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self.sub = RstSubmodule()

        self._make_association()

    def _impl(self):
        
        propagateClkRst(self)

        self.sub.a(self.a)
        self.b(self.sub.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(RstDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python RstDemo.py

```

The generated Verilog:

```verilog
module RstSubmodule (
    input wire a,
    output wire b,
    input wire clk,
    input wire rst
);
    reg b_reg = 1'b0;
    wire b_reg_next;
    assign b = b_reg;
    always @(posedge clk) begin: assig_process_b_reg
        if (rst == 1'b1)
            b_reg <= 1'b0;
        else
            b_reg <= b_reg_next;
    end

    assign b_reg_next = a;
endmodule
module RstDemo (
    input wire a,
    output wire b,
    input wire clk,
    input wire rst
);
    wire sig_sub_a;
    wire sig_sub_b;
    wire sig_sub_clk;
    wire sig_sub_rst;
    RstSubmodule sub_inst (
        .a(sig_sub_a),
        .b(sig_sub_b),
        .clk(sig_sub_clk),
        .rst(sig_sub_rst)
    );

    assign b = sig_sub_b;
    assign sig_sub_a = a;
    assign sig_sub_clk = clk;
    assign sig_sub_rst = rst;
endmodule

```