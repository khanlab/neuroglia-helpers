# neuroglia-helpers

Helper & wrapper scripts for using the neuroglia (and neuroglia-vasst-dev) singularity image locally and remotely on graham (compute canada)


## Install:
```
git clone http://github.com/khanlab/neuroglia-helpers ~/neuroglia-helpers
echo "export PATH=~/neuroglia-helpers:\$PATH" >> ~/.bashrc
echo "export SINGULARITY_IMG=/project/6007967/akhanf/singularity/khanlab_neuroglia-vasst-dev_0.0.1e.img" >> ~/.bashrc
echo "export SINGULARITY_OPTS=\"-e -B /project:/project -B /scratch:/scratch\"" >> ~/.bashrc
```

## Wrappers:

Wrappers for singularity that make use of the following environment variables in your environment (set in .bashrc):
```
SINGULARITY_IMG=<location of singularity container>
SINGULARITY_OPTS=<options for singularity exec>
```



* neuroglia

Wrapper for singularity exec. 

* neurogliaArray 

```
==========================================================================
Interface for running pipeline scripts on the cluster with singularity

  Loops through an input subject_list_txt (txt with subj id on each line)
  Can be used to run scripts that generally take command-line parameters as:

  <script_name> <before args (optional)> <subjid (required)> <after args (optional)>

--------------------------------------------------------------------------
Usage: neurogliaArray  <script_name>  <subject_list_txt>  <optional flags> 
--------------------------------------------------------------------------

optional flags:

 -g : group/reduce job, pass the subject list instead of looping over subjects
 -s <subjid> : single-subject mode, run on a single subject (must be in subjlist) instead
 -t : test-mode, don/'t actually submit any jobs

 Required resources:
 -j <job-template> :  sets requested resources
	Regular (default):	8core/32gb/24h
	LongSkinny:		1core/4gb/72h
	ShortFat:		32core/128gb/3h

 Passing arguments to pipeline script
  -b /args/ : cmd-line arguments that go *before* the subject id
  -a /args/ : cmd-line arguments that go *after* the subject id

 SLURM Job dependencies for pipelining (man sbatch for more details):
  -d aftercorr:jobid[:jobid]	: each subj depends on completed subj in submitted job ids
  -d afterok:jobid[:jobid]	: each subj depends on all completed subj in submitted job id
```


