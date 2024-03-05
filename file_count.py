import os


width_title = ["0_80em","0_90em","1_00em","1_10em","1_20em","1_30em", "1_32em", "1_40em", "1_50em","1_60em","1_70em","1_80em"]

file_type = ["lhe","root","GEN_SIM","PREMIX","HLT","AOD","MINIAOD","NANOAOD"]
#for i in range(len(file_type)):


print("Choose the width")
for i in range(len(width_title)):
    line_print = width_title[i] + " : " + str(i)
    print(line_print)
x = input()
x = int(x)

for y in range(7):
    folder_path = f"/xrootd_user/seungjun/xrootd_new/nano/"+file_type[y]+"/"+width_title[x]
    file_list = os.listdir(folder_path)
    print(file_type[y],"  " ,len(file_list))
    if len(file_list) > 3:
        size_one = folder_path+"/"+file_list[2]
        file_size = os.path.getsize(size_one)
        print('File Size:', "{0:.2f}".format(file_size/1024./1024./1024.), 'GB')
        size_one = folder_path+"/"+file_list[3]
        file_size = os.path.getsize(size_one)
        print('File Size:', "{0:.2f}".format(file_size/1024./1024./1024.), 'GB')
        size_one = folder_path+"/"+file_list[1]
        file_size = os.path.getsize(size_one)
        print('File Size:', "{0:.2f}".format(file_size/1024./1024./1024.), 'GB')
    #file_count = len(file_list)
    #print(file_type[i],"files :",file_count)

#file_size = os.path.getsize()
#print('File Size:', file_size, 'bytes')
	
