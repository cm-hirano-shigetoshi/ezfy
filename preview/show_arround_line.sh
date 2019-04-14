#!/usr/bin/bash

readonly FILE=$1
readonly LINE=$2
readonly HEIGHT=$3
readonly BOTTOM_MARGIN_PARCENT=30

start_line=$((${LINE} - ${HEIGHT} + 1))
start_line=$((${start_line} + $((${HEIGHT} * ${BOTTOM_MARGIN_PARCENT}/100))))
if [[ $start_line -le 0 ]]; then
  start_line=1
fi

cat ${FILE} \
  | sed -e "${LINE}s/^/[1;33m/" -e "${LINE}s/$/[0m/" \
  | tail -n +${start_line}

