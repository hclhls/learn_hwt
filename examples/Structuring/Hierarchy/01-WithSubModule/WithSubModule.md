# BitWiseLogic

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal, VectSignal
from hwt.hdl.types.bits import Bits
from hwt.synthesizer.hObjList import HObjList
from hwt.serializer.mode import serializeParamsUniq

@serializeParamsUniq
class SubModule(Unit):
    def _declr(self):
        self.i0 = Signal()
        self.i1 = Signal()
        self.o  = Signal()._m()

    def _impl(self):
        self.o(self.i0 & self.i1)

@serializeParamsUniq
class WithSubModule(Unit):
    def _config(self):
        self.D_W = Param(4)

    def _declr(self):
        self.a  = VectSignal(self.D_W)
        self.b  = VectSignal(self.D_W)
        self.c  = VectSignal(self.D_W)._m()      

        self.add21 = HObjList([
           SubModule() for _ in range(self.D_W)
        ])

    def _impl(self):
        
        for idx, item in enumerate(self.c):
            self.add21[idx].i0(self.a[idx])
            self.add21[idx].i1(self.b[idx])
            item(self.add21[idx].o)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(WithSubModule(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python WithSubModule.py

```

The generated Verilog:

```verilog
module SubModule (
    input wire i0,
    input wire i1,
    output reg o
);
    always @(i0, i1) begin: assig_process_o
        o = i0 & i1;
    end

endmodule
module WithSubModule #(
    parameter D_W = 4
) (
    input wire[3:0] a,
    input wire[3:0] b,
    output reg[3:0] c
);
    reg sig_add21_0_i0;
    reg sig_add21_0_i1;
    wire sig_add21_0_o;
    reg sig_add21_1_i0;
    reg sig_add21_1_i1;
    wire sig_add21_1_o;
    reg sig_add21_2_i0;
    reg sig_add21_2_i1;
    wire sig_add21_2_o;
    reg sig_add21_3_i0;
    reg sig_add21_3_i1;
    wire sig_add21_3_o;
    SubModule add21_0_inst (
        .i0(sig_add21_0_i0),
        .i1(sig_add21_0_i1),
        .o(sig_add21_0_o)
    );

    SubModule add21_1_inst (
        .i0(sig_add21_1_i0),
        .i1(sig_add21_1_i1),
        .o(sig_add21_1_o)
    );

    SubModule add21_2_inst (
        .i0(sig_add21_2_i0),
        .i1(sig_add21_2_i1),
        .o(sig_add21_2_o)
    );

    SubModule add21_3_inst (
        .i0(sig_add21_3_i0),
        .i1(sig_add21_3_i1),
        .o(sig_add21_3_o)
    );

    always @(sig_add21_0_o, sig_add21_1_o, sig_add21_2_o, sig_add21_3_o) begin: assig_process_c
        c = {{{sig_add21_3_o, sig_add21_2_o}, sig_add21_1_o}, sig_add21_0_o};
    end

    always @(a) begin: assig_process_sig_add21_0_i0
        sig_add21_0_i0 = a[0];
    end

    always @(b) begin: assig_process_sig_add21_0_i1
        sig_add21_0_i1 = b[0];
    end

    always @(a) begin: assig_process_sig_add21_1_i0
        sig_add21_1_i0 = a[1];
    end

    always @(b) begin: assig_process_sig_add21_1_i1
        sig_add21_1_i1 = b[1];
    end

    always @(a) begin: assig_process_sig_add21_2_i0
        sig_add21_2_i0 = a[2];
    end

    always @(b) begin: assig_process_sig_add21_2_i1
        sig_add21_2_i1 = b[2];
    end

    always @(a) begin: assig_process_sig_add21_3_i0
        sig_add21_3_i0 = a[3];
    end

    always @(b) begin: assig_process_sig_add21_3_i1
        sig_add21_3_i1 = b[3];
    end

    generate if (D_W != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```