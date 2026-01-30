#-----------------------------#
#functii de utilitate generala#
#-----------------------------#
def get_line_tokens(line): #functie de utilitate generala
    if "," in line:
        line=line.replace(","," ")
    line=line.split()
    return line
def get_line_type(line): #functie de utilitate generala
    keyword=get_line_tokens(line)[0]
    arithmetic_keywords=["add","sub","mul","imul","div","idiv","inc","dec"]
    flow_keywords=["jmp","jb","jbe","ja","jae","jl","jle","jg","jge","je","jne"]
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
def negate_conditional_jump(jump):
    if jump == "jmp":
        return "jmp"
    elif jump == "je":
        return "jne"
    elif jump == "jne":
        return "je"
    elif jump == "jbe":
        return "ja"
    elif jump == "jae":
        return "jb"
    elif jump == "jb":
        return "jae"
    elif jump == "ja":
        return "jbe"

#------------------------#
#functii pt loop_handling#
#------------------------#
def get_back_jumps(asm_lines):
    back_jumps=[]
    for line in asm_lines:
        #print(asm_lines.index(line),get_line_type(line))
        if get_line_type(line) == "control flow":
            jump_label=f"{get_line_tokens(line)[1]}:"
            if jump_label in asm_lines:
                label_index=asm_lines.index(jump_label)
                jump_index=asm_lines.index(line)
                if label_index < jump_index:
                    back_jumps.append(tuple([label_index,jump_index]))
    return back_jumps
def get_exit_condition(loop,asm_lines):
    for line_index in range(loop[0],loop[1]):
        line=asm_lines[line_index]
        if get_line_type(line) == "control flow":
            if asm_lines.index(f"{get_line_tokens(line)[1]}:")>loop[1]:
                return line_index
def get_code_blocks(loops,asm_lines): #functie aparent neutilizata
    start_index=asm_lines.index("main:")
    left_index=start_index
    right_index=loops[0][0]
    for loop in loops:
        print("hello")
    blocks=["hello"]
    return blocks
def partition_code_blocks2(loops,min_index=0,max_index=None): #functie care trebuie rescrisa
    if not loops:
        return [("iter", 0, max_index)] if max_index is not None else []

    # Sort loops by start index
    loops = sorted(loops, key=lambda x: x[0])

    blocks = []
    cursor = min_index

    for start, end in loops:
        # Add iterative block before loop
        if cursor < start:
            blocks.append(("iter", cursor, start - 1))

        # Add loop block
        blocks.append(("loop", start, end))

        cursor = end + 1

    # Add trailing iterative block if max_index is known
    if max_index is not None and cursor <= max_index:
        blocks.append(("iter", cursor, max_index))

    return blocks

def analyze_loop_structure(asm_lines): #functie care va fi folosita candva
    #functie care determina adancimea imbricarilor de foruri din pacate nu cred ca va mai exista suport pt foruri imbricate
    print("step 1.1")
    jumps=get_back_jumps(asm_lines)
    if len(jumps) >= 1:
        return 1
    return 0
def partition_code_blocks(asm_lines): #va fi rescrisa la un moment dat ca sa tina cont de foruri imbricate (Valentin)
    print("step 1.2.1")
    back_jumps=get_back_jumps(asm_lines)
    #back_jumps = loopuri (index_start,index-final)
    #print(back_jumps)
    #for jump in back_jumps:
        #analiza jumpurilor in exteriorul loopului
        #print(get_exit_condition(jump,asm_lines))
    code_blocks=partition_code_blocks2(back_jumps,asm_lines.index("main:"),len(asm_lines)-1)
    #print(code_blocks)

    labels={}
    idx=0
    for tuple in code_blocks:
        idx+=1
        #print(tuple)
        label_text=f"l{idx}"
        labels[label_text]=tuple

    labels["l_final"]=None
    return labels
def get_exit_conditions(asm_lines,code_blocks):
    #functie care returneaza conditiile de scoatere din for
    print("step 1.2.2")
    exit_conditions={}
    for block in code_blocks:
        if code_blocks[block] != None:
            if code_blocks[block][0] == "loop":
                exit_conditions[block]=[]
                block_lines=asm_lines[code_blocks[block][1]:code_blocks[block][2]+1]
                for line in block_lines:
                    if get_line_type(line) == "control flow":
                        if asm_lines.index(f"{get_line_tokens(line)[1]}:")>code_blocks[block][2]:
                            exit_conditions[block].append(asm_lines.index(line))
    print(exit_conditions)
    return exit_conditions
