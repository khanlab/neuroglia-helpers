#!/bin/bash

hours=6
mem=128000
gpus=1
cpus=32
account=ctb-akhanf


if [ "$#" -lt 2 ]
then
  echo "Usage $0 RULE_NAME NUM_BATCHES <optional snakemake args>" 
  echo ""
  echo "This script is used to submit batches  as cluster jobs, with the final batch dependent on the previous ones"
  echo ""
  echo "Runs the following (with RULENAME, N specified as required args):"
  echo "    snakemake -j $cpus --resources mem_mb=$mem gpus=$gpus --use-singularity --use-envmodules --batch RULE_NAME=i/NUM_BATCHES --nolock  "
  echo "" 
  exit 1
fi

rule=$1
N=$2

shift 2

mkdir -p jobs
job=jobs/batch_rule-${rule}_N-${N}.job

echo "#!/bin/bash" > $job
echo "#SBATCH --ntasks=1" >> $job
echo "#SBATCH --nodes=1" >> $job
echo "#SBATCH --time=${hours}:00:00" >> $job
echo "#SBATCH --cpus-per-task=${cpus}" >> $job
echo "#SBATCH --gres=gpu:t4:${gpus}" >> $job
echo "#SBATCH --mem=${mem}" >> $job
echo "#SBATCH --account=${account}" >> $job
echo "#SBATCH --output=jobs/batch_rule-${rule}_N-${N}.%A_%a.out" >> $job

echo cd $PWD >> $job
echo snakemake -j $cpus --resources mem_mb=$mem gpus=$gpus --use-singularity --use-envmodules --batch ${rule}=\${SLURM_ARRAY_TASK_ID}/${N} --nolock $@ >> $job

#submit array job for 1-$((N-1))
message=`sbatch --array=1-$((N-1)) $job`

# Extract job identifier from SLURM's message.
if ! echo ${message} | grep -q "[1-9][0-9]*$"; then 
	echo "Job(s) submission failed." >&2
	echo ${message} >&2
	exit 1
else
	jobid=$(echo ${message} | grep -oh "[1-9][0-9]*$")
fi

#submit array job for $N (dependent on prev)
sbatch --dependency=afterany:$jobid --array=$N $job
