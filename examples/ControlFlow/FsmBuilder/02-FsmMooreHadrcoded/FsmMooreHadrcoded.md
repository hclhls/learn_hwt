# Arithmetic

HWT python source:

```python

class FsmMooreHadrcoded(Unit):
    
    def _declr(self):
        addClkRstn(self)
        self.a = Signal()
        self.b = Signal()
        self.dout = VectSignal(3)._m()

    def _impl(self):
        a = self.a
        b = self.b
        out = self.dout

        st = self._reg("st", Bits(3), 1)

        If(st._eq(1),
            If(a & b,
                st(3)
            ).Elif(b,
                st(2)
            )
        ).Elif(st._eq(2),
            If(a & b,
               st(3)
            ).Elif(a,
                st(1)
            )
        ).Elif(st._eq(3),
            If(a & ~b,
               st(1)
            ).Elif(~a & b,
                st(2)
            )
        ).Else(
            st(1)
        )

        Switch(st)\
        .Case(1,
            out(1)
        ).Case(2,
            out(2)
        ).Case(3,
            out(3)
        ).Default(
            out(None)
        )

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(FsmMooreHadrcoded(), serializer_cls=VerilogSerializer))
    
```

Execute the python script to generate Verilog:

```sh
python FsmMooreHadrcoded.py

```

The generated Verilog:

```verilog
module FsmMooreHadrcoded (
    input wire a,
    input wire b,
    input wire clk,
    output reg[2:0] dout,
    input wire rst_n
);
    reg[2:0] st = 3'b001;
    reg[2:0] st_next;
    always @(st) begin: assig_process_dout
        case(st)
            3'b001:
                dout = 3'b001;
            3'b010:
                dout = 3'b010;
            3'b011:
                dout = 3'b011;
            default:
                dout = 3'bxxx;
        endcase
    end

    always @(posedge clk) begin: assig_process_st
        if (rst_n == 1'b0)
            st <= 3'b001;
        else
            st <= st_next;
    end

    always @(a, b, st) begin: assig_process_st_next
        if (st == 3'b001)
            if (a & b)
                st_next = 3'b011;
            else if (b)
                st_next = 3'b010;
            else
                st_next = st;
        else if (st == 3'b010)
            if (a & b)
                st_next = 3'b011;
            else if (a)
                st_next = 3'b001;
            else
                st_next = st;
        else if (st == 3'b011)
            if (a & ~b)
                st_next = 3'b001;
            else if (~a & b)
                st_next = 3'b010;
            else
                st_next = st;
        else
            st_next = 3'b001;
    end

endmodule

```