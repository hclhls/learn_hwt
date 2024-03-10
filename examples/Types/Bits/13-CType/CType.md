# Arithmetic

HWT python source:

```python

from hwt.code import Concat, replicate
from hwt.synthesizer.unit import Unit
from hwt.interfaces.std import Signal
from hwtLib.types.ctypes import uint32_t, int32_t, uint16_t, int16_t, uint8_t, int8_t


class CType(Unit):
    
    def _declr(self):
        self.a        = Signal(uint8_t)
        self.a_signed = Signal(int8_t)
        self.b        = Signal(uint16_t)._m()
        self.b_signed = Signal(int16_t)._m()
        self.c        = Signal(uint32_t)._m()
        self.c_signed = Signal(int32_t)._m()
        

    def _impl(self):
        self.b(Concat(self.a,self.a))
        self.b_signed(Concat(self.a_signed,self.a))
        self.c(Concat(self.b,self.b))
        self.c_signed(Concat(self.b_signed,self.b))
        

if __name__ == "__main__":

    from hwt.synthesizer.utils import to_rtl_str
    from hwt.serializer.verilog import VerilogSerializer
    
    print(to_rtl_str(CType(), serializer_cls=VerilogSerializer))

```

Execute the python script to generate Verilog:

```sh
python CType.py

```

The generated Verilog:

```verilog
module CType (
    input wire[7:0] a,
    input wire signed[7:0] a_signed,
    output reg[15:0] b,
    output reg signed[15:0] b_signed,
    output reg[31:0] c,
    output reg signed[31:0] c_signed
);
    always @(a) begin: assig_process_b
        reg[15:0] tmp_concat_0;
        tmp_concat_0 = {a, a};
        b = tmp_concat_0;
    end

    always @(a, a_signed) begin: assig_process_b_signed
        reg[15:0] tmp_concat_0;
        tmp_concat_0 = {$signed(a_signed), a};
        b_signed = $unsigned(tmp_concat_0);
    end

    always @(b) begin: assig_process_c
        reg[31:0] tmp_concat_0;
        tmp_concat_0 = {b, b};
        c = tmp_concat_0;
    end

    always @(b, b_signed) begin: assig_process_c_signed
        reg[31:0] tmp_concat_0;
        tmp_concat_0 = {$signed(b_signed), b};
        c_signed = $unsigned(tmp_concat_0);
    end

endmodule

```