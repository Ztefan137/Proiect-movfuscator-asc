import re

#vezi codul?

#yes super

#unde e


def get_line_type(line):
    if "mov" in line:
        return 0
    if "add" in line:
        return 1
    if "sub" in line:
        return 1
    if "mul" in line:
        return 1
    if "div" in line:
        return 1
    if "inc" in line:
        return 1
    if "dec" in line:
        return 1
    if "imul" in line:
        return 1
    if "cmp" in line:
        return 3
    if "je" in line:
        return 2
    if "jb" in line:
        return 2
    if "ja" in line:
        return 2
    if "jbe" in line:
        return 2
    if "jae" in line:
        return 2
    if "jne" in line:
        return 2
    if "jmp" in line:
        return 2
    if "int $0x80" in line:
        return 10
    if ".long" in line:
        return 30
    if ".word" in line:
        return 30
    if ".ascii" in line:
        return 30
    if ".asciz" in line:
        return 30
    if ".space" in line:
        return 30
    if ":" in line:
        return 20
    if "." in line:
        return 100

#compiler fun!!!!!!!

keywords=["add","sub","inc","dec","jmp"]
def get_line_tokens(line):
    line=line.replace(","," ")
    line=line.split()
    return line
def get_line_type(line):
    keyword=get_line_tokens(line)[0]
    arithmetic_keywords=["add","sub","mul","imul","div","idiv","inc","dec"]
    flow_keywords=["jmp","jb","jbe","ja","jae","jl","jle","jg","jge","je","jne","loop"]
    shift_keywords=["shr","shl","sar","sal"]
    logical_keywords=["and","or","xor","not"]
    decisional_keywords=["cmp","test"]
    if '.' in keyword:
        return "section"
    elif ':' in keyword:
        return "label"
    elif "int" in keyword:
        return "syscall"
    elif "mov" in keyword:
        return "move"
    else:
        for arithmetic_keyword in arithmetic_keywords:
            if arithmetic_keyword in keyword: 
                return "arithmetic"
        for flow_keyword in flow_keywords:
            if flow_keyword in keyword: 
                return "control flow"
        for shift_keyword in shift_keywords:
            if shift_keyword in keyword: 
                return "shift"
        for logical_keyword in logical_keywords:
            if logical_keyword in keyword: 
                return "logical"
        for decisional_keyword in decisional_keywords:
            if decisional_keyword in keyword: 
                return "decisional"
    return "other"

def get_label_idx(label):
    for idx in range(len(asm_lines)):
        if f"{label}:" == asm_lines[idx]:
            return idx+1
def check_loop_existance():
    global loop_existance
    for idx in range(len(asm_lines)):
        line=asm_lines[idx]
        if get_line_type(line) == "control flow" :
            label=get_line_tokens(line)[1]
            if get_label_idx(label)<idx+1:
                loop_existance=True

def identify_syscalls():
    global syscalls
    for idx in range(len(asm_lines)):
        line=asm_lines[idx]
        if get_line_type(line) == "syscall" :
            syscalls[idx+1]="syscall"

def get_mov_instructions(line):
    return 
    g.write(f"\t{line}\n")
def write_if(changed_data,if_start_line,if_end_line,else_start_line,else_end_line):
    print(changed_data)
    print(asm_lines)
    print(asm_lines[if_start_line])
    print(asm_lines[if_start_line+1:if_end_line+2])
    print(asm_lines[else_start_line+1:else_end_line+2])
    #stocare date initiale
    #scrie branch if
    #stocare date if
    #undload date initiale
    #scrie branch else
    #load date else peste initiale
    #initializeaza operanzii de comparatie 
    #codul care verifica egalitatea
    #unloadul datelor

f=open("C:/Users/stefa/OneDrive/Desktop/proiecte/python/proiect_asc/cod.txt",'r')
g=open("C:/Users/stefa/OneDrive/Desktop/proiecte/python/proiect_asc/cod2.txt",'w')
line_classification={}
asm_lines=[line.strip() for line in f.readlines()]

