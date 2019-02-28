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
            carry = Bit(0)
            zero = Bit(0)
            if inst == ALU_INST.Add:
                res, carry = data0.adc(data1, bit0)
            elif inst == ALU_INST.And:
                res = bit0.ite(data0 & data1, data0 | data1)
            elif inst == ALU_INST.Xor:
                res = data0 ^ data1
                zero = bit0
            elif inst == ALU_INST.Shft:
                res = bit0.ite(data0.bvshl(data1), data0.bvlshr(data1))
            else:
                raise TypeError()

            zero ^= ~ft.reduce(operator.or_, res, Bit(0))
            return res, carry, zero

        def flag_mux(inst : FLAG_INST, carry, zero):
            if inst == FLAG_INST.C:
                return carry
            elif inst ==  FLAG_INST.Z:
                return zero
            else:
                raise TypeError()

        def inverter(inst : INVERTER_INST, data):
            if inst == INVERTER_INST.Invert:
                return ~data
            elif inst == INVERTER_INST.Ident:
                return data
            else:
                raise TypeError()

        bit0 = Bit(inst.BIT.value)
        data1 = inverter(inst.INVERTER, data1)
        res, carry, zero = alu(inst.ALU, data0, data1, bit0)
        flag_out = flag_mux(inst.FLAG, carry, zero)
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
