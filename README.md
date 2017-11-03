# neuroglia-helpers

Helper & wrapper scripts for using the neuroglia (and neuroglia-vasst-dev) singularity image locally and remotely on graham (compute canada)


## Install:
```
git clone http://github.com/khanlab/neuroglia-helpers ~/neuroglia-helpers
echo "export PATH=~/neuroglia-helpers:\$PATH" >> ~/.bashrc
echo "export SINGULARITY_IMG=/project/6007967/akhanf/singularity/khanlab_neuroglia-vasst-dev_0.0.1e.img" >> ~/.bashrc
echo "export SINGULARITY_OPTS=\"-e -B /project:/project -B /eq-nas:/eq-nas\"" >> ~/.bashrc
```

## Wrappers:

Wrappers for singularity that make use of the following environment variables in your environment (set in .bashrc):
```
SINGULARITY_IMG=<location of singularity container>
SINGULARITY_OPTS=<options for singularity exec>
```



* neuroglia <command to run>
Wrapper for singularity exec. 

* neurogliaBatch <script/exec-name> <subjlist> <opt args>
Wrapper to submit jobs on graham. Will loop over subjlist and submit jobs (8core,32G,24h) for each as:
neuroglia <script/exec-name> <opt args> <subj i>


