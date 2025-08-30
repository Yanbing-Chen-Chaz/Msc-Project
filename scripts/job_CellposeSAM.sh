#!/bin/bash
# example job script for anaconda
#$ -N cellposeSAM_CPU_cho2_t
#$ -cwd

#$ -l h_rt=02:00:00 # only runs for 30  mins!
#$ -l h_vmem=32G
#$ -m bea -M s2751161@ed.ac.uk # CHANGE THIS TO YOUR EMAIL ADDRESS

. /etc/profile.d/modules.sh
module load anaconda # this loads a specific version of anaconda
conda activate cellposeSAM # this starts the 'mypython' environment

echo "CPU–Õ∫≈–≈œ¢£∫"
cat /proc/cpuinfo | grep 'model name' | uniq

/usr/bin/time -v python CP_SAM2.py 