
#cand citesti prima oara acest cod citeste-l de la final la inceput (are mai mult sens asa)


#-----------------------------#
#functii de utilitate generala#
#-----------------------------#
def get_line_tokens(line): #functie de utilitate generala
    line=line.replace(","," ")
    line=line.split()
    return line
def get_line_type(line): #fucntie de utilitate generala
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

def analyze_loop_structure(input): #functie care va fi folosita candva
    #functie care determina adancimea imbricarilor de foruri
    print("step 1.1")
    return 1
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
                            
    return exit_conditions
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
            loop_condtion_line_idx=0
            if code_blocks[block][0] == "loop": 
                loop_condtion_line_idx=loop_exits[block][0]
            for line in block_lines:
                if get_line_type(line) != "label":
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

def get_decisional_branches():
    print("step 2.1")
    #aici trebuie sa implementam ideea de 2 pointers sa analizam branchurile
    #branchuri imbricate wip

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
            output.write(f"{data}_if{i}: 0,0\n")
        output.write("\n")
    for i in range(1,depth+1):
        output.write(f"selector_if{i}: 0\n")
    output.write("\n")

    for i in range(idx_main,len(asm_lines)):
        output.write(f"{asm_lines[i]}\n")

def get_data():
    data=[f"eax",f"ebx",f"ecx",f"edx",f"edi",f"esi",f"esp",f"ebp"]
    variables=["n"]
    for variable in variables:
        data.append(variable)
    return data

#tot ce se va mai inlocui vor fi functiile de mai sus
#ce e sub comentariul asta ramane in mare parte batut in cuie

#----------------------------------------------------#
#functiile corespunzatoare celor 3 etape de compilare#
#----------------------------------------------------#
def loop_handling(input,output):
    asm_lines=[line.strip() for line in input.readlines()] #extragerea liniilor din fisierul de la pasul anterior
    for_depth=analyze_loop_structure(asm_lines) #returneaza un tuplu cu informatii
    code_blocks=partition_code_blocks(asm_lines) # dictionar cu loopuri(vezi idei proiect pt detalii)
    loop_exits=get_exit_conditions(asm_lines,code_blocks)
    define_flags(asm_lines,output,code_blocks) # formatare sectiune .data cu fi-urile
    add_labels(asm_lines,output,code_blocks,loop_exits) # adauga labelurile + codul fara etichete
    output.write("jmp main\n") # scrie jumpul principal
    #in acest moment ar trebui sa avem cod care ruleaza in x86 in mod iterativ

def decisional_handling(input,output):
    asm_lines=[line.strip() for line in input.readlines()] #extragerea liniilor din fisierul de la pasul anterior
    #identificare de structuri decizionale(branchuri conditii cmp-uri test-uri etc.)
    #decisional_structures=get_decisional_branches(asm_lines)
    #identificarea variabilelor schimbate in blocurile decizionale
    #changed_data=get_changed_data(asm_lines,decisional_structures)
    #define if storage data
    #define_if_variables()
    
    define_if_variables(asm_lines,output,get_data(),2)

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

def operational_handling(input, output):
    # Read all lines
    raw_lines = input.readlines()
    asm_lines = [line.strip() for line in raw_lines]
    
    print(f"DEBUG: Processing {len(asm_lines)} lines...")

    needs_and_lut = False
    needs_or_lut = False 
    needs_xor_lut = False
    needs_add_lut = False
    needs_not_lut = False
    needs_shl_lut = False
    needs_shr_lut = False

    for line in asm_lines:
        clean_line = line.lower().replace(",", " ")
        tokens = clean_line.split()
        if not tokens: continue
        
        instr = tokens[0]

        if instr in ["shl", "shll", "sal", "sall"]:
            needs_shl_lut = True
            needs_add_lut = True # SHL combină rezultatele prin ADD
            needs_or_lut = True  # ADD are nevoie de OR
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
            print("DEBUG: Found SUB! Setting flags...")
            needs_add_lut = True 
            needs_or_lut = True  
            needs_not_lut = True 
        elif instr == "not":
            needs_not_lut = True
        elif instr in ["shr", "shrl"]:
            needs_shr_lut = True
            needs_add_lut = True
            needs_or_lut = True

    # 2. Find .text section
    text_index = -1
    for i, line in enumerate(asm_lines):
        if ".text" in line:
            text_index = i
            print(f"DEBUG: Found .text at line {i}")
            break
    
    # 3. Handle Writing
    if text_index != -1:
        # Write everything BEFORE .text (the .data section)
        for i in range(text_index):
            output.write(f"{asm_lines[i]}\n")
        
        # Inject our necessary scratchpad variables
        output.write("\n# --- Operational Scratchpad ---\n")
        output.write("temp_eax: .long 0\n")
        output.write("temp_ebx: .long 0\n")
        output.write("temp_ecx: .long 0\n")
        output.write("temp_edx: .long 0\n")
        output.write("temp_src_buf: .long 0\n")
        output.write("temp_dest_buf: .long 0\n")
        output.write("temp_res: .long 0\n")
        output.write("current_carry: .byte 0\n") 
        output.write("temp_c1: .byte 0\n")
        output.write("temp_c2: .byte 0\n")

        # Inject the heavy tables
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
        
        # Write the .text section and all instructions
        for i in range(text_index, len(asm_lines)):
            output.write(f"{asm_lines[i]}\n")
    else:
        print("DEBUG: ERROR - Could not find .text section!")
        # Safety: If no .text, just dump the code
        for line in asm_lines:
            output.write(f"{line}\n")

#--------------------#
#functia de compilare#
#--------------------#
def compile(input,output,step):
    global key_idx
    key_idx = 0
    if step == "compilation step 1":
        loop_handling(input,output)
    if step == "compilation step 2":
        decisional_handling(input,output)
    if step == "compilation step 3":
        operational_handling(input,output)
    
