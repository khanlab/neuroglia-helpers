#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cfg_profile=_$1
else
  cfg_profile=
fi

echo "cfg_profile=${cfg_profile}" >> ~/.bash_profile
echo "source ~/neuroglia-helpers/00_init.sh" >> ~/.bash_profile
echo "module load singularity" >> ~/.bash_profile
