from hwtypes.adt import Enum, Product, Sum
from hwtypes.modifiers import new
from peak.bitfield import bitfield
from hwtypes import BitVector, Bit

WIDTH = 12
Word = BitVector[WIDTH]

# Direct vs indirect addressing
@bitfield(3)
class IA(Enum): 
    DIRECT = 0
    INDIRECT = 1

# Page
@bitfield(4)
class MP(Enum): 
    PAGE_ZERO = 0
    CURRENT_PAGE = 1

Addr= bitfield(5)(new(BitVector, 7, name='Addr'))

class MRI(Product):
    i = IA
    p = MP
    addr = Addr

class AND(MRI): pass
class TAD(MRI): pass
class ISZ(MRI): pass
class DCA(MRI): pass
class JMS(MRI): pass
class JMP(MRI): pass

@bitfield(3)
class IOT(Product):
    pass

@bitfield(4)
class OPR1(Product):
    cla = Bit # clear accumulator 1
    cll = Bit # clear link 1
    cma = Bit # complement accumulator 2
    cml = Bit # complelemnt link 2
    rar = Bit # rotate right 4
    ral = Bit # rotate left 4
    twice = Bit # rotate twice
    iac = Bit # increment accumulator 3

@bitfield(4)
class OPR2(Product):
    cla = Bit # clear accumulator 2
    sma = Bit # skip on minus (negastive) accumulator 1
    sza = Bit # skip on zero accumulator 1
    snl = Bit # skip on non-zero link 1
    skip = Bit # reverse skip 1
    osr = Bit # or switch register with accumulator 2
    hlt = Bit # halt 3
    NOP = Bit

@bitfield(3)
class OPR(Sum[OPR1, OPR2]): pass

@bitfield(0)
class Inst(Sum[AND, TAD, ISZ, DCA, JMS, JMP, IOT, OPR]): pass