def define_flags(asm_lines,output,code_blocks):
    #functie care scrie flagurile necesare pt executarea secventiala a blocrilor de cod
    print("step 1.3")

    idx_main=asm_lines.index("main:")
    #print(idx_main)
    output.write(f".data\n")
    line_pointer=1
    while get_line_type(asm_lines[line_pointer]) != "section":
        output.write(f"{asm_lines[line_pointer]}\n")
        line_pointer+=1
        key_idx=0
    for key in code_blocks:
        if key_idx == 0:
            output.write(f"f{key[1:]}: .long 1\n")
        else:
            output.write(f"f{key[1:]}: .long 0\n")
        key_idx+=1
    while line_pointer != idx_main:
        output.write(f"{asm_lines[line_pointer]}\n")
        line_pointer+=1
    output.write(f"main:\n")
def define_flags(asm_lines,output,code_blocks):
    print("step 1.3")
    line_index=0
    while asm_lines[line_index] != ".text":
        output.write(f"{asm_lines[line_index]}\n")
        line_index+=1
    flags=[key for key in code_blocks]
    print(flags)
    flag_index=0
    for flag in flags:
        if flag_index == 0:
            output.write(f"f{flag[1:]}: .long 1\n")
        else:
            output.write(f"f{flag[1:]}: .long 0\n")
        flag_index+=1
    output.write(f".text\n")
    output.write(f".global main\n")
    output.write(f"main:\n")

    

def add_labels(asm_lines,output,code_blocks,loop_exits):
    #functie care adauga verificarile cu flaguri
    print("step 1.4")

    keys=list(code_blocks.keys())
    for i,block in enumerate(code_blocks):
        output.write(f"{block}:\n")
        if i+1 < len(keys):
            output.write(f"cmp $1,f{block[1:]}\n")
            output.write(f"jne {keys[i+1]}\n")
        if code_blocks[block] != None:
            block_lines=asm_lines[code_blocks[block][1]:code_blocks[block][2]+1]
            is_block_loop=code_blocks[block][0] == "loop"
            if is_block_loop:
                block_lines=asm_lines[code_blocks[block][1]:code_blocks[block][2]]
            #block lines retine toate liniile de cod ale blocului curent care se scrie
            #nu vrem etichete
            #in cazul in care avem loopuri nu vrem conditia
            #de semenea daca e loop mai trebuie sa rescriem conditia inainte de actualizarea flagurilor

            print(loop_exits)
            loop_condtion_line_idx=0
            if code_blocks[block][0] == "loop": 
                loop_condtion_line_idx=loop_exits[block][0]
            for line in block_lines:
                if get_line_type(line) != "label" :
                    if is_block_loop:
                        curr_line_idx=asm_lines.index(line)
                        if not(curr_line_idx == loop_condtion_line_idx or curr_line_idx == loop_condtion_line_idx-1):
                            output.write(f"{line}\n")
                    else:
                        output.write(f"{line}\n")
            if is_block_loop:
                output.write(f"{asm_lines[loop_exits[block][0]-1]}\n")
                output.write(f"{negate_conditional_jump(get_line_tokens(asm_lines[loop_exits[block][0]])[0])} {keys[i+1]}\n")
        if i+1 < len(keys):
            output.write(f"mov $0,f{keys[i][1:]}\n")
            if i+2< len(keys):
                output.write(f"mov $1,f{keys[i+1][1:]}\n")

#------------------------------#
#functii pt decisional_handling#
#------------------------------#

