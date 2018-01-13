#!/bin/bash
set -eu

here=$(cd $(dirname "$0") && pwd)
project_root=$(cd "${here}/.." && pwd)

spec() {
  cd "${project_root}"
  python3 setup.py test
  cd -
}

set -x

spec
