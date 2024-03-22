# BitWiseLogic

HWT python source:

```python
from hwt.code import If
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, Clk, Rst_n
from hwt.interfaces.utils import propagateClkRstn

class Rst_nSubmodule(Unit):
    
    def _declr(self):
        self.clk = Clk()
    
        with self._associated(clk=self.clk):
            self.rst_n = Rst_n()
            with self._associated(rst=self.rst_n):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self._make_association()

    def _impl(self):
        b_reg = self._reg(name="b_reg", def_val=0)

        b_reg(self.a)
        self.b(b_reg)
        

class Rst_nDemo(Unit):
    
    def _declr(self):
        self.clk = Clk()

        with self._associated(clk=self.clk):
            self.rst_n = Rst_n()
            with self._associated(rst=self.rst_n):
                self.a = Signal()
                self.b = Signal()._m()     
        
        self.sub = Rst_nSubmodule()

        self._make_association()

    def _impl(self):
        
        propagateClkRstn(self)

        self.sub.a(self.a)
        self.b(self.sub.b)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(Rst_nDemo(), serializer_cls=VerilogSerializer))
   
```

Execute the python script to generate Verilog:

```sh
python Rst_nDemo.py

```

The generated Verilog:

```verilog
module Rst_nSubmodule (
    input wire a,
    output wire b,
    input wire clk,
    input wire rst_n
);
    reg b_reg = 1'b0;
    wire b_reg_next;
    assign b = b_reg;
    always @(posedge clk) begin: assig_process_b_reg
        if (rst_n == 1'b0)
            b_reg <= 1'b0;
        else
            b_reg <= b_reg_next;
    end

    assign b_reg_next = a;
endmodule
module Rst_nDemo (
    input wire a,
    output wire b,
    input wire clk,
    input wire rst_n
);
    wire sig_sub_a;
    wire sig_sub_b;
    wire sig_sub_clk;
    wire sig_sub_rst_n;
    Rst_nSubmodule sub_inst (
        .a(sig_sub_a),
        .b(sig_sub_b),
        .clk(sig_sub_clk),
        .rst_n(sig_sub_rst_n)
    );

    assign b = sig_sub_b;
    assign sig_sub_a = a;
    assign sig_sub_clk = clk;
    assign sig_sub_rst_n = rst_n;
endmodule

```