def run_pointers(asm_lines,idx):
    #imbunatatit functia asta
    p1=idx+1
    p2=asm_lines.index(f"{get_line_tokens(asm_lines[idx])[1]}:")
    false_lines=[]
    true_lines=[]
    while p1<p2:
        false_lines.append(p1)
        p1+=1
        if get_line_tokens(asm_lines[p1])[0] == 'jmp':
            p1=asm_lines.index(f"{get_line_tokens(asm_lines[p1])[1]}:")
        line=asm_lines[p1]
        if get_line_type(line) == "control flow" and get_line_tokens(line)[0] != "jmp":
            sub_if=run_pointers(asm_lines,p1)
            false_lines.append(sub_if)
            p1=sub_if[2]
    while p1>p2:
        true_lines.append(p2)
        p2+=1
        if get_line_tokens(asm_lines[p2])[0] == 'jmp':
            p2=asm_lines.index(f"{get_line_tokens(asm_lines[p2])[1]}:")
        line=asm_lines[p2]
        if get_line_type(line) == "control flow" and get_line_tokens(line)[0] != "jmp":
            sub_if=run_pointers(asm_lines,p2)
            true_lines.append(sub_if)
            p2=sub_if[2]
    if p1 == p2:
        return (true_lines,false_lines,p1,get_line_tokens(asm_lines[idx])[0][1:],(get_line_tokens(asm_lines[idx-1])[1],get_line_tokens(asm_lines[idx-1])[2]))

def get_decisional_branches(asm_lines):
    #important aceasta functie poate fi rulata doar dupa ce s-au eliminat forurile
    print("step 2.1")
    ifs=[]
    idx_main=asm_lines.index("main:")
    idx=idx_main
    while idx<len(asm_lines):
        line=asm_lines[idx]
        if get_line_type(line) == "control flow" and get_line_tokens(line)[0] != "jmp": #avem un jump conditionat
            #print(line,idx)
            current_if=run_pointers(asm_lines,idx)
            #print(current_if)
            ifs.append(current_if)
            idx=current_if[2]
        else:
            ifs.append(idx)
            idx+=1
    return ifs
    #aici trebuie sa implementam ideea de 2 pointers sa analizam branchurile
    #branchuri imbricate wip

def write_ifs_helper(asm_lines,output,if_list,depth):
    for i in range(len(if_list)):
        idx=if_list[i]
        if isinstance(idx,tuple):
            memory_copying(output,0,get_data(asm_lines=asm_lines,registers=True),depth)
            write_operand(output,'x',idx[4][0])
            write_operand(output,'y',idx[4][1])
            condition=idx[3]
            write_comparation(asm_lines,output,condition,depth)
            write_ifs_helper(asm_lines,output,idx[0],depth+1)
            memory_copying(output,1,get_data(asm_lines=asm_lines,registers=True),depth)
            memory_copying(output,2,get_data(asm_lines=asm_lines,registers=True),depth)
            write_ifs_helper(asm_lines,output,idx[1],depth+1)
            memory_copying(output,3,get_data(asm_lines=asm_lines,registers=True),depth)
            write_selector(output,depth)
            memory_copying(output,4,get_data(asm_lines=asm_lines,registers=True),depth)
            i=idx[2]
        else:
            output.write(f"{asm_lines[idx]}\n")
            i+=1
def write_ifs(asm_lines,output,if_list):
    print("step 2.4")
    write_ifs_helper(asm_lines,output,if_list,1)
def write_comparation(asm_lines,output,condition,depth):
    output.write(f"cmp_{condition} {depth}\n")
    memory_copying(output,2,["%eax","%ebx"],depth)
def write_operand(output,xory,operand):
    if "$" in operand:
        output.write(f"load_operand_{xory}_i {operand}\n")
    elif "%" in operand:
        output.write(f"load_operand_{xory}_r {operand}\n")
    else:
        output.write(f"load_operand_{xory}_v {operand}\n")
def write_selector(output,depth):
    output.write(f"prepare_selector {depth}\n")
def memory_copying(output,phase,data,depth): #functie auxiliara care se ocupa de a scrie loadurile si storeurile
    if phase == 0:
        for element in data:
            if element[0] == "%":
                output.write(f"storer {element},0,{depth}\n")
            else:
                output.write(f"storev {element},0,{depth}\n")

    if phase == 1:
        for element in data:
            if element[0] == "%":
                output.write(f"storer {element},4,{depth}\n")
            else:
                output.write(f"storev {element},4,{depth}\n")
    if phase == 2:
        for element in data:
            if element[0] == "%":
                output.write(f"loadr {element},0,{depth}\n")
            else:
                output.write(f"loadv {element},0,{depth}\n")
    if phase == 3:
        for element in data:
            if element[0] == "%":
                output.write(f"storer {element},0,{depth}\n")
            else:
                output.write(f"storev {element},0,{depth}\n")
    if phase == 4:
        for element in data:
            if element[0] == "%":
                output.write(f"updater {element},{depth}\n")
            else:
                output.write(f"updatev {element},{depth}\n")


