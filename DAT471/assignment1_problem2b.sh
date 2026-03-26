#!/bin/bash
#SBATCH -J ApptainerPractise
#SBATCH -t 00:01:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=outputPart2_%j.txt


# Path: /data/2026_dat471_dit066/containers/assignment1.sif/opt/mystery.py
# Path to data: /data/2026_dat471_dit066/datasets/bike_sharing_hourly.csv

CONTAINER="/data/courses/2026_dat471_dit066/containers/assignment1.sif"
DATA="/data/courses/2026_dat471_dit066/datasets/bike_sharing_hourly.csv"
MYSTERY_PATH="/opt/mystery.py"

echo "[$DATA]"
ls -l "$DATA"

apptainer exec --bind /data $CONTAINER python3 $MYSTERY_PATH $DATA

echo ==============================
apptainer exec $CONTAINER cat $MYSTERY_PATH

# avg_hourly_count_good_weather = df.query('weathersit == 1').groupby('hr')['cnt'].mean()
# avg_hourly_count_bad_weather = df.query('weathersit >= 3').groupby('hr')['cnt'].mean()
# worst_hourly_penalty = (avg_hourly_count_good_weather - avg_hourly_count_bad_weather).argmax()
# print(worst_hourly_penalty)

# The biggest difference of n bikes rented when comparing good weather and bad weather
# at the same hours is at hour: 17