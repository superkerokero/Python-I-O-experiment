#!/usr/bin/bash
# This script runs mreusBot.py and ensures its activity no matter what.

# first retrieve command line arguments.
start=""
end=""
workdir="/home/wanglj/multi_reus/multi1"
machinefile="mpd.hosts"
head_nml="namelist"
exec="/home/wanglj/FreeFlex/FreeFlex.exe"
n_core="112"
stime=""

if [ ! -z $1 ]; then
  start=$1
else
  start="1"
fi
if [ ! -z $2 ]; then
  end=$2
else
  end="4"
fi
if [ ! -z $3 ]; then
  stime=$3
else
  stime="10"
fi

# cd to working directory.
cd $workdir
echo "Current directory:" $PWD

# run program.
for i in $(seq $start $end);
do
  f_nml=$head_nml$i
  f_log="./0000/log"$i
  if [ -f $f_log ]; then
    echo $f_log "exists. Skip to next round."
  else
    echo Sleep for $stime secs.
    sleep ${stime}s
    echo Starting round $i.
    args="mpiexec -machinefile "$machinefile" -n "$n_core
    args=$args" "$exec" "$f_nml
    echo "Performing the following command."
    echo $args
    $args
  fi
done

echo "All batch tasks completed!"
