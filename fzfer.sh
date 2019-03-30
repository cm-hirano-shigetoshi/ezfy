#!/usr/bin/env bash
set -eu
readonly YAML=$1

readonly PYTHON=/usr/bin/python
readonly TOOLDIR=$(dirname $(readlink -e $0))
perl <(${PYTHON} ${TOOLDIR}/creator.py ${TOOLDIR}/template.pl ${YAML} | tee ~/.debug)

