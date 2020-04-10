#!/bin/bash

cd /afs/cern.ch/user/n/nbinnorj/work/AnaPUJetID_cmsjet/CMSSW_10_2_18/src/PUjetID/Analyzer
source ./sourceRecentROOT.sh
#
python SkimNtuples.py --sample ${1} --cores ${2}
python MakeHistograms.py --sample ${1} --cores ${2}
