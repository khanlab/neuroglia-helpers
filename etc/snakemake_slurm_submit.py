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
account = os.getenv('CC_COMPUTE_ALLOC', default='rrg-akhanf')

#if len(job_properties['log']) > 0 :
#    log = job_properties['log'][0]
#else:
    
log = os.path.join('logs','slurm','slurm_%j_{}_{}.out'.format(job_properties['jobid'],job_properties['rule']))

log = os.path.realpath(log)

#create the log directory (slurm fails if doesn't exist)
log_dir = os.path.dirname(log)
if not os.path.exists(os.path.dirname(log)):
    os.makedirs(log_dir)

#get values and set defaults
if 'time' in job_properties["resources"].keys():
    time = job_properties["resources"]["time"]
else:  
    time = 60

if 'mem_mb' in job_properties["resources"].keys():
    mem_mb = job_properties["resources"]["mem_mb"]
else:  
    mem_mb = 4000

#threads already set to 1 by default
threads = job_properties["threads"]


# collect all command-line options in an array
cmdline = ["sbatch"]

# set all the slurm submit options as before
slurm_args = " --parsable --account={account} --time={time} --mem={mem_mb} --cpus-per-task={threads} --output={log} ".format(account=account, time=time, mem_mb=mem_mb, threads=threads,log=log)

cmdline.append(slurm_args)

if dependencies:
    cmdline.append("--dependency")
    # only keep numbers in dependencies list
    dependencies = [ x for x in dependencies if x.isdigit() ]
    cmdline.append("afterok:" + ",".join(dependencies))

cmdline.append(jobscript)

os.system(" ".join(cmdline))
