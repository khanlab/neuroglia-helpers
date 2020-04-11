#!/usr/bin/env python3
import os
import sys

from snakemake.utils import read_job_properties

# last command-line argument is the job script
jobscript = sys.argv[-1]

# all other command-line arguments are the dependencies
dependencies = set(sys.argv[1:-1])


# parse the job script for the job properties that are encoded by snakemake within
job_properties = read_job_properties(jobscript)


# get account from CC_COMPUTE_ALLOC, else supply default account
account = os.getenv('CC_COMPUTE_ALLOC', default='ctb-akhanf')

   

if job_properties["type"]=='single':
    
    #this is a single rule, so set the resource request based on the rule itself
    # or to single rule defaults (1 core, 1hr, 4gb)
    job_name = job_properties['rule']

    #get values and set defaults
    if 'time' in job_properties["resources"].keys():
        time = job_properties["resources"]["time"]
    else:  
        time = 60

    if 'mem_mb' in job_properties["resources"].keys():
        mem_mb = job_properties["resources"]["mem_mb"]
    else:  
        mem_mb = 4000

    if 'gpus' in job_properties["resources"].keys():
        gpus = job_properties["resources"]["gpus"]
    else:  
        gpus = 0

    #for single job, threads already set to 1 by default
    threads = job_properties["threads"]


elif job_properties["type"]=='group':

    #for a grouped rule, we request an entire node in order to maximize throughput:
    job_name = job_properties['groupid']

    # Maybe look into later: add some checks to 
    #  1) set a reasonable walltime (less than 24hrs) based on 1hr 1core jobs
    #  2) check when there may be too many jobs in the group
    # if 2), could always try to resubmit with larger job?  
    
    time = 60*24
    mem_mb = 128000
    threads = 32
    gpus = 0

else:
    raise NotImplementedError(f"Don't know what to do with job_properties['type']=={job_properties['type']}")



log = os.path.realpath(os.path.join('logs','slurm',f'slurm_%j_{job_name}.out'))

#create the log directory (slurm fails if doesn't exist)
log_dir = os.path.dirname(log)
if not os.path.exists(os.path.dirname(log)):
    os.makedirs(log_dir)



# collect all command-line options in an array
cmdline = ["sbatch"]

if gpus > 0:
    gpu_arg = f'--gres=gpu:t4:{gpus}'
else:
    gpu_arg = ''

# set all the slurm submit options as before
slurm_args = f" --parsable --account={account} {gpu_arg} --time={time} --mem={mem_mb} --cpus-per-task={threads} --output={log} "

cmdline.append(slurm_args)

if dependencies:
    cmdline.append("--dependency")
    # only keep numbers in dependencies list
    dependencies = [ x for x in dependencies if x.isdigit() ]
    cmdline.append("afterok:" + ",".join(dependencies))

cmdline.append(jobscript)

os.system(" ".join(cmdline))
