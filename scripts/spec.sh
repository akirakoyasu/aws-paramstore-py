#!/bin/bash
set -eu

here=$(cd $(dirname "$0") && pwd)
project_root=$(cd "${here}/.." && pwd)

set -x

echo "Test"
