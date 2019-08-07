#!/bin/bash

#source this script in your .bashrc: (required if you run commands directly with ssh)
#  source ~/neuroglia-helpers/00_initrc.sh 

if [ ! -n "$SINGULARITY_DIR" ]
then
	
#	echo "Sourcing light version of $NEUROGLIA_DIR/00_init.sh from $BASH_SOURCE"

	export NEUROGLIA_DIR=$(dirname `realpath $BASH_SOURCE`)
	source $NEUROGLIA_DIR/00_init.sh light
fi

