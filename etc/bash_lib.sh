#!/bin/bash

# various functions for printing usage and job/app lists

function usage_batch_before_after {
   echo " Passing arguments to pipeline script:"
   echo "  -b /"args/" : cmd-line arguments that go *before* the subject id"
   echo "  -a /"args/" : cmd-line arguments that go *after* the subject id"
   echo ""
 }

function usage_job_templates {
   echo " Required resources:"
   echo " -j <job-template> :  sets requested resources"
   echo "	Regular (default):	8core/32gb/24h"
   echo "	LongSkinny:		1core/4gb/72h"
   echo "	ShortFat:		32core/128gb/3h"
   echo "  (for a list of ALL job templates, use the -J option)"
   echo ""
}

function usage_job_depends {
   echo " SLURM Job dependencies for pipelining (man sbatch for more details):"
   echo "  -d aftercorr:jobid[:jobid]	: each subj depends on completed subj in submitted job ids"  
   echo "  -d afterok:jobid[:jobid]	: each subj depends on all completed subj in submitted job id"
   echo ""
}


function print_job_templates {
	_print_job_templates | column -t >&2 
}

#miscellaneous shared functions
function _print_job_templates {


job_template_dir=$NEUROGLIA_DIR/job-templates

#want to print out full listing of job templates
echo "job-template ncpus mem_mb time"
for t in `ls $job_template_dir/*.job`
do
  name=${t##*/}
  name=${name%.job}
  mem=`grep mem= $t`
  mem=${mem##*=}
  ncpu=`grep cpus-per-task= $t`
  ncpu=${ncpu##*=}
  wtime=`grep time= $t`
  wtime=${wtime##*=}

 echo "$name $ncpu $mem $wtime"	

done


}



function print_app_list_names {

	app_list=$NEUROGLIA_DIR/bids-apps.tsv
	nlines=`cat $app_list | wc -l`
	tail -n $((nlines-1)) $app_list | awk -F '\t' '{print $1}' | column -c 150
}

function print_app_list_long {

	app_list=$NEUROGLIA_DIR/bids-apps.tsv
	cat $app_list | awk -F '\t' '{print $1 "\t"  $2  "\t" $4 }' | column -t

}

