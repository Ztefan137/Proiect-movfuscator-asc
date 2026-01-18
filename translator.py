import json

#-----------------------------#
#functii de utilitate generala#
#-----------------------------#
def get_line_tokens(line): #functie de utilitate generala
    line=line.replace(","," ")
    line=line.split()
    return line
def get_line_type(line): #functie de utilitate generala
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
def get_instruction_json_index(line,instructions):
    try:
        instruction_names=[instruction["name"] for instruction in instructions]
        index=instruction_names.index(get_line_tokens(line)[0])
        return index
    except:
        return -1

#------------------------------#
#functii pt convertion_handling#
#------------------------------#

def adapt_template(template,effective_param):
    new_template=[]
    for line in template:
        new_line=line
        for param_name,param_value in effective_param.items():
            new_line=new_line.replace(f"<{param_name}>",param_value)
        new_template.append(new_line)
    return new_template

def lower_half_register(register):
    return f"%al"

def convert(asm_lines,output,format):
    print("step 4.1")
    instructions=format["instructions"]
    for line in asm_lines:
        instruction_idx=get_instruction_json_index(line,instructions)
        if instruction_idx != -1:
            instruction=instructions[instruction_idx]
            params=get_line_tokens(line)[1:]
            #print(params)
            param_dict={}
            for i in range(len(instructions[instruction_idx]["param"])):
                param_dict[instructions[instruction_idx]["param"][i]]=params[i]
            try:
                for i in range(len(instruction["except"])):    
                    exception=instruction["except"][i]
                    new_parameter=exception[0]
                    rule=exception[1]
                    #print(new_parameter,rule)
                    if rule[0] == 'l':
                        param_dict[new_parameter]=param_dict[rule.split("/")[1]][1:]
            except:
                print("",end="")
            #print(param_dict)
            for print_line in adapt_template(instruction["template"],param_dict):
                output.write(f"{print_line}\n")
        else:
            output.write(f"{line}\n")
#---------------------------------------------#
#functia corespunzatoare etapei de translatare#
#---------------------------------------------#
def convertion_handling(input,output):
    with open("translation_information.json") as f:
        format=json.load(f)
    asm_lines=[line.strip() for line in input.readlines()] #extragerea liniilor din fisierul de la pasul anterior
    convert(asm_lines,output,format)

def translate(input,output,step):
    if step == "translation step 1":
        convertion_handling(input,output)
