import os, glob

width_title = ["0_80em","0_90em","1_00em","1_10em","1_20em","1_30em", "1_32em", "1_40em", "1_50em","1_60em","1_70em","1_80em"]



print("press the mode")
for i in range(len(width_title)):
    line_print = width_title[i] + " : " + str(i)
    print(line_print)
x = input()
x = int(x)

step_title = ["gen","premix" ,"HLT","AOD","MINIAOD","NANOAOD"]

print("press the mode")
for i in range(len(step_title)):
    line_print = step_title[i] + " : " + str(i)
    print(line_print)
y = input()
y = int(y)

line_print = "You choose the "+ width_title[x]
print(line_print)

dir_name = width_title[x]
#input_dir = f"/xrootd_user/seungjun/xrootd_new/nano/root/"+dir_name
input_dir = f"/cms/ldap_home/seungjun/nano/MC_b_bbar_4l/root/"+dir_name
#input_dir = f"/xrootd_user/seungjun/xrootd/nano/root/"+dir_name

file_list = os.listdir(input_dir)
#print(file_list)
file_count = len(file_list)

print(file_count)

command = "./submit_bbar_2018_"+step_title[y]+".py --nJob "+ str(file_count)

os.system(command)



width  = width_title[x]

os.chdir('/cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_'+step_title[y]+width +'/HTCondor_run/')
all_folder = glob.glob('mc*.sh')
all_file = [x for x in all_folder if os.path.isfile(x)]
all_file.sort()

for i,file_name in enumerate(all_file):
    command_line = "./" + file_name
    os.system(command_line)
    os.system("cp -r ../../dashgo.sh .")
