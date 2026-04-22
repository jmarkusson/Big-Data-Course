#!/bin/bash
#SBATCH -J ApptainerPractise
#SBATCH -t 00:01:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=outputPart2_%j.txt

Path="DAT471/assignment1_problem2c.py"
CONTAINER="/data/courses/2026_dat471_dit066/containers/assignment1.sif"
DATA="/data/courses/2026_dat471_dit066/datasets/bike_sharing_hourly.csv"

apptainer exec --bind /data "$CONTAINER" python3 "$Path" "$DATA"