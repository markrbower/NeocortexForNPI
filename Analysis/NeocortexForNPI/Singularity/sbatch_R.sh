#!/usr/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=256GB
#SBATCH --time=1-0

DATA=$(readlink -f Data/Halo_data_from_Roni)
singularity exec --bind ${DATA}:/data/Halo_data_from_Roni/ --bind /ocean/projects/ibn210001p/mbower:/mnt npi.sif Rscript /mnt/r_script.R
