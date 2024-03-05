import os, glob

width_title = ["0_80em","0_90em","1_00em","1_10em","1_20em","1_30em", "1_32em", "1_40em", "1_50em","1_60em","1_70em","1_80em"]

print("press the mode")
for i in range(len(width_title)):
    line_print = width_title[i] + " : " + str(i)
    print(line_print)
x = input()
x = int(x)

step_title = ["gen","premix" ,"HLT","AOD","MINIAOD","NANOAOD"]
step_title_root = ["GEN_SIM","PREMIX" ,"HLT","AOD","MINIAOD","NANOAOD"]
step_title_root2 = ["GEN-SIM","PREMIX" ,"HLT","AOD","MINIAOD","NANOAOD"]



dir_name = width_title[x]
for i in range(3):
    input_dir = f"/xrootd_user/seungjun/xrootd_new/nano/"+step_title_root[i+1]+"/"+dir_name
	size_i = "1k"
    if i == 0: size_i = "9216M" #PREMIX
    if i == 1: size_i = "8294M" #HLT
    if i == 2: size_i = "2048M" #AOD
    command = "find "+input_dir+"/* -size -"+size_i+" -exec rm -rf {} \; &"
    os.system(command)


