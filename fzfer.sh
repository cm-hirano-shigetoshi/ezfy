#!/usr/bin/env bash
set -eu
readonly YAML=$1
shift

readonly PYTHON=/usr/bin/python
readonly TOOLDIR=$(dirname $(readlink -e $0))
set +u
perl <( \
  ${PYTHON} ${TOOLDIR}/creator.py ${TOOLDIR}/template.pl \
  <(cat ${YAML} | sed \
      -e "s\`\${1}\`$1\`g" \
      -e "s\`\${2}\`$2\`g" \
      -e "s\`\${3}\`$3\`g" \
      -e "s\`\${4}\`$4\`g" \
      -e "s\`\${5}\`$5\`g" \
      -e "s\`\${6}\`$6\`g" \
      -e "s\`\${7}\`$7\`g" \
      -e "s\`\${8}\`$8\`g" \
      -e "s\`\${9}\`$9\`g" \
  ) | tee ~/.debug \
)

