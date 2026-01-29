def preprocess(input, output):
    line=0 #nr liniei, debugging purposes
    currlab="" #etichete...
    for l in input.readlines():
        
        if(len(l.strip())==0):
            output.write("\n")
            mmn=""
            continue
        line+=1
        if(len(l.strip().split())):
            mmn=l.strip().split()[0] #first keyword of line, supposed mnemonic
        
        #print(len(mmn),line)

        if(mmn[len(mmn)-1]==':' and len(mmn)==len(l.strip())): #check if label
            output.write(l)
            currlab=mmn[0:len(mmn)-1]

        elif(mmn=="loop"): #LOOP INSTR CHECK
            output.write("\tdec %ecx\n")
            output.write("\tcmp $0, %ecx\n")
            output.write("\tjne " + currlab + "\n")

        #temp_eax, ebx, ecx, edx... din movfuscat 
        elif(mmn=="test"): #CHECK TEST INSTR
            tmp=l.strip().split(" ",1)
            
            #print(tmp,line)
            mmn=tmp[0]
            ops=tmp[1].split(",")
            op1,op2=ops[0].strip(),ops[1].strip()
            #print(ops,op1,op2, line)

            #etapa de copy op1, use eax ca registru copie
            output.write("\tmov %eax, temp_eax" + "\n")
            output.write(f"\tmov {op1}, %eax" + "\n")
            
            #operatia efectiva
            output.write("\tand " + op1 + ", " + op2 + "\n") # and op1, op2 => op1=op1&op2

            #etapa de restore
            output.write(f"\tmov %eax, {op1}" + "\n") #restore op1
            output.write("\tmov temp_eax, %eax" + "\n") #restore eax

        else: #other instr
            output.write(l)


#DEBUG PURPOSES
#f=open("test.s","r")
#g=open("prep.s","w")
#preprocess(f,g)
#f.close()
#g.close()
