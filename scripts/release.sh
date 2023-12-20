#!/bin/bash
set -euo pipefail

if [ -z ${NO_DATABASE} ]; then
   echo "NO_DATABASE is set, skipping database setup"
   exit 1
fi
