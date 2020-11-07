#!/bin/bash

function kill_chan{
    pid=`ps aux | grep "python3 channelManager.py" | grep -v "grep" | awk '{print $2}'`
    if [[ ! -z "$pid" ]]
    then
        echo "chan pid ${pid}"
        kill -9 ${pid}
    else
        echo "no pid found for CHAN"
    fi
}
function kill_react{
    pid=`ps aux | grep "reactionManager.py" | grep -v "grep" | awk '{print $2}'`
    if [[ ! -z "$pid" ]]
    then
        echo "react pid ${pid}"
        kill -9 ${pid}
    else
        echo "no pid found for REACT"
    fi
}

function kill_siteswap{
    pid=`ps aux | grep "siteswap.py" | grep -v "grep" | awk '{print $2}'`
    if [[ ! -z "$pid" ]]
    then
        echo "siteswap pid ${pid}"
        kill -9 ${pid}
    else
        echo "no pid found for SITESWAP"
    fi
}


while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
       kill_chan
       kill_react
       kill_siteswap
       exit 1
      ;;

    --chan)
        kill_chan
        exit 1
      ;;
    --react)
        kill_react
        exit 1
      ;;
    --siteswap)
        kill_siteswap
        exit 1
      ;;
    --help|-h)
      printf "Meaningful help message" # Flag argument
      exit 0
      ;;
    *)
      >&2 printf "Error: Invalid argument\n"
      exit 1
      ;;
  esac
  shift
done