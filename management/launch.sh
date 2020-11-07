#!/bin/bash

log_dir="../log/"
log_channel="chanManager.log"
log_reaction="reactManager.log"
log_siteswap="siteswap.log"

script_dir="./"



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

touch ${log_dir}${log_reaction}
touch ${log_dir}${log_siteswap}
touch ${log_dir}${log_channel}


echo > ${log_dir}${log_reaction}
echo > ${log_dir}${log_siteswap}

if [[ ${react} -eq 1 ]]
then
    echo "launch : reaction managet"
    echo > "${log_dir}${log_reaction}"
    cd ${script_dir}
    nohup python3 reactionManager.py & > "${log_dir}${log_react}"
    cd -
fi

if [[ ${chan} -eq 1 ]]
then
    echo "launch : channel manager"
    echo > "${log_dir}${log_channel}"
    cd ${script_dir}
    nohup python3 channelManager.py & > "${log_dir}${log_channel}"
    cd -
fi

if [[ ${siteswap} -eq 1 ]]
then
    echo "launch : siteswap"
    echo > "${log_dir}${log_siteswap}"
    cd ${script_dir}
    nohup python3 siteswap.py & > "${log_dir}${log_siteswap}"
    cd -
fi
