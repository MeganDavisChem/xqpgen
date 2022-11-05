#!/bin/sh
#SBATCH --job-name=00038.h2o
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=32gb

/home/qc/bin/psi4v12.sh -n 4 -i 00038.com