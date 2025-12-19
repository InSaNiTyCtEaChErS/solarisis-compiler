generic_opcodes = "add sub mul mulh nand or and nor".split()
special_opcodes = "rec cmp awc swc bra jum key swap".split()
jump_opcodes = "nop jump je jne jl jg jle jge".split()
ram_opcodes = "load store push pull call ret dstore dload".split()
all_opcodes = generic_opcodes+special_opcodes+jump_opcodes+ram_opcodes

def opcode_checker(opc):
    if opc in all_opcodes:
        return(bin(all_opcodes.index(opc)))
    else:
        raise KeyError(f"Invalid opcoce: {opc}")
def register(reg):
    return(bin(reg[1:-1]))

def encode(argument):
    argument.split(" ")
    token_count = len(argument)
    opc = argument[0]
    opcode_binary = (opcode_checker(opc))
    if "i" in opc:
        immediate = 1
    if token_count == 1:  #handle registerless opcodes
        if opc in "nop ret bra jum":
            return(f"00000000 000{opcode_binary} 00000000 00000000")
        else:
            raise ValueError(f"invalid token in: {argument}")
    elif token_count == 2:  #handle opcodes with either rs2 or rd
        rs2 = opc[1]
        if opc in "call push swap jump je jne jl jg jle jge ": #rs2 opcodes
            return(f"{bin(rs2)[16:5]}{opcode_binary} 00000{bin(rs2)[4:0]}{immediate}00000")
        elif opc in "call rec key pull": #rd opcodes
            return(f"000000000 000{opcode_binary}{register(rs2)}000 00000000")
        else:
            raise ValueError(f"invalid token in: {argument}")
    elif token_count == 3:
        rs2 = opc[1]
        rd = opc[2]
        if opc in "cmp store dstore":
            return(f"{bin(rs2)[16:5]}{opcode_binary} {bin(rd)[4:0]}00000{immediate}{bin(rs2)[4:0]}")
        elif opc in "load dload":
            return(f"{bin(rs2)[16:5]}{opcode_binary} {bin(rd)[4:0]}{bin(rs2)[4:0]}{immediate}00000")
        else:
            raise ValueError(f"invalid token in: {argument}")
    elif token_count == 4:
        rs1 = opc[1]
        rs2 = opc[2]
        rd = opc[3]
        return(f"{bin(rs2)[16:5]}{opcode_binary} {bin(rd)[4:0]}{bin(rs2)[4:0]}{immediate}{bin(rs1)}")
    else:
        raise ValueError(f"invalid number of operands: {argument}")
    
print(encode("nop r1"))
