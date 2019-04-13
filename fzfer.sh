#!/usr/bin/env bash
set -eu
readonly YAML=$1
shift

readonly PYTHON=/usr/bin/python
readonly TOOLDIR=$(dirname $(readlink -e $0))
set +u
perl <( \
  ${PYTHON} ${TOOLDIR}/creator.py ${TOOLDIR}/template.pl \
  <(cat ${YAML} | sed -e "s\`\${\([1-9]\)}\`\$arg\1\`g") | tee ~/.debug \
) "$@"

