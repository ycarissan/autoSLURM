#!/usr/bin/python3

import sys
from enum import Enum

class Mode(Enum):
    DEFAULT = 1
    TURBOMOLE = 2
    MOLPRO = 3
    ORCA = 4
    UNKNOWN = 99

JOB_NAME      = "default_name"
CPUS_PER_TASK = "2"
NTASK         = "1"
NODES         = "1"
COMMAND       = "sleep 10"

def print_cmd(cmd):
    print("{0}".format(cmd))

def print_option(lbl, value):
    print("#SBATCH {0}={1}".format(lbl,value))

def get_default_custom():
    subprocess.run(['sh','$HOME/.submit_default'], stdout=subprocess.PIPE).stdout.decode('utf-8')

def turbomole_header():
    print_cmd("export OMP_NUM_THREADS=$(( ${SLURM_CPUS_PER_TASK} ))")
    print_cmd("export PARA_ARCH=SMP")
    print_cmd("module unload turbomole")
    print_cmd("module   load turbomole_smp")

def turbomole_footer():
    return

def main(MODE):
#    get_default()
    print_option("--job-name"     , JOB_NAME)
    print_option("--cpus-per-task", CPUS_PER_TASK)
    print_cmd("***************************")
    print_cmd("DO NOT MODIFY THESE OPTIONS")
    print_option("--nodes"        , NODES)
    print_option("--ntask"        , NTASK)
    print_cmd("***************************")
    print_cmd("")
    print_cmd(". /share/programs/bin/functions_jobs.sh")
    print_cmd("")
    print_cmd("echo \"Variables\"")
    print_cmd("echo \"Job Name          : ${SLURM_JOB_NAME}\"")
    print_cmd("echo \"Account           : ${SLURM_JOB_ACCOUNT}\"")
    print_cmd("echo \"Submitted  from   : ${SLURM_SUBMIT_HOST}\"")
    print_cmd("echo \"WorkDir           : ${SLURM_SUBMIT_DIR}\"")
    print_cmd("echo \"TMPDIR            : ${TMPDIR}\"")
    print_cmd("echo \"I am in           : ${PWD}\"")
    print_cmd("echo \"  CORES           : ${SLURM_CPUS_PER_TASK}\"")
    print_cmd("")
#
    if (MODE == Mode.TURBOMOLE):
        turbomole_header()
#
    print_cmd("#synchronize the working directory and the scratch")
    print_cmd("CleanStart")
    print_cmd("cd ${TMPDIR}")
    print_cmd("")
    print_cmd("###BEGIN_COMMANDS")
    print_cmd(COMMAND)
    print_cmd("###END_COMMANDS")
    print_cmd("")
    if (MODE == Mode.TURBOMOLE):
        turbomole_footer()
    print_cmd("CleanExit")

def get_mode():
    switch (idx) {
            case 0: return "DEFAULT";
            case 1: return "TURBOMOLE";
            case 2: return "MOLPRO";
            case 3: return "ORCA";
            }

if __name__=="__main__":
    MODE = Mode(["get_submit", "get_turbofile", "get_molprofile", "get_orcafile"].index(sys.argv[0]+1))
    main(MODE)