def get_changed_data():
    print("step 2.2")

def define_if_variables(asm_lines,output,datas,depth):
    print("step 2.3")
    output.write(f".data\n")
    idx_main=asm_lines.index(".text")
    for i in range(1,idx_main):
        output.write(f"{asm_lines[i]}\n")

    output.write("\n")
    for i in range(1,depth+1):
        for data in datas:
            output.write(f"{data}_if{i}: .long 0,0\n")
        output.write("\n")
    for i in range(1,depth+1):
        output.write(f"selector_if{i}: .long 0\n")
    output.write("\n")

    output.write(f"\n")
    output.write(f"if_operand_x: .long 0\n")
    output.write(f"if_operand_y: .long 0\n")

    output.write("edi_saving: .long 0\n")
    output.write("ebp_saving: .long 0\n")
    output.write("eax_saving: .long 0\n")

    output.write(f".bss\n")
    output.write(f"eq: .skip 256\n")

    idx_text=asm_lines.index(".text")
    idx_main=asm_lines.index("main:")
    for i in range(idx_text,idx_main):
        output.write(f"{asm_lines[i]}\n")


def get_data(asm_lines,registers):
    prefix=""
    if registers:
        prefix="%"
    temporary_disabled=[f"{prefix}edi"]
    data=[f"{prefix}ecx",f"{prefix}edx",f"{prefix}esi",f"{prefix}esp",f"{prefix}ebp"]
    idx_data=asm_lines.index(".data")
    idx_text=asm_lines.index(".text")
    variables=[]
    special_registers=[f"{prefix}eax",f"{prefix}ebx"]
    for i in range(idx_data,idx_text+1):
        if get_line_type(asm_lines[i]) == "label":
            variables.append(get_line_tokens(asm_lines[i])[0][:-1])
    for variable in variables:
        data.append(variable)
    for special_register in special_registers:
        data.append(special_register)
    return data

#-------------------------------#
#functii pt operational_handling#
#-------------------------------#

#face Ecaterina
def define_lookup_tables(asm_lines,output):
    line_index=0
    while asm_lines[line_index] != ".bss":
        output.write(f"{asm_lines[line_index]}\n")
        line_index+=1

    line_index-=1
    output.write("inc_table: .long ")
    for i in range(0,256):
        output.write(f"{i},")
    while line_index < len(asm_lines):
        output.write(f"{asm_lines[line_index]}\n")
        line_index+=1

def parse_operations(asm_lines,output):
    for line in asm_lines:
        if line != "":
            if get_line_tokens(line)[0] == "int":
                flag="f3"
                output.write(f"syscall {flag}\n")
            else:
                output.write(f"{line}\n")
    
    write_system_calls(output)

def write_system_calls(output):
    print("step 3.4")
    output.write("\n")
    output.write(f"syscall_section:\n")
    output.write(f"int $0x80\n")
    output.write(f"jmp return_syscall\n")

def write_data_section(asm_lines,output,bss_index):
    # Write everything BEFORE .text (the .data section)
    for i in range(bss_index):
        output.write(f"{asm_lines[i]}\n")
    
    # Inject our necessary scratchpad variables
    output.write("\n# --- Operational Scratchpad ---\n")
    output.write("temp_eax: .long 0\n")
    output.write("temp_ebx: .long 0\n")
    output.write("temp_ecx: .long 0\n")
    output.write("temp_edx: .long 0\n")
    output.write("temp_eax_buf: .long 0\n")
    output.write("temp_src_buf: .long 0\n")
    output.write("temp_dest_buf: .long 0\n")
    output.write("temp_src_buf_2: .long 0\n")
    output.write("temp_dest_buf_2: .long 0\n")
    output.write("temp_res: .long 0\n")
    output.write("current_carry: .byte 0\n") 
    output.write("temp_c1: .byte 0\n")
    output.write("temp_c2: .byte 0\n")
    output.write("prod_low: .byte 0\n")
    output.write("prod_high: .byte 0\n")
    output.write("div_divisor: .long 0\n")
    output.write("div_quotient: .long 0\n")
    output.write("div_remainder: .long 0\n")
    output.write("div_temp_res: .long 0\n")
    output.write("div_mask: .long 0\n")
    output.write("div_inv_mask: .long 0\n")
    output.write("div_temp_a: .long 0\n")
    output.write("is_negative: .byte 0\n") 

