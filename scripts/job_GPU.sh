#!/bin/bash
# example job script for anaconda
#$ -N GPU_cho2t1000
#$ -cwd
# 在 GPU 队列中请求一个 GPU：
#$ -q gpu 
#$ -l gpu=1
#$ -l h_rt=01:00:00 # only runs for 30  mins!
#$ -l h_vmem=32G
#$ -m bea -M s2751161@ed.ac.uk # CHANGE THIS TO YOUR EMAIL ADDRESS

. /etc/profile.d/modules.sh
module load anaconda # this loads a specific version of anaconda
conda activate cellposeSAM # this starts the 'mypython' environment

nvidia-smi --query-gpu=timestamp,name,memory.used,memory.total,utilization.gpu --format=csv -l 1 > gpu_log.csv &

python train.py 


