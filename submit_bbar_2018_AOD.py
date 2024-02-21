#!/usr/bin/env python3

import os
import sys
import time
import glob
import json
import random
from argparse import ArgumentParser

width_title = ["0_80em","0_90em","1_00em","1_10em","1_20em","1_30em", "1_32em", "1_40em", "1_50em","1_60em","1_70em","1_80em"]
#                 0        1        2         3       4       5         6        7         8          9        10        11
width_dir = [   "0_80"  , "0_90",  "1_00",  "1_10",  "1_20"  ,"1_30",  "1_32",   "1_40"  , "1_50",   "1_60",  "1_70", "1_80"]
#width_value = 0
#dir_name = width_title[width_value]

print("press the mode")
for i in range(len(width_title)):
    line_print = width_title[i] + " : " + str(i)
    print(line_print)

x = input()
x = int(x)
line_print = "You choose the "+ width_title[x]
print(line_print)
width = width_title[x]
dir_name = width_title[x]


voms_dir = f"/cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_AOD"+dir_name
work_dir = f"/cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run_AOD"+dir_name
#work_dir = f"/u/user/seungjun/scratch/b_bbar/run"+dir_name
run_dir = f"{work_dir}/HTCondor_run"
#input_dir = f"/u/user/seungjun/scratch/b_bbar"
#input_dir = f"root://cms-xrdr.private.lo:2094//xrd/store/user/seungjun/nano/HLT/"+dir_name
input_dir = f"root://cms-xrdr.private.lo:3094//xrd/store/user/seungjun/nano/HLT/"+dir_name
output_dir = f"root://cms-xrdr.private.lo:3094//xrd/store/user/seungjun/nano/AOD/"+dir_name
#output_dir = f"root://cms-xrdr.private.lo:2094//xrd/store/user/seungjun/nano/AOD/"+dir_name




####################################################################################
def get_fragment():
####################################################################################
    
    fragment=''
    fragment+=f'''import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
 
                         #bbbar_4l settings
                         emissionVeto1 = cms.untracked.PSet(),
                         EV1_vetoOn = cms.bool(True),
                         EV1_maxVetoCount = cms.int32(100),
                         EV1_pThardMode = cms.int32(0),
                         EV1_pTempMode = cms.int32(0),
                         EV1_emittedMode = cms.int32(0),
                         EV1_pTdefMode = cms.int32(1),
                         EV1_MPIvetoOn = cms.bool(True),
                         EV1_nFinalMode = cms.int32(2),
                         EV1_nFinal = cms.int32(999), 
                         #New Line
 
                         PythiaParameters = cms.PSet(
                              pythia8CommonSettingsBlock,
                              pythia8CP5SettingsBlock,
                              pythia8PSweightsSettingsBlock,
                              pythia8BBBar4lSettings = cms.vstring(
                                          'SpaceShower:pTmaxMatch = 2', # 1 without main31; 2 for main31
                                          'TimeShower:pTmaxMatch  = 2', # 1 without main31; 2 for main31
                                          'MultipartonInteractions:pTmaxMatch = 2',
                                          'POWHEGres:calcScales = off',   # obsolete routine, don't use
                                          'POWHEG:bb4l = on', # should be on
                                          'POWHEG:bb4l:FSREmission:veto = true', # default veto implemented using doVetoFSREmission hook
                                          'POWHEG:bb4l:FSREmission:onlyDistance1 = false', # whether to veto only the first emission, or all of them. Due to shower evolution scale mismatch, all should be vetoed. The pheno impact seems negligible. Only applies to FSREmission veto
                                          'POWHEG:bb4l:FSREmission:dryRun = false',   # debug switch, don't modify
                                          'POWHEG:bb4l:FSREmission:vetoAtPL = false', # for debugging only, don't modify
                                          'POWHEG:bb4l:FSREmission:vetoQED = false',  # whether to veto QED emissions. QED emissions should not be vetoed in b_bbar_4l
                                          'POWHEG:bb4l:PartonLevel:veto = false',     # alternative veto implemented using doVetoPartonLevel hook. Should yield results equivalent to the FSREmission veto but it is much slower. This is because vetoing individual emissions, the event is completely reshowered if at the first emission should be vetoed. Note that this veto requires features not available in the public version of Pythia (as of version 8.230)
                                          'POWHEG:bb4l:PartonLevel:excludeFSRConflicting = false', # debug switch, don't modify
                                          'POWHEG:bb4l:DEBUG = false',  # debug switch, don't modify
                                          'POWHEG:bb4l:ScaleResonance:veto = false', # alternative veto implemented using ScaleResonance hook. Suffers from scale definition mismatch.
                                          'POWHEG:bb4l:FSREmission:vetoDipoleFrame = false', # whether or not to calculate veto pt in the dipole frame instead of the resonance frame
                                          'POWHEG:bb4l:FSREmission:pTpythiaVeto = false', # whether or not to use Pythia's definition of pt
                                          'POWHEG:bb4l:pTminVeto = 0.8', # hardness in the case of no radiation from the top decay. This should effectively align with Pythia's IR cutoff
                                          ),                

                              processParameters = cms.vstring(
                                          #'POWHEG:nFinal = 2', ## Number of final state particles
                                          ## (BEFORE THE DECAYS) in the LHE
                                          ## other than emitted extra parton
                                          'TimeShower:mMaxGamma = 1.0',#cutting off lepton-pair production
                                          ##in the electromagnetic shower
                                          ##to not overlap with ttZ/gamma* samples
                                          '6:m0 = 172.5',    # top mass'
                                          ),
                              parameterSets = cms.vstring('pythia8CommonSettings',
                                          'pythia8CP5Settings',
                                          'pythia8BBBar4lSettings',
                                          'pythia8PSweightsSettings',
                                          'processParameters'
                                          )

                              )
                        )
ProductionFilterSequence = cms.Sequence(generator)'''

    return fragment

