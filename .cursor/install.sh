#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
  else
    echo "python3 is required but could not be installed automatically." >&2
    exit 1
  fi
fi

if ! python3 -m pip --version >/dev/null 2>&1; then
  python3 -m ensurepip --upgrade
fi

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install --upgrade -r requirements-dev.txt
