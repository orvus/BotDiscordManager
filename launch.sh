#!/bin/bash

while [[ $# -gt 0 ]]; do
  case "$1" in
    --chan)
        python3 channelManager.py > log/chan.log &
        pid=`jobs -l | grep "channelManager.py" | cut -d' ' -f 2`
        if [[ -z "$pid" ]]
        then
            echo "chan pid ${pid}"
        fi
      ;;
    --react)
        python3 reactionManager.py > log/react.log &
        pid=`jobs -l | grep "reactionManager.py" | cut -d' ' -f 2`
        if [[ -z "$pid" ]]
        then
            echo "react pid ${pid}"
        fi
      ;;
    --siteswap)
        python3 siteswap.py > log/siteswap.log &
        pid=`jobs -l | grep "siteswap.py" | cut -d' ' -f 2`
        if [[ -z "$pid" ]]
        then
            echo "siteswap pid ${pid}"
        fi
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