####################################################################################
def get_shell_script(dataset_name, nEvents, fragment_path, job_id, dir_name):
####################################################################################
    
    script=''
    script+=f'''#!/bin/bash

#source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh

# Dump all code into 'MC_Generation_Script_{job_id}.sh'
cat <<'EndOfMCGenerationFile' > MC_Generation_Script_{job_id}.sh
#!/bin/bash

### Job configuration ###
echo "Processing job number {job_id} ... "
export X509_USER_PROXY={work_dir}/x509up
CWD=`pwd -P`
cd $_CONDOR_SCRATCH_DIR
mkdir -p {dir_name}/job_{job_id}

cd {dir_name}/job_{job_id}

### Premix step ###

#export CMS_PATH=/cms/ldap_home/seungjun
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_27/src ] ; then
  echo release CMSSW_10_6_27 already exists
else
  scram p CMSSW CMSSW_10_6_27
fi
cd CMSSW_10_6_27/src
eval `scram runtime -sh`
scram b
cmsenv



[ ! -d Configuration/GenProduction/python ] && mkdir -p Configuration/GenProduction/python
cp {fragment_path} Configuration/GenProduction/python/PY8_fragment.py
scram b
cd ../..


mkdir .dasmaps/
cp -r /cms/ldap_home/seungjun/.dasmaps/das_maps_dbs_prod.js .dasmaps/

dasgoclient -query="file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX"

  
  
### AOD step ###
cd CMSSW_10_6_27/src
eval `scram runtime -sh`
cd ../..

cmsDriver.py --python_filename AOD_cfg.py \\
             --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM \\
             --filein file:{input_dir}/HLT_{job_id}.root --fileout file:AOD_{job_id}.root \\
             --conditions 106X_upgrade2018_realistic_v11_L1v1 \\
             --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --era Run2_2018 --runUnscheduled --no_exec --mc -n {nEvents} || exit $? ;
cmsRun AOD_cfg.py || exit $? ;
xrdcp AOD_{job_id}.root {output_dir}/
python3 /cms/ldap_home/seungjun/tmp/catbot.py AOD_{job_id}.root
#  
#  
#  
#  ### MINIAOD step ####
#  cmsDriver.py --python_filename MINIAOD_cfg.py \\
#               --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM \\
#               --filein file:AOD.root --fileout file:MINIAOD.root \\
#               --conditions 106X_upgrade2018_realistic_v16_L1v1 \\
#               --step PAT --geometry DB:Extended --procModifiers run2_miniAOD_UL --era Run2_2018 --runUnscheduled --no_exec --mc -n {nEvents} || exit $? ;
#  cmsRun MINIAOD_cfg.py || exit $? ;
#  
#  ### NANOAOD step ###
#  cmsDriver.py --python_filename NANOAOD_cfg.py \\
#               --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM \\
#               --filein file:MINIAOD.root --fileout file:NANOAOD.root \\
#               --conditions 106X_upgrade2018_realistic_v16_L1v1 \\
#               --step NANO --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n {nEvents} || exit $? ;
#  cmsRun NANOAOD_cfg.py || exit $? ;
#  
#  ### Saving NANOAOD files ###
#  [ ! -d {output_dir}/{dataset_name} ] && mkdir -p {output_dir}/{dataset_name}
#  #mv MINIAOD.root {output_dir}/{dataset_name}/MINIAOD_{job_id}.root
#  cp -r  MINIAOD.root {output_dir}/{dataset_name}/MINIAOD_{job_id}.root
#  #mv NANOAOD.root {output_dir}/{dataset_name}/NANOAOD_{job_id}.root
#  cp -r NANOAOD.root {output_dir}/{dataset_name}/NANOAOD_{job_id}.root
#  
#  ### Cleaning ###
#  cd $CWD
#  rm -rf /u/user/seungjun/scratch/{dir_name}/job_{job_id}
#  echo "shell script has finished"
#  
# End of MC_Generation_Script_{job_id}.sh
EndOfMCGenerationFile

# Make file executable
chmod +x MC_Generation_Script_{job_id}.sh


'''
    
    return script

