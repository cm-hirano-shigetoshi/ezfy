#!/usr/bin/env bash
set -eu
readonly YAML=$1

readonly PYTHON=/usr/bin/python
readonly TOOLDIR=$(dirname $(readlink -e $0))
${PYTHON} ${TOOLDIR}/creator.py ${TOOLDIR}/template.pl ${YAML} | perl

