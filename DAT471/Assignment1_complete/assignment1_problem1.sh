#!/bin/bash

#SBATCH -J NodeSpecs
#SBATCH -t 00:01:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --output=output_%j.txt
#SBATCH --nodelist=europa,uranus

echo "Models selected"
echo $SLURM_JOB_NODELIST

echo "======================================="
srun -l lscpu | grep -E "Model name|CPU\(\s)|MHz|Socket\(s\)|Thread\(s\)"
echo "======================================="
echo "Model Name"
srun -l lscpu | grep "Model name"
echo "======================================="
echo "CPU Frequency:"
srun -l lscpu | grep "MHz"
echo "======================================="
echo "CPU Cores:"
srun -l lscpu | grep "CPU(s)"
echo "======================================="
echo "CPU Sockets"
srun -l lscpu | grep "Socket(s):"
echo "======================================="
echo "Architecture:"
srun -l lscpu | grep "Architecture"
echo "======================================="
echo "Cache length:"
#srun -l lscpu 
echo "L1d cache:"
srun -l lscpu | grep "L1d cache"
echo "L1i cache:"
srun -l lscpu | grep "L1i cache"
echo "L2 cache:"
srun -l lscpu | grep "L2 cache"
echo "L3 cache:"
srun -l lscpu | grep "L3 cache"
echo "======================================="
echo "System RAM:"
srun -l free -h
echo "---------------------------------------"
echo "GPU Count:"
srun -l bash -c 'nvidia-smi -L | wc -l'
echo "---------------------------------------"
echo "GPU Memory:"
srun -l nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader
echo "======================================="
echo "Type and size of filesystem:"
srun -l df -hT /data
echo "======================================="
echo GNU/Linux distribution:
srun -l uname -v
echo "======================================="
echo GNU/Linux version:
srun -l uname -r
echo "======================================="
echo python3 version:
srun -l python3 --version
echo "======================================="