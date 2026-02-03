import compiler
import translator
import sys
import tempfile
import shutil
import os

arguments=sys.argv[1:]

if(len(arguments) == 0):
    print("Eroare: nu s-a gasit fisierul")
else:
    input_file=arguments[0]
    output_file=arguments[1]
    flag_keep=False
    if len(arguments)>2:
        flag_keep=arguments[2] == "-i"

    # transformare 0 -> 1
    step0 = open(input_file, "r")
    step1 = tempfile.TemporaryFile(mode="w+")
    preprocessor.preprocess(step0, step1)
    step0.close()
    step1.seek(0)
    
    # transformare 1 -> 2
    step1 = open(input_file, "r")
    step2 = tempfile.TemporaryFile(mode="w+")
    compiler.compile(step1, step2, "compilation step 1")
    step1.close()
    step2.seek(0)

    # transformare 2 -> 3
    step3 = tempfile.TemporaryFile(mode="w+")
    compiler.compile(step2, step3, "compilation step 2")
    step2.close()
    step3.seek(0)

    # transformare 3 -> 4
    step4 = tempfile.TemporaryFile(mode="w+")
    compiler.compile(step3, step4, "compilation step 3")
    step3.close()
    step4.seek(0)

    #in cazul citirii '-i' se pstreaza fisierul cu isa intermediar
    if flag_keep:
        with open("isa_intermediar.txt", "w") as saved:
            shutil.copyfileobj(step4, saved)
        step4.seek(0)


    # transformare 4 -> 5
    step5 = open(output_file, "w")
    translator.translate(step4, step5, "translation step 1")
    step4.close()
    step5.close()

