CC_COMPUTE_ALLOC=rrg-akhanf #for compute resources
CC_STORAGE_ALLOC=rrg-akhanf  #for singularity image storage

SINGULARITY_OPTS="-e -B /cvmfs:/cvmfs -B /project:/project -B /scratch:/scratch -B /localscratch:/localscratch"
NEUROGLIA_URI="shub://akhanf/vasst-dev:v0.0.4g"


USER_STORAGE=$HOME/projects/$CC_STORAGE_ALLOC/$USER
SINGULARITY_DIR=$USER_STORAGE/singularity
if [ ! -e $USER_STORAGE ]
then
 echo "Project space storage folder, $USER_STORAGE does not exist, is $CC_STORAGE_ALLOC the correct allocation?"
 exit 1
fi

#make SINGULARITY_DIR if it doesn't exist
if [ ! -e $SINGULARITY_DIR ]
then
	mkdir -p $SINGULARITY_DIR 
fi

if [ ! "$?" = 0 -o ! -e $SINGULARITY_DIR ]
then
	echo "Unable to set local SINGULARITY_DIR to $SINGULARITY_DIR"
	exit 1
fi

#source other helpers
source $(dirname $0)/01_utils.sh
