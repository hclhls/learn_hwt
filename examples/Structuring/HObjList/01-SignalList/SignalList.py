#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, VectSignal
from hwt.synthesizer.hObjList import HObjList

class SignalList(Unit):
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
    from hwt.serializer.hwt import HwtSerializer
    from hwt.serializer.vhdl import Vhdl2008Serializer
    from hwt.serializer.verilog import VerilogSerializer
    from hwt.serializer.systemC import SystemCSerializer

    print(to_rtl_str(SignalList(), serializer_cls=HwtSerializer))
    print(to_rtl_str(SignalList(), serializer_cls=Vhdl2008Serializer))
    print(to_rtl_str(SignalList(), serializer_cls=VerilogSerializer))
    print(to_rtl_str(SignalList(), serializer_cls=SystemCSerializer))