def write_lut():
    print("nothing here yet")
def write_main(asm_lines,output,text_index):
    flag=None
    for i in range(text_index, len(asm_lines)):
        line=asm_lines[i]
        if line != "":
            if get_line_type(line) == "label":
                print (line)
                if line[0] == "l":
                    print (line[0])
                    if line[1].isdigit():
                        flag=line[1:-1]
            if get_line_tokens(line)[0] == "int" and flag != None:
                    output.write(f"syscall f{flag}\n")
            else:
                output.write(f"{line}\n")
    if flag != None:
        write_system_calls(output)


def generate_and_tables(output):
    output.write("\n# --- AND LOOKUP TABLES ---\n")
    # 1. Generate the AND_LUT (The 64KB logic grid)
    output.write(".align 4\n")
    output.write("AND_LUT:\n")
    for row in range(256):
        results = [str(row & col) for col in range(256)]
        output.write(f"    .byte {','.join(results)}\n")
    
    # 2. Generate the AND_PTR (Pointers to the rows for 1-step lookup)
    output.write("\n.align 4\n")
    output.write("AND_PTR:\n")
    for i in range(256):
        output.write(f"    .long AND_LUT + {i * 256}\n")
    output.write("# --- END OF AND TABLES ---\n\n")

def generate_or_tables(output):
    output.write("\n# --- OR LOOKUP TABLES ---\n")
    output.write(".align 4\n")
    output.write("OR_LUT:\n")
    for row in range(256):
        results = [str(row | col) for col in range(256)]
        output.write(f"    .byte {','.join(results)}\n")
    
    output.write("\n.align 4\n")
    output.write("OR_PTR:\n")
    for i in range(256):
        output.write(f"    .long OR_LUT + {i * 256}\n")
    output.write("# --- END OF OR TABLES ---\n\n")

def generate_xor_tables(output):
    output.write("\n# --- XOR LOOKUP TABLES ---\n")
    output.write(".align 4\n")
    output.write("XOR_LUT:\n")
    for row in range(256):
        # row ^ col calculeaza bitwise XOR in Python
        results = [str(row ^ col) for col in range(256)]
        output.write(f"    .byte {','.join(results)}\n")
    
    output.write("\n.align 4\n")
    output.write("XOR_PTR:\n")
    for i in range(256):
        output.write(f"    .long XOR_LUT + {i * 256}\n")
    output.write("# --- END OF XOR TABLES ---\n\n")

def generate_add_tables(output):
    output.write("\n# --- ADD LOOKUP TABLES ---\n")
    
    # 1. ADD_LUT: (a + b) % 256
    output.write(".align 4\nADD_LUT:\n")
    for row in range(256):
        results = [str((row + col) % 256) for col in range(256)]
        output.write(f"    .byte {','.join(results)}\n")
    
    output.write("\n.align 4\nADD_PTR:\n")
    for i in range(256):
        output.write(f"    .long ADD_LUT + {i * 256}\n")

    # 2. ADD_CARRY_LUT: (a + b) > 255 ? 1 : 0
    output.write("\n# --- ADD CARRY LOOKUP TABLES ---\n")
    output.write(".align 4\nADD_CARRY_LUT:\n")
    for row in range(256):
        # Dacă suma depășește 255, carry este 1, altfel 0
        carries = ["1" if (row + col) > 255 else "0" for col in range(256)]
        output.write(f"    .byte {','.join(carries)}\n")
    
    output.write("\n.align 4\nADD_CARRY_PTR:\n")
    for i in range(256):
        output.write(f"    .long ADD_CARRY_LUT + {i * 256}\n")
    output.write("# --- END OF ADD TABLES ---\n\n")

def generate_not_table(output):
    output.write("\n# --- NOT LOOKUP TABLE ---\n")
    output.write(".align 4\nNOT_LUT:\n")
    # Inversăm fiecare valoare: 255 - i (sau ~i & 0xFF)
    results = [str(255 - i) for i in range(256)]
    output.write(f"    .byte {','.join(results)}\n")

