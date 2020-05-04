import itertools

givenTestCase = [0x20072000, 0x20e6fffd, 0x00072022, 0x00864020, 0x3105000f, 0x0085402a,
                 0xac082008, 0x20e70008, 0xace8fffc, 0x8c082004, 0x8ce50000]

myTestCase = [0x2084115c, 0x2001115c, 0x00812022, 0x200501a4, 0x30a60539, 0xac062000, 0x8c072000, 0xac070000]

instructions = {"0b000000": {"0b100000": "add", "0b100010": "sub", "0b101010": "slt",
                             "0b011010": "div", "0b010000": "mfhi", "0b000100": "sllv",
                             "0b000011": "sra", "0b001000": "jr", "0b100110": "xor",
                             "0b000000": "sll", "0b100100": "aand"},
                "0b001000": "addi", "0b001100": "andi", "0b100011": "lw", "0b101011": "sw", "0b000100": "beq",
                "0b000101": "bne", "0b000010": "j", "0b000011": "jal", "0b001110": "xori", "0b001010": "slti",
                }

file = open('Output.txt', 'w')

i_instructions, alu_instructions, r_instructions, memory_instructions, \
other_instructions, jump_instructions, branch_instructions = itertools.repeat(0, 7)

registers = {}  # created empty dictionary for registers
for x in range(32):
    registers.update({f'${x}': 0})
registers.update({'lo': 0, 'hi': 0})

dataMemory = {}  # created empty dictionary for dataMemory
for x in range(0x2E000, 0x3000, 4):
    dataMemory.update({x: 0})
dataMemory.update({0x2000: 0, 0x2004: 0})


def setPc(n=0):
    global pc
    # pc = n*
    pc = n


def incrementPc(n=1):
    global pc
    pc += n * 4


def reg(num):
    return "$" + str(num)

counter = 0
class ShowUpdate(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        global registers, counter

        old_registers = dict(registers)
        old_pc = int(pc)
        # old_data = registers[0x2000], registers[0x2004]
        incrementPc()
        self.f()

        print(assembly_language)
        for key in registers.keys():
            if registers[key] != old_registers[key]:
                pass
                print(f"\t\t{key}: {old_registers[key]} -> {registers[key]}")
        if old_pc != pc:
            print(f"\t\tpc: {'0x' + format(old_pc, '004X')} -> {'0x' + format(pc, '004X')}")
        #
        # if pc == 644:
        #     print(f"Counter: {registers[reg(2)]}, A: {dataMemory[0x2000]}, B: {dataMemory[0x2004]}")




        registers['$0'] = 0  # Register $0 is always 0.


@ShowUpdate
def sra():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}, ${rt}, {shamt}"
    registers[reg(rd)] = registers[reg(rt)] >> shamt


@ShowUpdate
def xori():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction}, ${rt}, ${rs}, {imm}"
    registers[reg(rt)] = registers[reg(rs)] ^ imm
    i_instructions += 1
    alu_instructions += 1


@ShowUpdate
def slti():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction}, ${rt}, ${rs}, {imm}"
    registers[reg(rt)] = 1 if registers[reg(rs)] < imm else 0
    i_instructions += 1
    alu_instructions += 1


@ShowUpdate
def xor():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}, ${rs}, ${rt}"
    registers[reg(rd)] = registers[reg(rs)] ^ registers[reg(rt)]
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def sllv():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}, ${rt}, ${rs}"
    registers[reg(rd)] = registers[reg(rt)] << registers[reg(rs)]
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def sll():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}, ${rt}, {shamt}"
    registers[reg(rd)] = registers[reg(rt)] << shamt
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def add():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}, ${rs}, ${rt}"
    registers[reg(rd)] = registers[reg(rs)] + registers[reg(rt)]
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def sub():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}, ${rs}, ${rt}"
    registers[reg(rd)] = registers[reg(rs)] - registers[reg(rt)]
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def aand():
    global assembly_language, i_instructions, registers, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\tand ${rd}, ${rs}, ${rt}"
    registers[reg(rd)] = registers[reg(rs)] & registers[reg(rt)]
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def slt():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}, ${rs}, ${rt}"
    registers[reg(rd)] = 1 if registers[reg(rs)] < registers[reg(rt)] else 0
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def addi():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction}, ${rt}, ${rs}, {imm}" if abs(
        imm) < 8192 else f"\t{instruction}, ${rt}, ${rs}, {hex(imm)}"
    registers[reg(rt)] = registers[reg(rs)] + imm
    i_instructions += 1
    alu_instructions += 1


