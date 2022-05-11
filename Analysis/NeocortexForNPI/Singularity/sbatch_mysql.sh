#!/usr/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH --time=1-0

MYSQL_LIB=$(mkdir -p var_lib_mysql && readlink -f var_lib_mysql)
MYSQL_RUN=$(mkdir -p var_run_mysql && readlink -f var_run_mysql)
MYSQL_FILES=$(mkdir -p var_lib_mysql-files && readlink -f var_lib_mysql-files)


singularity instance start --bind ${MYSQL_LIB}:/var/lib/mysql,${MYSQL_RUN}:/var/run/mysqld,${MYSQL_FILES}:/var/lib/mysql-files mysql-server_latest.sif mysql &

sleep 30

singularity run instance://mysql


