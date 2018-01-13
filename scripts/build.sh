#!/bin/bash
set -eu

here=$(cd $(dirname "$0") && pwd)
project_root=$(cd "${here}/.." && pwd)

required() {
  local subject=$1

  if ! type "${subject}" > /dev/null 2>&1; then
    echo "missing required: ${subject}"
    return 1
  fi
}

required_py() {
  local subject=$1

  if ! pip3 show "${subject}" > /dev/null 2>&1; then
    echo "missing required python package: ${subject}"
    return 1
  fi
}

md2rst() {
  pandoc "${project_root}/README.md" \
    --from=markdown \
    --to=rst \
    --standalone \
    --output="${project_root}/README.rst"
}

build() {
  cd "${project_root}"
  python3 setup.py clean --all bdist_wheel
  cd -
}

required pandoc
required_py wheel

set -x

md2rst
build