@ShowUpdate
def andi():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction}, ${rt}, ${rs}, {imm}" if abs(
        imm) < 8192 else f"\t{instruction}, ${rt}, ${rs}, {hex(imm)}"
    registers[reg(rt)] = registers[reg(rs)] & imm
    i_instructions += 1
    alu_instructions += 1


@ShowUpdate
def lw():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rt}, {imm}(${rs})" if abs(
        imm) < 8192 else f"\t{instruction} ${rt}, {hex(imm)}(${rs})"
    a = dataMemory[(registers[reg(rs)] + imm)]
    registers[reg(rt)] = dataMemory[(registers[reg(rs)] + imm)]
    i_instructions += 1
    memory_instructions += 1


@ShowUpdate
def sw():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rt}, {imm}(${rs})" if abs(
        imm) < 8192 else f"\t{instruction} ${rt}, {hex(imm)}(${rs})"
    dataMemory[registers[reg(rs)] + imm] = registers[reg(rt)]
    i_instructions += 1
    memory_instructions += 1


@ShowUpdate
def div():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction}, ${rs}, %{rt}"
    registers["lo"] = int(registers[reg(rs)] / registers[reg(rt)])
    registers["hi"] = int(registers[reg(rs)] % registers[reg(rt)])
    r_instructions += 1
    alu_instructions += 1


@ShowUpdate
def mfhi():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rd}"
    registers[reg(rd)] = registers["hi"]
    other_instructions += 1


@ShowUpdate
def beq():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction}, ${rs}, ${rt}, {imm}" if abs(
        imm) < 8192 else f"\t{instruction}, ${rs}, ${rt}, {hex(imm)}"
    if registers[reg(rs)] == registers[reg(rt)]:
        incrementPc(imm)
    else:
        pass
    jump_instructions += 1
    branch_instructions += 1


@ShowUpdate
def bne():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction}, ${rs}, ${rt}, {imm}" if abs(
        imm) < 8192 else f"\t{instruction}, ${rs}, ${rt}, {hex(imm)}"
    if registers[reg(rs)] == registers[reg(rt)]:
        pass
    else:
        incrementPc(imm)
    jump_instructions += 1
    branch_instructions += 1


@ShowUpdate
def j():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} {jumpi * 4}" if abs(imm) < 8192 else f"\t{instruction} {hex(jumpi)}"
    setPc(int(4 * jumpi))
    jump_instructions += 1
    branch_instructions += 1


@ShowUpdate
def jr():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} ${rs}"
    setPc(registers[reg(31)])
    jump_instructions += 1
    branch_instructions += 1


@ShowUpdate
def jal():
    global assembly_language, registers, i_instructions, alu_instructions, r_instructions, memory_instructions, \
        other_instructions, r_instructions, jump_instructions, branch_instructions
    assembly_language = f"\t{instruction} {jumpi * 4}" if abs(imm) < 8192 else f"\t{instruction} {hex(jumpi)}"
    registers[reg(31)] = int(pc)
    setPc(int(4 * jumpi))
    jump_instructions += 1
    branch_instructions += 1


i = ""
rd = ""
rt = ""
rs = ""
op = ""
shamt = ""
jumpi = ""
assembly_language = ""
imm = 0
instruction = ""


# This was stolen from StackOverflow
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)  # compute negative value
    return val  # return positive value as is


def register_contents():
    global pc, file
    print("______________________")
    print(" registers |   value |")
    for register in registers:
        if (register == 'lo'):
            print("lo          %7d" % (registers[register]))
        elif (register == 'hi'):
            print("hi          %7d" % (registers[register]))
        else:
            print("$%3d     %10d    " % (int(register[1:]), registers[register]))
    print("pc             %5d       " % (pc))


