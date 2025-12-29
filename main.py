opcodes = "nand or and nor add sub awc swc nop bra be bne bl bg ble bge load store 8load 8store push pull call ret cmp llpi lupi jmp bcc bcs key cmpi  nandi ori andi nori addi subi awci swci nopi brai bei bnei bli bgi blei bgei loadi storei 8loadi 8storei pushi pulli calli reti".split()
linecount = 0


def opcode_checker(opc):
    opc = opc.split()
    if opcodes.index(opc[0]) != -1:
        return(format(opcodes.index(opc[0]),"8b")[2:])
    else:
        raise KeyError(f"Invalid opcoce: {opc}")
    
def isnumeric(input_):
    for char in input_:
        if char not in "0123456789":
            return False
    return True

def register(reg):
    if isnumeric(reg):
        return(bin(reg)[2:])
    else:
        return(bin(reg[1:])[2:])
    
def encode(argument):
    print(f"line == '{argument}'")
    if argument[0] == "#":
        return ""
    if "#" in argument:
        res = ""
        for char in argument:
            if char == "#": break
            res += char
    else:
        res = argument
    argument = res
    argument = argument.split(",")
    opcode = argument[0]
    opcode_bin = opcode_checker(opcode)
    argument.append("")
    argument.append("")
    argument.append("")
    if argument[1] == "":   #handles nop, nopi, ret, reti, jmp, bcc, bcs, call, calli
        return(f"00000000000{opcode_bin[0:4]}0000000000{opcode_bin[5]}00000").strip()
    elif argument[2] == "":   #handles push, pushi, llpi, lupi, key, all branches, call, calli, pull, pulli
        if opcode in "pushi bra be bne bl bg ble bge call brai bei bnei bli bgi blei bgei calli":
            return(f"{register(argument[1])[5:16]}{opcode_bin[0:4]}00000{register(argument[1])[0:4]}{opcode_bin[5]}00000").strip()
        elif opcode in "pull pulli":
            return(f"00000000000{opcode_bin[0:4]}{register(argument[1])[0:4]}00000{opcode_bin[5]}00000").strip()
    elif argument[3] == "":
        if opcode in "store storei cmp cmpi":
            return(f"{register(argument[2])[5:16]}{opcode_bin[0:4]}00000{register(argument[2])[0:4]}{opcode_bin[5]}{register(argument[1])[0:4]}").strip()
        elif opcode in "load loadi":
            return(f"{register(argument[1])[5:16]}{opcode_bin[0:4]}{register(argument[2])[0:4]}{register(argument[1])[0:4]}{opcode_bin[5]}00000").strip()
    else:
        return(f"{register(argument[2])[5:16]}{opcode_bin[0:4]}{register(argument[1])[0:4]}{register(argument[2])[0:4]}{opcode_bin[5]}{register(argument[3])[0:4]} ").strip()
print(encode("nop #this is a nop"))
print(encode("addi r1,5,r2"))
