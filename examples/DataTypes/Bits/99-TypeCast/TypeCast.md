# TypeCast

HWT python source:

```python
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal

class TypeCast(Unit):
    def _config(self):
        self.D_W = Param(8)

    def _declr(self):
        self.a       = Signal(Bits(self.D_W))
        self.b       = Signal(Bits(self.D_W,   signed=True))
        self.a_add_b = Signal(Bits(self.D_W+1, signed=True))._m()

    def _impl(self):
        self.a_signed = self._sig(name="a_signed", dtype=Bits(self.D_W,   signed=True))

        self.a_signed(self.a._auto_cast(self.a_signed._dtype))

        self.a_add_b (self.a_signed._reinterpret_cast(self.a_add_b._dtype) +  self.b._reinterpret_cast(self.a_add_b._dtype))


if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer

    print(to_rtl_str(TypeCast(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python TypeCast.py

```

The generated Verilog:

```verilog
module TypeCast #(
    parameter D_W = 8
) (
    input wire[7:0] a,
    output reg signed[8:0] a_add_b,
    input wire signed[7:0] b
);
    reg signed[7:0] a_signed;
    always @(a_signed, b) begin: assig_process_a_add_b
        reg[8:0] tmp_concat_0;
        reg[8:0] tmp_concat_1;
        tmp_concat_0 = {a_signed[7], $signed(a_signed)};
        tmp_concat_1 = {b[7], $signed(b)};
        a_add_b = $unsigned(tmp_concat_0) + $unsigned(tmp_concat_1);
    end

    always @(a) begin: assig_process_a_signed
        a_signed = $unsigned(a);
    end

    generate if (D_W != 8)
        $error("%m Generated only for this param value");
    endgenerate

endmodule


```