def generate_shl_tables(output):
    for pos in range(4):
        # Tabelul de valori (longs)
        output.write(f"\n.align 4\nSHL_B{pos}_LUT:\n")
        for val in range(256):
            res_list = []
            for shift in range(32):
                # Punem byte-ul la pozitia lui originala (0, 8, 16, 24 biți)
                # și apoi aplicăm shift-ul propriu-zis
                image = (val << (pos * 8)) << shift
                res_list.append(str(image & 0xFFFFFFFF))
            output.write(f"    .long {','.join(res_list)}\n")
        
        # Tabelul de pointeri către rânduri
        output.write(f"\n.align 4\nSHL_B{pos}_PTR:\n")
        for i in range(256):
            # Fiecare rând are 32 de long-uri (4 bytes fiecare) = 128 bytes
            output.write(f"    .long SHL_B{pos}_LUT + {i * 128}\n")

def generate_shr_tables(output):
    output.write("\n# --- SHR LOOKUP TABLES (4 POSITIONS) ---\n")
    for pos in range(4):
        output.write(f".align 4\nSHR_B{pos}_LUT:\n")
        for val in range(256):
            res_list = []
            for s in range(32):
                # Punem byte-ul la locul lui original (B0=0, B1=8, B2=16, B3=24)
                # Aplicăm shift right logic (>>)
                # Folosim masca 0xFFFFFFFF pentru a simula un registru de 32 biți
                shifted = (val << (pos * 8)) >> s
                res_list.append(str(shifted & 0xFFFFFFFF))
            output.write(f"    .long {','.join(res_list)}\n")
        
        output.write(f"\n.align 4\nSHR_B{pos}_PTR:\n")
        for i in range(256):
            output.write(f"    .long SHR_B{pos}_LUT + {i * 128}\n")
