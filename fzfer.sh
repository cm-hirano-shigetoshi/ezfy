#!/usr/bin/env bash
set -eu
readonly YAML=$1
shift

function readlink_e() {
  local p
  if ! p=$(readlink -e "$1" 2>/dev/null); then
    p="$1"
    while [[ -L "$p" ]]; do
      p=$(readlink "$p")
    done
  fi
  echo $p
}

readonly PYTHON=/usr/bin/python
readonly TOOLDIR=$(dirname $(readlink_e $0))
perl <(${PYTHON} ${TOOLDIR}/creator.py ${TOOLDIR}/template.pl ${YAML} | tee ~/.debug) "$@"

