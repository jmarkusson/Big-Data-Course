#!/bin/bash
#SBATCH -J ApptainerPractise
#SBATCH -t 00:01:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=outputPart2_%j.txt


# Path: /data/2026_dat471_dit066/containers/assignment1.sif
# Path to data: /data/2026_dat471_dit066/datasets/bike_sharing_hourly.csv

CONTAINER="/data/courses/2026_dat471_dit066/containers/assignment1.sif"


echo Kernel version inside the container:
apptainer exec $CONTAINER uname -r
echo ==========================================================================

echo Python3 version inside the container:
apptainer exec $CONTAINER python3 --version
echo ==========================================================================


echo CPU Model:
apptainer exec $CONTAINER lscpu | grep "Model name"
echo ==========================================================================
