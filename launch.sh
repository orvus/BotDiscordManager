#!/bin/bash

while [[ $# -gt 0 ]]; do
  case "$1" in
    --chan)
      chan=1
      ;;
    --react)
      react=1
      ;;
    --siteswap)
      siteswap=1
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

if [[ ${react} -eq 1 ]]
then
    echo "launch : reaction manager"
    touch log/react.log
    echo > log/react.log
    nohup python3 reactionManager.py & > log/react.log
fi

if [[ ${chan} -eq 1 ]]
then
    echo "launch : channel manager"
    touch log/chan.log
    echo > log/chan.log
    nohup python3 channelManager.py & > log/chan.log
fi

if [[ ${siteswap} -eq 1 ]]
then
    echo "launch : siteswap"
    touch log/siteswap.log
    echo > log/siteswap.log
    nohup python3 siteswap.py & > log/siteswap.log
fi
