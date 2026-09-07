#!/bin/bash
set -e
export LD_LIBRARY_PATH=/cvmfs/sft.cern.ch/lcg/views/LCG_104c/x86_64-el9-gcc13-opt/lib64:$LD_LIBRARY_PATH
./gain_MC "$1" "$2"