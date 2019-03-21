#!/bin/bash

export NEUROGLIA_DIR=$(dirname `realpath $BASH_SOURCE`)

export PATH=${NEUROGLIA_DIR}/bin:$PATH
export NEUROGLIA_BASH_LIB=$NEUROGLIA_DIR/etc/bash_lib.sh

set -a
source $NEUROGLIA_DIR/cfg/graham.cfg
set +a

#make SINGULARITY_DIR if it doesn't exist
if [ ! -e $SINGULARITY_DIR ]
then
	mkdir -p $SINGULARITY_DIR 

	if [ ! "$?" = 0 -o ! -e $SINGULARITY_DIR ]
	then
		echo "neuroglia-helpers init error:  Unable to set local SINGULARITY_DIR to $SINGULARITY_DIR"
	fi

fi
