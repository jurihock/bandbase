#!/bin/bash

BANDBASE=$(dirname "$(readlink -f "$0")")

python3 $BANDBASE/main.py
