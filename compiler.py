
#cand citesti prima oara acest cod citeste l de la final la inceput (are mai mult sens asa)

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
def identify_syscalls(asm_lines):
    global syscalls
    for idx in range(len(asm_lines)):
        line=asm_lines[idx]
        if get_line_type(line) == "syscall" :
            syscalls[idx+1]="syscall"

def get_mov_instructions(line):
    #functia care se ocupa de inlocuiri de tip macro + ifuri si foruri cu helpere
    #helper if->write_if
    #helper for->write_for
    #important pt if si for trebuie realizata analiza sintactica in prealabil
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
#h=open("C:/Users/stefa/OneDrive/Desktop/proiecte/python/proiect_asc/cod.txt",'w')
g=open("C:/Users/stefa/OneDrive/Desktop/proiecte/python/proiect_asc/cod2.txt",'w')
line_classification={}
asm_lines=[line.strip() for line in f.readlines()]

#program flags
loop_existance=False
if_existance=True
syscalls={}

    
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
#identify_syscalls()
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
#etapa de formatare a ifurilor
#etapa de formatare a operatiilor aritmetice/logice


#functii pt loop_handling
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
def get_code_blocks(loops,asm_lines):
    start_index=asm_lines.index("main:")
    left_index=start_index
    right_index=loops[0][0]
    for loop in loops:
        print("hello")
    blocks=["hello"]
    return blocks
def partition_code_blocks2(loops,min_index=0,max_index=None):
    """
    Given a list of (start, end) loop ranges, return a list of code blocks.
    A block is either:
        ("loop", start, end)
        ("iter", start, end)
    If max_index is provided, the function will include trailing iterative code.
    """
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


def partition_code_blocks(file):
    print("step 1.2")
    #aceasta functie va fi realizata prin apeluri utile ale functiilor anterioare
    #daca citi aceste 2 comentarii inseamna ca mi am bagat picioarele ))

    '''
    asm_lines=[line.strip() for line in input.readlines()]
    back_jumps=get_back_jumps(asm_lines)
    #back_jumps = loopuri (index_start,index-final)
    print(back_jumps)
    for jump in back_jumps:
        #analiza jumpurilor in exteriorul loopului
        print(get_exit_condition(jump,asm_lines))
    code_blocks=partition_code_blocks2(back_jumps,asm_lines.index("main:"),len(asm_lines)-1)
    print(code_blocks)
    for block_index in range(len(code_blocks)):
        output.write(f"l{block_index+1}:\n")
        output.write(f"cmp f{block_index+1},$1\njne l{block_index+2}\n")
        block=code_blocks[block_index]
        for i in range(block[1],block[2]+1):
            output.write(f"{asm_lines[i]}\n")
        output.write(f"mov $0,f{block_index+1}\n")
        output.write(f"mov $1,f{block_index+2}\n")
    output.write(f"l4:\njmp main")
    '''

def analyze_loop_structure():
    print("step 1.1")

def define_flags():
    print("step 1.3")

def add_labels():
    print("step 1.4")

#a se ignora momentan ce e mai sus; functiile alea trebuie rescrise dar functionalitatea lor minimala conteaza momentan
#vreau sa fac un sistem cat mai modular incat sa schimbam zilele urmatoare doar functiile de mai sus fara sa ne atingem de cadrul de apel din cele 3 functii corespunzatoare celor 3 etape


def loop_handling(input,output):
    for_depth=analyze_loop_structure(input)
    code_blocks=partition_code_blocks(input) # dictionar cu loopuri(vezi idei proiect pt detalii)
    define_flags(input,output,code_blocks) # formatare sectiune .data cu fi-urile
    add_labels(output,output,code_blocks) # adauga labelurile
    output.write("jmp main\n") # scrie jumpul principal

def decisional_handling(input,output):
    print("")

def operational_handling(input,output):
    print("")

def compile(input,output):
    loop_handling(input,output)
    decisional_handling(output,output)
    operational_handling(output,output)
