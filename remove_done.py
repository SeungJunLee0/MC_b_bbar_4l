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



print("press the mode")
for i in range(len(step_title)):
    line_print = step_title[i] + " : " + str(i)
    print(line_print)
y = input()
y = int(y)

line_print = "You choose the "+ width_title[x]
print(line_print)

dir_name = width_title[x]
input_dir = f"/xrootd_user/seungjun/xrootd/nano/"+step_title_root[y]+"/"+dir_name

file_list = os.listdir(input_dir)
for i in range(len(file_list)):
    title_name = step_title_root2[y]+"_"
    file_list[i]=file_list[i].strip(title_name)
    file_list[i]=file_list[i].strip(".root")
file_list.sort()
for i in range(10):
    print(file_list[i])
file_count = len(file_list)

print(file_count)


for i in range(len(file_list)):
    job_id =int(file_list[i])
    #print(job_id, "  ", i)
    job_name = "0000"
    if job_id < 10:                        job_name ="000"+str(job_id)
    if job_id >= 10 and job_id < 100:       job_name ="00"+str(job_id)
    if job_id >= 100 and job_id < 1000:     job_name ="0"+str(job_id)
    if job_id >= 1000 and job_id < 10000:     job_name =str(job_id)
    #print(job_name, "  " ,job_id)
    
    command = 'rm -rf /cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_'+step_title[y]+width_title[x] +'/HTCondor_run/mc_generation_jobs_'  +job_name     +".submit"
    os.system(command)
    command = 'rm -rf /cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_'+step_title[y]+width_title[x] +'/HTCondor_run/mc_generation_job_'   +file_list[i] +".sh"
    os.system(command)
    command = 'rm -rf /cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_'+step_title[y]+width_title[x] +'/HTCondor_run/MC_Generation_Script_'+file_list[i] +".sh"
    os.system(command)





line_print = "Now we are checking the previous files "+ width_title[x]
print(line_print)

dir_name = width_title[x]


input_dir = f"/xrootd_user/seungjun/xrootd/nano/root/"+dir_name

file_list_root = os.listdir(input_dir)
for i in range(len(file_list_root)):
    title_name = "lhe_"
    file_list_root[i]=file_list_root[i].strip(title_name)
    file_list_root[i]=file_list_root[i].strip(".root")
file_list_root.sort()



input_dir = f"/xrootd_user/seungjun/xrootd/nano/"+step_title_root[y-1]+"/"+dir_name

file_list_all = os.listdir(input_dir)
for i in range(len(file_list_all)):
    title_name = step_title_root2[y-1]+"_"
    file_list_all[i]=file_list_all[i].strip(title_name)
    file_list_all[i]=file_list_all[i].strip(".root")
file_list_all.sort()


file_list_all = list(map(int, file_list_all))
file_list_root = list(map(int, file_list_root))
file_list = list(map(int, file_list))
result = list(set(file_list_all) - set(file_list))
result = list(set(file_list_root) - set(result))
result = list(map(str,result))

for i in range(len(result)):
    job_id =int(result[i])
    #print(job_id, "  ", i)
    job_name = "0000"
    if job_id < 10:                        job_name ="000"+str(job_id)
    if job_id >= 10 and job_id < 100:       job_name ="00"+str(job_id)
    if job_id >= 100 and job_id < 1000:     job_name ="0"+str(job_id)
    if job_id >= 1000 and job_id < 10000:     job_name =str(job_id)
    #print(job_name, "  " ,job_id)
    
    command = 'rm -rf /cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_'+step_title[y]+width_title[x] +'/HTCondor_run/mc_generation_jobs_'  +job_name     +".submit"
    os.system(command)
    command = 'rm -rf /cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_'+step_title[y]+width_title[x] +'/HTCondor_run/mc_generation_job_'   +result[i] +".sh"
    os.system(command)
    command = 'rm -rf /cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_'+step_title[y]+width_title[x] +'/HTCondor_run/MC_Generation_Script_'+result[i] +".sh"
    os.system(command)

