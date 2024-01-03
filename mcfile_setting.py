import os, glob

width_title = ["0_80em","0_90em","1_00em","1_10em","1_20em","1_30em", "1_32em", "1_40em", "1_50em","1_60em","1_70em","1_80em"]
#                 0        1        2         3       4       5         6        7         8          9        10        11
width_dir = [   "0_80"  , "0_90",  "1_00",  "1_10",  "1_20"  ,"1_30",  "1_32",   "1_40"  , "1_50",   "1_60",  "1_70", "1_80"]

num = 0

width  = width_title[num]
widthdir = width_dir[num]

print(width)
print(width)
print(width)



os.chdir('/u/user/seungjun/scratch/b_bbar/run'+width +'/HTCondor_run/')
all_folder = glob.glob('mc*.sh')
all_file = [x for x in all_folder if os.path.isfile(x)]
all_file.sort()

for i,file_name in enumerate(all_file):
    command_line = "./" + file_name
    #print(command_line)
    os.system(command_line)
