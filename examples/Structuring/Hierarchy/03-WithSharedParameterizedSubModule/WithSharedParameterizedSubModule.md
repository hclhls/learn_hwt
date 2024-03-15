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
        self.D1_W = Param(8)
        self.D2_W = Param(8)

    def _declr(self):
        self.i0 = VectSignal(self.D1_W)
        self.i1 = VectSignal(self.D1_W)
        self.i2 = VectSignal(self.D2_W)
        self.i3 = VectSignal(self.D2_W)
        self.o0 = VectSignal(self.D1_W)._m()
        self.o1 = VectSignal(self.D2_W)._m()

    def _impl(self):
        self.o0(self.i0 & self.i1)
        self.o1(self.i3 | self.i2)

@serializeParamsUniq
class WithSharedParameterizedSubModule(Unit):
    def _config(self):
        self.D1_W = Param(4)
        self.D2_W = Param(3)

    def _declr(self):
        self.a0  = VectSignal(self.D1_W)
        self.b0  = VectSignal(self.D1_W)
        self.c0  = VectSignal(self.D1_W)._m()
        self.a1  = VectSignal(self.D2_W)
        self.b1  = VectSignal(self.D2_W)
        self.c1  = VectSignal(self.D2_W)._m()       

        with self._paramsShared():
            self.subm = SubModule()

    def _impl(self):        
        self.subm.i0(self.a0)
        self.subm.i1(self.b0)
        self.c0(self.subm.o0)
        self.subm.i2(self.a1)
        self.subm.i3(self.b1)
        self.c1(self.subm.o1)
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
   
    print(to_rtl_str(WithSharedParameterizedSubModule(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python WithSharedParameterizedSubModule.py

```

The generated Verilog:

```verilog
module SubModule #(
    parameter D1_W = 4,
    parameter D2_W = 3
) (
    input wire[3:0] i0,
    input wire[3:0] i1,
    input wire[2:0] i2,
    input wire[2:0] i3,
    output reg[3:0] o0,
    output reg[2:0] o1
);
    always @(i0, i1) begin: assig_process_o0
        o0 = i0 & i1;
    end

    always @(i2, i3) begin: assig_process_o1
        o1 = i3 | i2;
    end

    generate if (D1_W != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (D2_W != 3)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
module WithSharedParameterizedSubModule #(
    parameter D1_W = 4,
    parameter D2_W = 3
) (
    input wire[3:0] a0,
    input wire[2:0] a1,
    input wire[3:0] b0,
    input wire[2:0] b1,
    output wire[3:0] c0,
    output wire[2:0] c1
);
    wire[3:0] sig_subm_i0;
    wire[3:0] sig_subm_i1;
    wire[2:0] sig_subm_i2;
    wire[2:0] sig_subm_i3;
    wire[3:0] sig_subm_o0;
    wire[2:0] sig_subm_o1;
    SubModule #(
        .D1_W(4),
        .D2_W(3)
    ) subm_inst (
        .i0(sig_subm_i0),
        .i1(sig_subm_i1),
        .i2(sig_subm_i2),
        .i3(sig_subm_i3),
        .o0(sig_subm_o0),
        .o1(sig_subm_o1)
    );

    assign c0 = sig_subm_o0;
    assign c1 = sig_subm_o1;
    assign sig_subm_i0 = a0;
    assign sig_subm_i1 = b0;
    assign sig_subm_i2 = a1;
    assign sig_subm_i3 = b1;
    generate if (D1_W != 4)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (D2_W != 3)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

```