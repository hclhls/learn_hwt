# Arithmetic

HWT python source:

```python

from hwt.code import FsmBuilder, Switch, If
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.interfaces.std import Signal, VectSignal
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.unit import Unit

class FsmMealy(Unit):

    def _declr(self):
        addClkRstn(self)
        self.a = Signal()
        self.b = Signal()
        self.dout = VectSignal(3)._m()

    def _impl(self):
        # :note: stT member names are colliding with port names and thus
        #     they will be renamed in HDL
        stT = HEnum("st_t", ["a", "b", "aAndB"])

        a = self.a
        b = self.b
        out = self.dout

        st = FsmBuilder(self, stT)\
        .Trans(stT.a,
            (a & b, stT.aAndB),
            (b, stT.b)
        ).Trans(stT.b,
            (a & b, stT.aAndB),
            (a, stT.a)
        ).Trans(stT.aAndB,
            (a & ~b, stT.a),
            (~a & b, stT.b),
        ).stateReg

        If(st._eq(stT.a) & b,
            out(1)
        ).Elif(st._eq(stT.b) & a,
            out(2) 
        ).Elif(st._eq(stT.aAndB) & (~a),
            out(3)
        ).Elif(st._eq(stT.aAndB) & (~b),
            out(4)
        ).Else(
            out(0)
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(FsmMealy(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python FsmMealy.py

```

The generated Verilog:

```verilog
module FsmMealy (
    input wire a,
    input wire b,
    input wire clk,
    output reg[2:0] dout,
    input wire rst_n
);
    reg[1:0] st = 0;
    reg[1:0] st_next;
    always @(a, b, st) begin: assig_process_dout
        if (st == 0 & b == 1'b1)
            dout = 3'b001;
        else if (st == 1 & a == 1'b1)
            dout = 3'b010;
        else if (st == 2 & a == 1'b0)
            dout = 3'b011;
        else if (st == 2 & b == 1'b0)
            dout = 3'b100;
        else
            dout = 3'b000;
    end

    always @(posedge clk) begin: assig_process_st
        if (rst_n == 1'b0)
            st <= 0;
        else
            st <= st_next;
    end

    always @(a, b, st) begin: assig_process_st_next
        case(st)
            0:
                if (a & b)
                    st_next = 2;
                else if (b)
                    st_next = 1;
                else
                    st_next = st;
            1:
                if (a & b)
                    st_next = 2;
                else if (a)
                    st_next = 0;
                else
                    st_next = st;
            default:
                if (a & ~b)
                    st_next = 0;
                else if (~a & b)
                    st_next = 1;
                else
                    st_next = st;
        endcase
    end

endmodule

```