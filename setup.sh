#!/usr/bin/env bash

execpath=`dirname $0`
execpath=`realpath $execpath`


if [ $# -gt 0 ]; then
  cfg_profile=_$1
else
  cfg_profile=
fi

echo "module load singularity/3.2" >> ~/.bash_profile
echo "cfg_profile=${cfg_profile}" >> ~/.bash_profile
echo "source $execpath/00_init.sh" >> ~/.bash_profile
