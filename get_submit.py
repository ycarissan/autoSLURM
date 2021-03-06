#!/usr/bin/python3

import os
import sys
from enum import Enum

version="# version 1.0.2"

class Mode(Enum):
    DEFAULT = 1
    TURBOMOLE = 2
    MOLPRO = 3
    ORCA = 4
    UNKNOWN = 99

JOB_NAME      = "default_name"
NTASKS        = "2"
CPUS_PER_TASK = "1"
NODES         = "1"
MEM           = "1000"
COMMAND       = "sleep 10"

fout = open("submit.job","w+")

def print_cmd(cmd):
    fout.write("{0}\n".format(cmd))

def print_option(lbl, value):
    fout.write("#SBATCH {0}={1}\n".format(lbl,value))

def get_default_custom():
    subprocess.run(['sh','$HOME/.submit_default'], stdout=subprocess.PIPE).stdout.decode('utf-8')

###
#TURBOMOLE SPECIFIC ROUTINES
###
def turbomole_header():
    print_cmd("export OMP_NUM_THREADS=$(( ${SLURM_NTASKS} ))")
    print_cmd("export PARNODES=$(( ${SLURM_NTASKS} ))")
    print_cmd("export PARA_ARCH=SMP")
    print_cmd("module unload turbomole")
    print_cmd("module   load turbomole_smp")
    default_header()

def turbomole_footer():
    default_footer()
    return

def turbomole_cmd():
    print_cmd('ridft > ridft.log')
    return

###
#MOLPRO SPECIFIC ROUTINES
###
def molpro_header():
    print_cmd("module load molpro")

def molpro_footer():
    return

def molpro_cmd():
    print_cmd('molpro -n${SLURM_NTASKS} -d ${TMPDIR} -W ${PWD} -h${SLURM_JOB_NODELIST} molpro.in')
    return

###
#ORCA SPECIFIC ROUTINES
###
def orca_header():
    print_cmd("module load orca")
    default_header()

def orca_footer():
    default_footer()
    return

def orca_cmd():
    print_cmd('$ORCA/orca orca.inp > orca.out')
    return

###
#DEFAULT ROUTINES
###
def default_header():
    print_cmd("#synchronize the working directory and the scratch")
    print_cmd("CleanStart")
    print_cmd("cd ${TMPDIR}")
    print_cmd("")

def default_footer():
    print_cmd("CleanExit")
    return

def default_cmd():
    print_cmd('sleep 10')
    return

def head():
    print_cmd("#!/bin/sh")
    print_cmd(version)
    print_cmd("#")
    print_option("--job-name"     , JOB_NAME)
    print_option("--ntasks"       , NTASKS)
    print_option("--mem", MEM)
    print_cmd("#***************************")
    print_cmd("#DO NOT MODIFY THESE OPTIONS")
    print_option("--nodes"        , NODES)
    print_option("--cpus-per-task", CPUS_PER_TASK)
    print_cmd("#***************************")
    print_cmd("")
    print_cmd(". /share/programs/bin/functions_jobs.sh")
    print_cmd("")
    print_cmd("echo \"Variables\"")
    print_cmd("echo \"Job Name          : ${SLURM_JOB_NAME}\"")
    print_cmd("echo \"Account           : ${SLURM_JOB_ACCOUNT}\"")
    print_cmd("echo \"Submitted  from   : ${SLURM_SUBMIT_HOST}\"")
    print_cmd("echo \"Nodelist          : ${SLURM_JOB_NODELIST}\"")
    print_cmd("echo \"WorkDir           : ${SLURM_SUBMIT_DIR}\"")
    print_cmd("echo \"TMPDIR            : ${TMPDIR}\"")
    print_cmd("echo \"I am in           : ${PWD}\"")
    print_cmd("echo \"  NTASKS          : ${SLURM_NTASKS}\"")
    print_cmd("")

def main(MODE):
    head()
#
    if (MODE == Mode.TURBOMOLE):
        turbomole_header()
    elif (MODE == Mode.MOLPRO):
        molpro_header()
    elif (MODE == Mode.ORCA):
        orca_header()
    else:
        default_header()
#
    print_cmd("###BEGIN_COMMANDS")
    if (MODE == Mode.TURBOMOLE):
        turbomole_cmd()
    elif (MODE == Mode.MOLPRO):
        molpro_cmd()
    elif (MODE == Mode.ORCA):
        orca_cmd()
    else:
        default_cmd()
    print_cmd("###END_COMMANDS")
    print_cmd("")
    if (MODE == Mode.TURBOMOLE):
        turbomole_footer()
    elif (MODE == Mode.MOLPRO):
        molpro_footer()
    elif (MODE == Mode.ORCA):
        orca_footer()
    else:
        default_footer()

if __name__=="__main__":
    call_name = os.path.basename(sys.argv[0])
    MODE = Mode(["get_submit", "get_turbofile", "get_molprofile", "get_orcafile"].index(call_name)+1)
    main(MODE)
