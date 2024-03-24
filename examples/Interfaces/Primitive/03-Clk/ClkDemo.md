# BitWiseLogic

HWT python source:

```python
from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk
from hwt.interfaces.utils import propagateClk

class ClkSubmodule(Unit):
    
    def _declr(self):
        self.clk     = Clk()

        with self._associated(clk=self.clk):
            self.a = Signal()
            self.b = Signal()._m()     
        
        self._make_association()

    def _impl(self):
        b_reg = self._reg(name="b_reg", clk=self.clk, def_val=None)

        b_reg(self.a)
        self.b(b_reg)
        

class ClkDemo(Unit):
    
    def _declr(self):
        self.clk = Clk()

        with self._associated(clk=self.clk):
            self.a = Signal()
            self.b = Signal()._m()
        
        self.sub = ClkSubmodule()

        self._make_association()

    def _impl(self):
        
        propagateClk(self)

        self.sub.a(self.a)
        self.b(self.sub.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(ClkDemo(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python ClkDemo.py

```

The generated Verilog:

```verilog
module ClkSubmodule (
    input wire a,
    output wire b,
    input wire clk
);
    reg b_reg;
    wire b_reg_next;
    assign b = b_reg;
    always @(posedge clk) begin: assig_process_b_reg
        b_reg <= b_reg_next;
    end

    assign b_reg_next = a;
endmodule
module ClkDemo (
    input wire a,
    output wire b,
    input wire clk
);
    wire sig_sub_a;
    wire sig_sub_b;
    wire sig_sub_clk;
    ClkSubmodule sub_inst (
        .a(sig_sub_a),
        .b(sig_sub_b),
        .clk(sig_sub_clk)
    );

    assign b = sig_sub_b;
    assign sig_sub_a = a;
    assign sig_sub_clk = clk;
endmodule

```