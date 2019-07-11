from peak.assembler.assembler import Assembler
from examples.demo_pes.pe5.isa import INST as pe5_isa
from examples.arm.isa import Inst as arm_isa
from examples.pico.isa import Inst as pico_isa
from hwtypes import AbstractBitVector
from hwtypes.adt import Enum, Product, Tuple, Sum
from hwtypes.adt import new_instruction
from hwtypes import BitVector
import pytest


@pytest.mark.parametrize("isa", [pe5_isa, arm_isa, pico_isa])
def test_assembler_disassembler(isa):
    assembler = Assembler(isa)
    for inst in isa.enumerate():
        opcode = assembler.assemble(inst)
        assert isinstance(opcode, BitVector[assembler.width])
        assert assembler.disassemble(opcode) == inst

        for name,field in isa.field_dict.items():
            sub_asssembler = Assembler(field)
            assert getattr(assembler.sub, name).asm is sub_asssembler
            assert assembler.sub[name].asm is sub_asssembler

            if issubclass(field, (Product, Tuple)) \
                    or (issubclass(field, Sum)
                        and inst.value_dict[name] is not None):
                sub_opcode = opcode[assembler.sub[name].idx]
                assert sub_opcode.size <= sub_asssembler.width
                sub_inst = sub_asssembler.disassemble(sub_opcode)
                assert isinstance(sub_inst, field)
                assert sub_inst == inst.value_dict[name]

def test_enum_determinism():
    def assemble():
        class ALUOP(Enum):
            Add = new_instruction()
            Sub = new_instruction()
            Or =  new_instruction()
            And = new_instruction()
            XOr = new_instruction()

        assembler = Assembler(ALUOP)
        instr_bv = assembler.assemble(ALUOP.Or)
        return int(instr_bv)
    val = assemble()
    for _ in range(100):
        assert val == assemble()

def test_product_determinism():
    def assemble():
        class ALUOP(Enum):
            Add = new_instruction()
            Sub = new_instruction()
            Or =  new_instruction()
            And = new_instruction()
            XOr = new_instruction()

        class Inst(Product):
            alu_op1 = ALUOP
            alu_op2 = ALUOP

        assembler = Assembler(Inst)
        instr_bv = assembler.assemble(Inst(ALUOP.Add, ALUOP.Sub))
        return int(instr_bv)
    val = assemble()
    for _ in range(100):
        assert val == assemble()

def test_sum_determinism():
    def assemble():
        class OP1(Enum):
            Add = new_instruction()
            Sub = new_instruction()

        class OP2(Enum):
            Or =  new_instruction()
            And = new_instruction()
            XOr = new_instruction()


        class Inst(Sum[OP1, OP2]): pass

        assembler = Assembler(Inst)
        add_instr = Inst(OP1.Add)
        instr_bv = assembler.assemble(add_instr)
        return int(instr_bv)

    val = assemble()
    for _ in range(100):
        assert val == assemble()
