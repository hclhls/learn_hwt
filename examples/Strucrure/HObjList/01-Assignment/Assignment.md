# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, VectSignal
from hwt.synthesizer.hObjList import HObjList

class Assignment(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a = Signal(Bits(self.D_W))
        self.b = HObjList([Signal() for _ in range(self.D_W)])
        self.c = HObjList([Signal()._m() for _ in range(self.D_W // 2)])
        self.d = VectSignal(self.D_W//2)._m()
        self.f = Signal(Bits(self.D_W))
        self.g = Signal()._m()
    
    def _impl(self):

        for idx, item in enumerate(self.c):
            item(self.a[idx*2] | self.a[idx*2+1])
        
        for idx, item in enumerate(self.d):
            item(self.b[idx*2] & self.b[idx*2+1])
        
        i     = 0
        width = self.D_W

        list_0 = HObjList([self._sig(name=f"l_{i}_{j}",dtype=Bits(1)) for j in range(width)])
        
        for idx, item in enumerate(list_0):
            item(self.f[idx])

        while (True):
            width  = width // 2
            list_1 = HObjList([self._sig(name=f"l_{i}_{j}",dtype=Bits(1)) for j in range(width)])
            
            for idx, item in enumerate(list_1):
                list_1[idx](list_0[idx*2] & list_0[idx*2+1])
            
            list_0 = list_1
            
            if width <= 1:
                self.g(list_1[0])
                break
            
            i = i + 1

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(Assignment(), serializer_cls=VerilogSerializer))


```

Execute the python script to generate Verilog:

```sh
python Assignment.py

```

The generated Verilog:

```verilog
module Assignment #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    input wire b_0,
    input wire b_1,
    input wire b_2,
    input wire b_3,
    input wire b_4,
    input wire b_5,
    input wire b_6,
    input wire b_7,
    output reg c_0,
    output reg c_1,
    output reg c_2,
    output reg c_3,
    output reg[3:0] d,
    input wire[7:0] f,
    output wire g
);
    reg l_0_0;
    reg l_0_0_0;
    reg l_0_1;
    reg l_0_1_0;
    reg l_0_2;
    reg l_0_2_0;
    reg l_0_3;
    reg l_0_3_0;
    reg l_0_4;
    reg l_0_5;
    reg l_0_6;
    reg l_0_7;
    reg l_1_0;
    reg l_1_1;
    reg l_2_0;
    always @(a) begin: assig_process_c_0
        c_0 = a[0] | a[1];
    end

    always @(a) begin: assig_process_c_1
        c_1 = a[2] | a[3];
    end

    always @(a) begin: assig_process_c_2
        c_2 = a[4] | a[5];
    end

    always @(a) begin: assig_process_c_3
        c_3 = a[6] | a[7];
    end

    always @(b_0, b_1, b_2, b_3, b_4, b_5, b_6, b_7) begin: assig_process_d
        d = {{{b_6 & b_7, b_4 & b_5}, b_2 & b_3}, b_0 & b_1};
    end

    assign g = l_2_0;
    always @(f) begin: assig_process_l_0_0
        l_0_0 = f[0];
    end

    always @(l_0_0, l_0_1) begin: assig_process_l_0_0_0
        l_0_0_0 = l_0_0 & l_0_1;
    end

    always @(f) begin: assig_process_l_0_1
        l_0_1 = f[1];
    end

    always @(l_0_2, l_0_3) begin: assig_process_l_0_1_0
        l_0_1_0 = l_0_2 & l_0_3;
    end

    always @(f) begin: assig_process_l_0_2
        l_0_2 = f[2];
    end

    always @(l_0_4, l_0_5) begin: assig_process_l_0_2_0
        l_0_2_0 = l_0_4 & l_0_5;
    end

    always @(f) begin: assig_process_l_0_3
        l_0_3 = f[3];
    end

    always @(l_0_6, l_0_7) begin: assig_process_l_0_3_0
        l_0_3_0 = l_0_6 & l_0_7;
    end

    always @(f) begin: assig_process_l_0_4
        l_0_4 = f[4];
    end

    always @(f) begin: assig_process_l_0_5
        l_0_5 = f[5];
    end

    always @(f) begin: assig_process_l_0_6
        l_0_6 = f[6];
    end

    always @(f) begin: assig_process_l_0_7
        l_0_7 = f[7];
    end

    always @(l_0_0_0, l_0_1_0) begin: assig_process_l_1_0
        l_1_0 = l_0_0_0 & l_0_1_0;
    end

    always @(l_0_2_0, l_0_3_0) begin: assig_process_l_1_1
        l_1_1 = l_0_2_0 & l_0_3_0;
    end

    always @(l_1_0, l_1_1) begin: assig_process_l_2_0
        l_2_0 = l_1_0 & l_1_1;
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule


```