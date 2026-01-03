
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
    #functie care scrie flagurile necesare pt executarea secventiala a blocrilor de cod
    print("step 1.3")

    idx_main=asm_lines.index("main:")
    print(idx_main)
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
    #identificarea variabilelor schimbate in bloculuri decizionale
    #define if storage data
    #adaugarea arhitecturii de load store
    #

def operational_handling(input,output):
    asm_lines=[line.strip() for line in input.readlines()] #extragerea liniilor din fisierul de la pasul anterior

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
    
