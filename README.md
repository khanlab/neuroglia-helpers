# neuroglia-helpers

Helper & wrapper scripts for using Singularity images locally and remotely on graham (compute canada) - or any other SLURM system

Features:
* wrapper scripts for submitting single and batch jobs using SLURM arrays
* variants of scripts that use (neuroglia*) and do not use (regular*) singularity
* scripts for interactive job submission 
* BIDS-App support with parallelization over subjects with SLURM arrays
* Deployment via Singularity (pulling containers from shub://, docker://, or file://)

## Install:

To set-up neuroglia-helpers on graham, run the following:
```
git clone http://github.com/khanlab/neuroglia-helpers ~/neuroglia-helpers
~/neuroglia-helpers/setup.sh
```

If you want to use a different configuration profile, e.g. `khanlab`, add it as an argument to `setup.sh`:
```
~/neuroglia-helpers/setup.sh khanlab
```


NOTE: You should remove any lines that source `00_init.sh` or set `SINGULARITY_*` variables in your `.bashrc` file. If the above lines are in your .bashrc file, then you will have problems using sftp or scp clients. If you need to use your .bashrc file, use the following:
```
echo "source ~/neuroglia-helpers/00_initrc.sh" >> ~/.bashrc
```

## Configuration

The `cfg/graham_default.cfg` file contains environment variables defining Compute Canada resource allocation accounts for compute jobs, and for defining where your Singularity container folder is placed.  

## Job templates

The wrappers make use of the job templates to define resources for submitted jobs, e.g. the number of CPUs, size of memory, and length of time. The predefined job templates are designed based on the size of Compute Canada (graham cluster) nodes and queues to make optimal use of the resources. You should use the template that best fits your job type. The `Regular` job type is default in most cases (8core, 32gb, 24hrs), but the full list of job templates can be found by using the `-J` option with any wrapper.

## BIDS Apps:

The bidsBatch wrapper uses SLURM to parallelize over *subjects*, and by default will run a job for every subject in your participants.tsv file. 
bidsBatch uses SLURM Arrays, so it groups all the different jobs under a single job ID, with each array job indicated as `<jobid>_<index>`.


Each deployed BIDS app has a name (unique identifier), a URI (location of the container), default options, and default job template. These are all stored in the `bids-apps.tsv` file. Each line is a different deployment, which may use the same container (URI) as another deployement, but e.g. with different default options and/or job templates.

The list of BIDS app names is given when you run `bidsBatch`.

To get a list of names for all BIDS apps deployed, along with URI and default job template, use `bidsBatch -B`.

To get usage information for a particular BIDS app, use `bidsBatch <app_name>`. This will also display the default options for that deployment.

Note: when you run bidsBatch to process a dataset located at `BIDS_DIR`, a `BIDS_DIR/code/jobs` folder is created containing the SLURM log files.


### Example: Running fmriprep on your bids dataset
```
bidsBatch fmriprep_1.0.4 ~/my-bids-dataset ~/my-bids-dataset/derivatives/fmriprep-v1.0.4 participant 
```
To get usage/options for a particular bids app, leave out the bids-app required arguments, e.g.:

```
bidsBatch fmriprep_1.0.4 
```





## Wrappers:

Wrappers for singularity and job submission that make use of the neuroglia configuration.

* neuroglia

Simple wrapper for singularity exec (does not submit a job)

* neurogliaShell

Simple wrapper for singularity shell (does not submit a job)

* neurogliaSubmit

Creates and submits a singularity exec job, e.g.: `neurogliaSubmit bet t1.nii` will submit a job to perform bet skull stripping.
Enter `neurogliaSubmit` for more details.

* neurogliaBatch

Wrapper for submitting batch cluster jobs, using a singularity container, looping through a subject list. User provides the command to run, and the arguments that come before and after the subjid.  Enter `neurogliaBatch` for more details.

* regularSubmit, regularBatch

These are the analogous to neurogliaSubmit and neurogliaBatch, but run the commands directly and do not use `singularity exec`.

* regularInteractive

Wrapper for submitting an interactive cluster job, this gives you command-line access to a compute node terminal for a short period of time (up to 3 hours), to run jobs directly. Remember that you are not supposed to run any jobs directly on the *login* nodes. 

Note: interactive job default is 3hours, 8cores, 32GB memory

With `regularInteractive` you can also run GUI applications from Compute Canada, if you use `ssh -Y` when connecting to graham.



