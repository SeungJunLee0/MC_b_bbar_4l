import os, glob
#haha

width_title = ["0_80em","0_90em","1_00em","1_10em","1_20em","1_30em", "1_32em", "1_40em", "1_50em","1_60em","1_70em","1_80em"]



print("press the mode")
for i in range(len(width_title)):
    line_print = width_title[i] + " : " + str(i)
    print(line_print)
x = input()
x = int(x)

line_print = "You choose the "+ width_title[x]
print(line_print)

dir_name = width_title[x]
input_dir = f"/u/user/seungjun/SE_UserHome/root/"+dir_name

file_list = os.listdir(input_dir)
file_count = len(file_list)

print(file_count)

command = "./submit_bbar_2018.py --nJob "+ str(file_count)

os.system(command)



width  = width_title[x]

os.chdir('/u/user/seungjun/scratch/b_bbar/run'+width +'/HTCondor_run/')
all_folder = glob.glob('mc*.sh')
all_file = [x for x in all_folder if os.path.isfile(x)]
all_file.sort()

for i,file_name in enumerate(all_file):
    command_line = "./" + file_name
    #print(command_line)
    os.system(command_line)