def generate_mul_tables(output):
    output.write("\n# --- MUL LOOKUP TABLES ---\n")
    
    # 1. Generăm rândurile pentru MUL_LOW
    for i in range(256):
        results = [str((i * j) % 256) for j in range(256)]
        output.write(f"MUL_L_ROW_{i}: .byte {','.join(results)}\n")
    
    # 2. Tabelul de pointeri pentru MUL_LOW
    output.write(".align 4\nMUL_LOW_PTR:\n")
    for i in range(256):
        output.write(f"    .long MUL_L_ROW_{i}\n")

    # 3. Generăm rândurile pentru MUL_HIGH
    for i in range(256):
        results = [str((i * j) // 256) for j in range(256)]
        output.write(f"MUL_H_ROW_{i}: .byte {','.join(results)}\n")
    
    # 4. Tabelul de pointeri pentru MUL_HIGH
    output.write(".align 4\nMUL_HIGH_PTR:\n")
    for i in range(256):
        output.write(f"    .long MUL_H_ROW_{i}\n")

def generate_div_support_tables(output):
    # 1. Tabel bit de semn
    output.write("IS_NEG_BYTE_LUT: .byte " + ",".join(["1" if i >= 128 else "0" for i in range(256)]) + "\n")
    
    # 2. Tabel masca (pozitiv -> toti bitii 1, negativ -> toti 0)
    # Atentie: Inversam indexul in functie de cum ai logica in JSON
    output.write(".align 4\nSIGN_TO_MASK_LUT: .long 0xFFFFFFFF, 0x00000000\n")

    # 3. Tabel MSB (pentru shift-ul combinat)
    output.write("GET_MSB_LUT: .byte " + ",".join(["1" if i >= 128 else "0" for i in range(256)]) + "\n")


#----------------------------------------------------#
#functiile corespunzatoare celor 3 etape de compilare#
#----------------------------------------------------#
def loop_handling(input,output):
    asm_lines=[line.strip() for line in input.readlines()] #extragerea liniilor din fisierul de la pasul anterior
    for_depth=analyze_loop_structure(asm_lines) #returneaza un tuplu cu informatii
    if for_depth>=1:
        code_blocks=partition_code_blocks(asm_lines) # dictionar cu loopuri(vezi idei proiect pt detalii)
        print(code_blocks) #print de debug
        loop_exits=get_exit_conditions(asm_lines,code_blocks)
        define_flags(asm_lines,output,code_blocks) # formatare sectiune .data cu fi-urile
        add_labels(asm_lines,output,code_blocks,loop_exits) # adauga labelurile + codul fara etichete
        output.write("jmp main\n") # scrie jumpul principal
    else:
        for line in asm_lines:
            output.write(f"{line}\n")
    #dupa aceasta etapa codul este inca x86 standard, dar totul ruleaza intr-o bucla mare in mod iterativ

def decisional_handling(input,output):
    asm_lines=[line.strip() for line in input.readlines()] #extragerea liniilor din fisierul de la pasul anterior
    ifs=get_decisional_branches(asm_lines) #crearea unui arbore care reprezinta ifurile
    print(ifs) #debug
    define_if_variables(asm_lines,output,get_data(asm_lines=asm_lines,registers=False),2) #scrierea in .data 
    write_ifs(asm_lines,output,ifs) #rescrierea mainului

    #dupa aceasta etapa codul contine doar jumpuri absolut necesare(cel final,apeluri de sistem,apeluri de functii), cu instructiuni scrise in isa intermediar

def operational_handling(input,output):
    asm_lines=[line.strip() for line in input.readlines()] #extragerea liniilor din fisierul de la pasul anterior

    needs_and_lut = False
    needs_or_lut = False 
    needs_xor_lut = False
    needs_add_lut = False
    needs_not_lut = False
    needs_shl_lut = False
    needs_shr_lut = False
    needs_mul_lut = False
    needs_div_lut = False

    for line in asm_lines:
        clean_line = line.lower().replace(",", " ")
        tokens = clean_line.split()
        if not tokens: continue
        
        instr = tokens[0]

        if instr in ["div", "divl", "idiv"]:
            needs_div_lut = True
            needs_add_lut = True
            needs_not_lut = True
            needs_and_lut = True
            needs_or_lut = True
        elif instr in ["shl", "shll", "sal", "sall"]:
            needs_shl_lut = True
            needs_add_lut = True
            needs_or_lut = True
        elif instr in ["shr", "shrl"]:
            needs_shr_lut = True
            needs_add_lut = True
            needs_or_lut = True
        elif instr in ["mul", "mull"]: # Detecție MUL
            needs_mul_lut = True
            needs_add_lut = True
            needs_or_lut = True
        elif instr == "and":
            needs_and_lut = True
        elif instr == "or":
            needs_or_lut = True
        elif instr in ["xor", "xorl"]:
            needs_xor_lut = True
        elif instr in ["add", "addl"]:
            needs_add_lut = True
            needs_or_lut = True 
        elif instr in ["sub", "subl"]:
            needs_add_lut = True 
            needs_or_lut = True  
            needs_not_lut = True 
        elif instr == "not":
            needs_not_lut = True

    text_index = -1
    for i, line in enumerate(asm_lines):
        if ".bss" in line:
            text_index = i
            print(f"DEBUG: Found .text at line {i}")
            break
    
    if text_index != -1:
        write_data_section(asm_lines,output,text_index)
        # Inject the heavy tables
        if needs_div_lut: 
            generate_div_support_tables(output)
        if needs_not_lut: 
            # Daca nu ai o functie separata, genereaz-o rapid aici:
            output.write("NOT_LUT: .byte " + ",".join([str(255-i) for i in range(256)]) + "\n")

        if needs_and_lut:
            print("DEBUG: Generating AND tables now...")
            generate_and_tables(output)
        else:
            print("DEBUG: AND tables NOT generated (flag was False)")

        if needs_or_lut: # Injectare tabela OR
            generate_or_tables(output)

        if needs_xor_lut:
            generate_xor_tables(output)

        if needs_add_lut:
            generate_add_tables(output)

        if needs_shl_lut:
            print("DEBUG: Generating 4-position SHL tables...")
            generate_shl_tables(output)

        if needs_shr_lut:
            print("DEBUG: Generating 4-position SHR tables...")
            generate_shr_tables(output)

        if needs_mul_lut: 
            generate_mul_tables(output)
        
        write_main(asm_lines,output,text_index)
    else:
        print("DEBUG: ERROR - Could not find .text section!")
        # Safety: If no .text, just dump the code
        for line in asm_lines:
            output.write(f"{line}\n")

    #dupa aceasta etapa codul are toate operatiile necesare pentru a fi translatat 1 la 1 linie cu linie in movuri

#--------------------#
#functia de compilare#
#--------------------#
def compile(input,output,step):
    if step == "compilation step 1":
        loop_handling(input,output)
    if step == "compilation step 2":
        decisional_handling(input,output)
    if step == "compilation step 3":
        operational_handling(input,output)
    