####################################################################################
def get_condor_submit_file(work_dir,run_dir, nJobs,job_num):
#def get_condor_submit_file(work_dir,run_dir, nJobs):
####################################################################################
    
    script_name = run_dir + "/MC_Generation_Script"
    #script_name = run_dir + "/mc_generation_job"
    
    file=''
    file+=f'RequestMemory         = 4 GB\n'
    file+=f'RequestDisk           = 12 GB\n'
    file+=f'universe              = vanilla\n'
    file+=f'getenv                = true\n'
    #file+=f'executable            = {script_name}_$(ProcId).sh\n'
    file+=f'executable            = {script_name}_{job_num}.sh\n'
    #file+=f'output                = {script_name}_$(ProcId).out\n'
    file+=f'output                = {script_name}_{job_num}.out\n'
    #file+=f'error                 = {script_name}_$(ProcId).err\n'
    file+=f'error                 = {script_name}_{job_num}.err\n'
    #file+=f'log                   = {script_name}_$(ProcId).log\n'
    file+=f'log                   = {script_name}_{job_num}.log\n'
    file+=f'transfer_executable   = True\n'
    file+=f'x509userproxy = {work_dir}/x509up\n'
    #file+=f'queue {nJobs}\n'
    file+=f'queue 1\n'
    file+=f'#\n'
    
    return file

