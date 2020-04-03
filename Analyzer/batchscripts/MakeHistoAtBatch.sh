#!/bin/bash

cd REPLACEME
source ./sourceRecentROOT.sh
#
#
python MakeHistograms.py --sample ${1} --cores ${2}
#
#
# python SkimNtuples.py --sample ${1} --cores ${2}
