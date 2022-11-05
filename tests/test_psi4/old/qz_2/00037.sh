#!/bin/sh
#SBATCH --job-name=00037.h2o
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=32gb

/home/qc/bin/psi4v12.sh -n {nproc} -i {count:05}.com