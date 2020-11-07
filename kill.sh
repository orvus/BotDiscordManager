#!/bin/bash

while [[ $# -gt 0 ]]; do
  case "$1" in
    --chan)
        pid=`ps aux | grep "channelManager.py" | cut -d' ' -f 2`
        if [[ ! -z "$pid" ]]
        then
            echo "chan pid ${pid}"
            kill -9 ${pid}
        else
            echo "no pid found for CHAN"
        fi
      ;;
    --react)
        pid=`ps aux | grep "reactionManager.py" | cut -d' ' -f 2`
        if [[ ! -z "$pid" ]]
        then
            echo "react pid ${pid}"
            kill -9 ${pid}
        else
            echo "no pid found for REACT"
        fi
      ;;
    --siteswap)
        pid=`ps aux | grep "siteswap.py" | cut -d' ' -f 2`
        if [[ ! -z "$pid" ]]
        then
            echo "siteswap pid ${pid}"
            kill -9 ${pid}
        else
            echo "no pid found for SITESWAP"
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