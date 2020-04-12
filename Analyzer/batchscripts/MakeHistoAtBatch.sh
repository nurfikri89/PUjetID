#!/bin/bash

cd REPLACEME
source ./sourceRecentROOT.sh

python SkimNtuples.py --sample ${1} --cores ${2}
python MakeHistograms.py --sample ${1} --cores ${2} --useSkimNtuples

# python MakeHistograms.py --sample ${1} --cores ${2}
