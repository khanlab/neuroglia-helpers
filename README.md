# neuroglia-helpers

Helper & wrapper scripts for using the neuroglia (and neuroglia-vasst-dev) singularity image locally and remotely on graham (compute canada)


### Install:
```
git clone http://github.com/khanlab/neuroglia-helpers ~/neuroglia-helpers
echo "export PATH=~/neuroglia-helpers:\$PATH" >> ~/.bashrc
echo "export SINGULARITY_DIR=/project/6007967/akhanf/singularity" >> ~/.bashrc
echo "export SINGULARITY_IMG=\${SINGULARITY_DIR}/khanlab_neuroglia-vasst-dev_0.0.2.img" >> ~/.bashrc
echo "export SINGULARITY_OPTS=\"-e -B /cvmfs:/cvmfs -B /project:/project -B /scratch:/scratch\"" >> ~/.bashrc
```

### Wrappers:

Wrappers for singularity that make use of the following environment variables in your environment (set in .bashrc):
```
SINGULARITY_DIR=<path to folder containing singularity images>
SINGULARITY_IMG=<path to default (neuroglia) singularity container>
SINGULARITY_OPTS=<options for singularity, e.g. path binding>
```



* neuroglia

Simple wrapper for singularity exec (does not submit a job)

* neurogliaShell

Simple wrapper for singularity shell (does not submit a job)

* neurogliaInteractive

Wrapper for submitting an interactive cluster job, using a singularity container
Note: interactive job default is 1hour, 8cores, 32GB memory

* neurogliaBatch

Wrapper for submitting batch cluster jobs, using a singularity container

```
==========================================================================
Interface for running pipeline scripts on the cluster with singularity

  Loops through an input subject_list_txt (txt with subj id on each line)
  Can be used to run scripts that generally take command-line parameters as:

  <script_name> <before args (optional)> <subjid (required)> <after args (optional)>

--------------------------------------------------------------------------
Usage: neurogliaBatch  <script_name>  <subject_list_txt>  <optional flags> 
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




