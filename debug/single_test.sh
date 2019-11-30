set -eu

single_test() {
  all="$@"
  input="$1"; shift
  answer="$1"; shift
  result=$(echo "$input" | $(dirname $0)/../main/single.py "$@")
  if [[ "$result" != "$answer" ]]; then
    echo "[31m$all => '$result'[00m"
    exit 1
  fi
}

range_test() {
  all="$@"
  input="$1"; shift
  answer="$1"; shift
  result=$(echo "$input" | $(dirname $0)/../main/range.py "$@")
  if [[ "$result" != "$answer" ]]; then
    echo "[31m$all => '$result'[00m"
    exit 1
  fi
}

single_test "  aaa  bbb  ccc  " "aaa" 1
single_test "  aaa  bbb  ccc  " "ccc" -1
single_test "\t\taaa  bbb  ccc  " "bbb" 2
single_test "  aaa: bbb :ccc  " " bbb " 2 -F :
single_test "  aaa: bbb :ccc  " "  aaa" -3 -F :

range_test "  aaa  bbb  ccc  " "aaa  bbb  ccc" 1 -1
range_test "  aaa  bbb  ccc  " "aaa  bbb" 1 2
range_test "  aaa  bbb  ccc  " "aaa  bbb" 1 -2
range_test "\t\taaa\t \tbbb  ccc  " "aaa\t \tbbb" 1 -2
range_test "  aaa: bbb :ccc  " "aaa: bbb" 1 2 -F :
range_test "  aaa: bbb :ccc  " "aaa" 1 -3 -F :
range_test "  aaa: bbb :ccc  " "aaa: bbb :ccc" 1 -1 -F :
range_test "  aaa] bbb ]ccc  " "aaa] bbb" 1 -2 -F ']'
range_test "  aaa  bbb  ccc  " "" -1 2

