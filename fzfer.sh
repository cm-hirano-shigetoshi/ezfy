#!/usr/bin/env bash
set -eu
readonly SUBCMD=$1
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
readonly TOOLDIR=$(dirname $(readlink_e $0))

if [[ "${SUBCMD}" = "run" ]]; then
  readonly YAML=$1
  shift
  perl <(python ${TOOLDIR}/creator.py ${TOOLDIR}/template.pl ${YAML}) "$@"
elif [[ "${SUBCMD}" = "debug" ]]; then
  readonly YAML=$1
  shift
  python ${TOOLDIR}/creator.py ${TOOLDIR}/template.pl ${YAML}
elif [[ "${SUBCMD}" = "preview" ]]; then
  readonly FILE=$1
  shift
  ${TOOLDIR}/preview/${FILE} "$@"
fi