#program flags
loop_existance=False
if_existance=True
syscalls={}
'''
line_idx=0
for line in asm_lines:
    line_idx+=1
    line_classification[line]=get_line_type(line)
    if get_line_type(line) == None:
        print(f"error: unknown data type at line {line_idx}")
    print(get_line_tokens(line),get_line_type(line))

#declarari
#.data
g.write(".data\n")
#tabel adunari
g.write("\tinc_adress: .byte 0\n")
g.write("\tinc: .byte ")
for i in range(256):
    g.write(f"{i},")
g.write("\n")
g.write("\tinc_offset: .byte 0\n")
#.bss
g.write(".bss\n")
#.text
g.write(".text\n")
#.global main
g.write(".global main\n")

#.text
for line in asm_lines:
    if line_classification[line] == 20:
        g.write(f"{line}\n")
    if line_classification[line] == 0:
        g.write(f"\t{line}\n")
    if line_classification[line] == 1:
        if "inc" in line or "dec" in line:
            offset=0
            operand=line.split(" ")[1]
            if "dec" in line:
                offset=0
            if "inc" in line:
                offset=2
            if "%" in operand:
                operand_low="%"+operand[2]+"l"
                g.write(f"\tmov $0, %ecx\n")
                g.write(f"\tmov {operand_low}, %cl\n")
                g.write(f"\tmov $inc_adress, %edi\n")
                g.write(f"\tmov $0,{operand}\n")
                g.write(f"\tmov {offset}(%edi,%ecx,1), %cl\n")
                g.write(f"\tmov %cl, {operand_low}\n")
            else:                    
                g.write(f"\tmov $0, %ecx\n")
                g.write(f"\tmov {operand}, %cl\n")
                g.write(f"\tmov $inc_adress, %edi\n")
                g.write(f"\tmov {offset}(%edi,%ecx,1), %cl\n")
                g.write(f"\tmov %cl, {operand}\n")
            g.write("\n")
        if "add" in line or "sub" in line:
            offset=0
            operand=line.split(",")[1].strip()
            operand_src=line.split(" ")[1]
            operand_src=operand_src.split(",")[0].strip()
            print(operand,operand_src)
            if "%" in operand:
                operand_src_low="%"+operand_src[2]+"l"
                offset=operand_src_low
            else:
                offset=operand_src
            if "%" in operand:
                operand_low="%"+operand[2]+"l"
                g.write(f"\tmov $0, %ecx\n")
                g.write(f"\tmov {operand_low}, %cl\n")
                g.write(f"\tmov $inc_adress, %edi\n")
                g.write(f"\tmov $0,{operand}\n")
                g.write(f"\tmovb {offset},inc_offset\n")
                g.write(f"\tmov inc_offset(%edi,%ecx,1), %cl\n")
                g.write(f"\tmov %cl, {operand_low}\n")
            else:                    
                g.write(f"\tmov $0, %ecx\n")
                g.write(f"\tmov {operand}, %cl\n")
                g.write(f"\tmov $inc_adress, %edi\n")
                g.write(f"\tmovb {offset},inc_offset\n")
                g.write(f"\tmov inc_offset(%edi,%ecx,1), %cl\n")
                g.write(f"\tmov %cl, {operand}\n")
            g.write("\n")
#exit
g.write("exit:\n")
g.write("\t")
g.write("mov $0,%eax\n")
g.write("\t")
g.write("mov $0,0(%eax)\n")
'''

    
#etapa de analiza
    #urmarim foruri
        #un flag prezenta_foruri
        #2 metadate numerice despre adancimea forurilor imbricate si adancimea ifurilor imbricate
        #pozitia apelurilor de sistem
    
for line in asm_lines:
    print(get_line_tokens(line),get_line_type(line))

print("program meta-data:")
check_loop_existance()
print(f"loop_existance: {loop_existance}")
identify_syscalls()
print(f"system calls: {syscalls}")


#etapa de formatare a datelor
#formatare .data
g.write(".data\n")
#formatare .bss
g.write(".bss\n")
#formatare .text
g.write(".text\n")
#formatare .global main
g.write(".global main\n")

instructions_start_index=asm_lines.index(".global main")

if not loop_existance:
    if not if_existance:
        for line in asm_lines[instructions_start_index:]:
            if get_line_type(line) == "label":
                g.write(f"{line}\n")
            elif get_line_type(line) in ["move","syscall"]:
                g.write(f"\t{line}\n")
            else:
                get_mov_instructions(line)
    else:
        write_if(["%eax","%ebx","%ecx"],18,19,20,20)
else:
    g.write("mult noroc") 
#etapa de formatare a ifurilor
#etapa de formatare a operatiilor aritmetice/logice


f.close()
g.close()
