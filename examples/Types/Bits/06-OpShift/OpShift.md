# Arithmetic

HWT python source:

```python

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class OpShift(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W, signed=True))
        self.c       = Signal(Bits(self.D_W))._m()
        self.d       = Signal(Bits(self.D_W))._m()
        self.e       = Signal(Bits(self.D_W))._m()
        self.f       = Signal(Bits(self.D_W))._m()
        self.g       = Signal(Bits(self.D_W))._m()

    def _impl(self):
        self.c(self.a >> 1)
        self.d(self.a << 2)
        self.e(self.b >> 3)
        self.f((self.b._reinterpret_cast(Bits(self.D_W+3, signed=True)) >> 3)._reinterpret_cast(Bits(self.D_W)))
        self.g(self.b << 4)


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(OpShift(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python OpShift.py

```

The generated Verilog:

```verilog
module OpShift #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    input wire signed[7:0] b,
    output reg[7:0] c,
    output reg[7:0] d,
    output reg[7:0] e,
    output reg[7:0] f,
    output reg[7:0] g
);
    always @(a) begin: assig_process_c
        c = {1'b0, a[7:1]};
    end

    always @(a) begin: assig_process_d
        d = {a[5:0], 2'b00};
    end

    always @(b) begin: assig_process_e
        e = {$signed(b[7:5]), $signed(b[7:3])};
    end

    always @(b) begin: assig_process_f
        reg[10:0] tmp_concat_0;
        reg signed[10:0] tmp_index_0;
        tmp_concat_0 = {{{b[7], b[7]}, b[7]}, $signed(b)};
        tmp_index_0 = $unsigned(tmp_concat_0);
        f = $signed(tmp_index_0[10:3]);
    end

    always @(b) begin: assig_process_g
        g = {$signed(b[3:0]), 4'h0};
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule


```