def instruction_statistics():
    global file
    total_instructions = alu_instructions + other_instructions + branch_instructions + jump_instructions + memory_instructions
    print("       instruction_statistics             ")
    print(" _____________________________________________")
    print("|type:   | operations  | percentage          |")
    print("|ALU         %5d             %8.2f       " % (
        alu_instructions, ((alu_instructions / total_instructions) * 100)))
    print("|Jumps       %5d             %8.2f       " % (
        jump_instructions, ((jump_instructions / total_instructions) * 100)))
    print("|Branch      %5d             %8.2f      " % (
        branch_instructions, ((branch_instructions / total_instructions) * 100)))
    print("|Memory      %5d             %8.2f      " % (
        memory_instructions, ((memory_instructions / total_instructions) * 100)))
    print("|Other       %5d             %8.2f       " % (
        other_instructions, ((other_instructions / total_instructions) * 100)))
    print("total_instructions = {}".format(total_instructions))


def instruction_counter():
    global file
    total_instructions = r_instructions + i_instructions + jump_instructions
    print(" \n      instruction_counter          ")
    print(" ________________________________________________")
    print("|type:   | operations  | percentage             |")
    print("|R-type      %5d          %8.2f      " % (r_instructions, ((r_instructions / total_instructions) * 100)))
    print("|I-type      %5d          %8.2f     " % (i_instructions, ((i_instructions / total_instructions) * 100)))
    print(
        "|J-type      %5d          %8.2f      " % (jump_instructions, ((jump_instructions / total_instructions) * 100)))
    print("total_instructions = {} \n".format(total_instructions))


def memory_contents():
    global file
    print("\n_____Memory content________")
    file.write("\n_____Memory content________\n")
    for x in dataMemory:
        if dataMemory[x] != 0 or x == 0x2000 or x == 0x2004:
            print("address x: {}   ~ contains: {} ".format(hex(x), dataMemory[x]))


def machine_to_assembly(textfile):
    global i
    global rd
    global rt
    global rs
    global op
    global shamt
    global jumpi
    global assembly_language
    global imm
    global instruction

    assembly_languages = []

    print(f"\n\n\nFrom {textfile}:\n")
    with open(textfile) as machine_codes_text:
        max_pc = 0
        setPc(0)
        machine_codes = []
        for machine_code in machine_codes_text:
            max_pc += 4
            machine_codes.append(machine_code)

        while pc < max_pc:
            machine_code = machine_codes[int(pc / 4)]

            machine_code = int(machine_code, 16)  # change the hex string into an int
            machine_code = format(machine_code, '#034b')  # change the int into a binary string

            i = machine_code[23:]
            rd = str(machine_code[18:23])
            rt = str(machine_code[13:18])
            rs = str(machine_code[8:13])
            op = str(machine_code[0:8])  # if 0, instruction is r-type
            shamt = str(machine_code[-11:-6])
            jumpi = str(machine_code[9:])

            r_type = True if op == "0b000000" else False

            if r_type:
                funct = "0b" + i[-6:]

            imm = twos_comp(int(i, 2), 16) if r_type else twos_comp(int((rd + i), 2), 16)

            rd = int(rd, 2)
            rt = int(rt, 2)
            rs = int(rs, 2)
            shamt = int(shamt, 2)
            jumpi = int(jumpi, 2)

            instruction = instructions[op][funct] if r_type else instructions[op]
            pythonInstruction = globals()[instruction]
            pythonInstruction()

            assembly_languages.append(assembly_language)


    memory_contents()
    register_contents()
    instruction_counter()
    instruction_statistics()



machine_to_assembly("testcaseA_hex_dump.txt")
#machine_to_assembly("testcaseB_hex_dump.txt")
#machine_to_assembly("testcaseC_hex_dump.txt")
#machine_to_assembly("testcaseD_hex_dump.txt")

# machine_to_assembly("perceptron_v1.txt")
# machine_to_assembly("perceptron_v2.txt")