####################################################################################
def get_find_script(output_dir, subdir_list, nJobs):
####################################################################################
    
    dirs_to_look = ''
    for d in subdir_list:
        dirs_to_look+=f'{output_dir}/{d} '
    
    file=''
    file+='#!/bin/sh\n\n'
    file+='#  @1  -->  "resubmit" for resubmition\n\n'
    file+='find '+dirs_to_look+'-name "*.root" > find_tmp\n\n'
    file+='array=()\n'
    file+='n_miss_job=0\n'
    file+='for j in {0..'+str(nJobs-1)+'}\n'
    file+='do\n'
    file+='if ! grep -q "_"${j}".root" find_tmp\n'
    file+='then\n'
    file+='    array+=(${j})\n'
    file+='    let n_miss_job++\n'
    file+='fi\n'
    file+='done\n\n'
    file+='echo ""\n'
    file+='echo "The number of missing files is: "${n_miss_job}\n'
    file+='echo ""\n'
    file+='echo "The jobs failed are: ${array[@]}"\n'
    file+='echo ""\n\n\n'
    file+='if [ "${1}" = "resubmit" ]\n'
    file+='then\n'
    file+='    [ -d resubmit ] && rm -rf resubmit\n'
    file+='    mkdir resubmit\n'
    file+='    n_sub_job=0\n'
    file+='    for j in ${array[@]}\n'
    file+='    do\n'
    file+='        cp mc_generation_job_${j}.sh resubmit/mc_generation_job_${n_sub_job}.sh\n'
    file+='        let n_sub_job++\n'
    file+='    done\n'
    file+='    cd resubmit\n'
    file+='    cp ../mc_generation_jobs.submit .\n'
    file+="    sed -i 's|HTCondor_run|HTCondor_run/resubmit|g' mc_generation_jobs.submit\n"
    file+="    sed -i 's|"+str(nJobs)+"|'${n_sub_job}'|g' mc_generation_jobs.submit\n"
    file+='    cd ../\n\n\n'
    file+='    echo "Jobs ready to be re-submitted in '+"'resubmit'"+' directory ... "\n'
    file+='fi\n\n'
    file+='echo ""\n\n'
    file+='rm find_tmp\n\n'
    file+='echo "done."\n\n'
    file+='echo ""\n'

    return file

####################################################################################
def main():
####################################################################################
    
    parser = ArgumentParser(description="Generate MC Events")
    parser.add_argument("--nJob", type=int, required=True, help="number of jobs per dataset")
    parser.add_argument("--nEvent", type=int, default=-1, required=False, help="number of events per job (nTot_dataset = nEvent x nJob)")
    args = parser.parse_args()
    
    if(not os.path.exists(work_dir)):
        os.system(f"mkdir {work_dir}")
    else:
        os.system(f"rm -rf {work_dir}/*")

    os.system(f"voms-proxy-init --voms cms -valid 192:00 --out {work_dir}/x509up")


    if(not os.path.exists(run_dir)):
        os.system(f"mkdir {run_dir}")
    else:
        os.system(f"rm -rf {run_dir}/*")
    
    fragment_dir = f'{work_dir}/fragments'
    if(not os.path.exists(fragment_dir)):
        os.system(f"mkdir {fragment_dir}")
    else:
        os.system(f"rm -rf {fragment_dir}/*")


    gridpack_dict = {
        #'bb4l_nominal':'/afs/cern.ch/user/s/seungjun/private/lhe_product/pwgevents-0001.lhe',
        'bb4l_nominal':'pwgevents-0001.lhe',
    }
    job_id=0
    for dataset in gridpack_dict.keys():
        
        with open(f'{fragment_dir}/{dataset}.py','w') as fragment_file:
            fragment_file.write(get_fragment())
            
        for iJob in range(args.nJob):
            
            with open(f'{run_dir}/mc_generation_job_{str(job_id)}.sh','w') as bash_file:
                bash_file.write(get_shell_script(dataset, args.nEvent , f'{fragment_dir}/{dataset}.py', job_id,dir_name))
            
            job_id+=1
    
    
    job_id=0
    for i_num in range(args.nJob):
        job_name = "0000"
        if job_id < 10:                        job_name ="000"+str(job_id)
        if job_id >= 10 and job_id < 100:       job_name ="00"+str(job_id)
        if job_id >= 100 and job_id < 1000:     job_name ="0"+str(job_id)
        if job_id >= 1000 and job_id < 10000:     job_name =str(job_id)


        with open(f'{run_dir}/mc_generation_jobs_{job_name}.submit','w') as file_out:
        #with open(f'{run_dir}/mc_generation_jobs_{str(job_id)}.submit','w') as file_out:
            file_out.write(get_condor_submit_file(work_dir,run_dir, job_id,job_id))
        job_id+=1

    with open(f'{run_dir}/find.sh','w') as file_out:
        file_out.write(get_find_script(output_dir, list(gridpack_dict.keys()), job_id))

    os.system(f'chmod u+x {run_dir}/*.sh')

    print(f'\nGeneration is ready to be submitted comprising {len(list(gridpack_dict.keys()))} sample(s) with {args.nJob*args.nEvent} event(s) each, total number of jobs is {job_id} ...\n')

if __name__ == "__main__":
    main()
## how am i 
