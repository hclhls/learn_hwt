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
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.i0 = VectSignal(self.D_W)
        self.i1 = VectSignal(self.D_W)
        self.o  = VectSignal(self.D_W)._m()

    def _impl(self):
        self.o(self.i0 & self.i1)

@serializeParamsUniq
class WithParameterizedSubModule(Unit):
    def _config(self):
        self.D_W = Param(4)

    def _declr(self):
        self.a  = VectSignal(self.D_W)
        self.b  = VectSignal(self.D_W)
        self.c  = VectSignal(self.D_W)._m()      

        self.add21 = HObjList([])
        for _ in range(self.D_W//2):
            self.add21.append(SubModule())
            self.add21[-1].D_W = self.D_W//2

    def _impl(self):        
        for idx, subm in enumerate(self.add21):
            subm.i0(self.a[idx*2+2:idx*2])
            subm.i1(self.b[idx*2+2:idx*2])
            self.c[idx*2+2:idx*2](subm.o)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(WithParameterizedSubModule(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python WithParameterizedSubModule.py

```

The generated Verilog:

```verilog
module SubModule #(
    parameter D_W = 2
) (
    input wire[1:0] i0,
    input wire[1:0] i1,
    output reg[1:0] o
);
    always @(i0, i1) begin: assig_process_o
        o = i0 & i1;
    end

    generate if (D_W != 2)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module WithParameterizedSubModule #(
    parameter D_W = 4
) (
    input wire[3:0] a,
    input wire[3:0] b,
    output reg[3:0] c
);
    reg[1:0] sig_add21_0_i0;
    reg[1:0] sig_add21_0_i1;
    wire[1:0] sig_add21_0_o;
    reg[1:0] sig_add21_1_i0;
    reg[1:0] sig_add21_1_i1;
    wire[1:0] sig_add21_1_o;
    SubModule #(
        .D_W(2)
    ) add21_0_inst (
        .i0(sig_add21_0_i0),
        .i1(sig_add21_0_i1),
        .o(sig_add21_0_o)
    );

    SubModule #(
        .D_W(2)
    ) add21_1_inst (
        .i0(sig_add21_1_i0),
        .i1(sig_add21_1_i1),
        .o(sig_add21_1_o)
    );

    always @(sig_add21_0_o, sig_add21_1_o) begin: assig_process_c
        c = {sig_add21_1_o, sig_add21_0_o};
    end

    always @(a) begin: assig_process_sig_add21_0_i0
        sig_add21_0_i0 = a[1:0];
    end

    always @(b) begin: assig_process_sig_add21_0_i1
        sig_add21_0_i1 = b[1:0];
    end

    always @(a) begin: assig_process_sig_add21_1_i0
        sig_add21_1_i0 = a[3:2];
    end

    always @(b) begin: assig_process_sig_add21_1_i1
        sig_add21_1_i1 = b[3:2];
    end

    generate if (D_W != 4)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```