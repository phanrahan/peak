import typing as  tp
import operator
from .isa import *
import functools as ft

from hwtypes import AbstractBitVector

def gen_alu(BV_t : tp.Type['AbstractBitVector']):
    Bit = BV_t[1]
    Data = BV_t[DATAWIDTH]

    def PE(inst : INST, data0 : Data, data1 : Data):
        def alu(inst : ALU_INST, data0 : Data, data1 : Data, bit0 : Bit):
            if inst == ALU_INST.Add:
                res, carry = data0.adc(data1, bit0)
            elif inst == ALU_INST.And:
                res = data0 & data1
                carry = Bit(0)
            elif inst == ALU_INST.Xor:
                res = data0 ^ data1
                carry = Bit(0)
            elif inst == ALU_INST.Shft:
                res = data0.bvshl(data1)
                carry = Bit(0)
            else:
                raise TypeError()

            zero = ~ft.reduce(operator.or_, res, Bit(0))
            return res, carry, zero

        bit0 = Bit(0)
        res, _, _ = alu(inst.ALU, data0, data1, bit0)
        flag_out = Bit(0)
        return res, flag_out

    in_width_map = {
            'data0' : DATAWIDTH,
            'data1' : DATAWIDTH,
    }
    out_width_map = {
            0 : DATAWIDTH,
            1 : 1,
    }
    return PE, in_width_map, out_width_map
