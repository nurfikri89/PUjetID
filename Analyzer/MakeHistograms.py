import sys
import os
import glob
import ROOT
from collections import OrderedDict 
import VariableList
ROOT.gROOT.SetBatch()
#
# Only on lxplus7
# source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.18.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh
#
EOSUSER="root://eosuser.cern.ch/"
treeName="Events"

ROOT.ROOT.EnableImplicitMT(8)

def main():
  # file to be read from
  INFILE=EOSUSER+"/eos/user/n/nbinnorj/CRABOUTPUT_JetPUId_DiMuonSkim_v0/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/JetPUId_MC16NanoAODv5_ext1-v1_DiMuonSkim_v0/191123_043755/0000/tree_1.root"

# how to read a file in RDataFrame
  df = ROOT.ROOT.RDataFrame(treeName, INFILE)
  numOfEvents = df.Count()
  print("Number of all events: %s " %numOfEvents.GetValue())
  
# branches to be read
    # br = var
  # cut1 = "mu0_mass < 60 && mu0_mass > 30"
  # df_filtered = df.Filter(cut1)
  # numOfEvents_filtered = df_filtered.Count()
  # print("Number of filtered events: %s" %numOfEvents_filtered.GetValue())
  
# create histogram dictionary
  Histograms = {}

  for varName in VariableList.Variables:
    var = VariableList.Variables[varName]
    print "Creating %s histogram." %var.varNameInTree
    Histograms[var.varNameInTree] = df.Histo1D((var.varNameInTree, var.varNameInTree, var.nbins, var.xmin, var.xmax), var.varNameInTree)
    # h_filtered = df_filtered.Histo1D((var.varNameInTree, var.varNameInTree, var.nbins, var.xmin, var.xmax), var.varNameInTree)

# Open a new ROOT file to store TH1
  f = ROOT.TFile('test.root', 'RECREATE')

# Loop over the Histograms dictionary and store TH1 in ROOT file
  for histName in Histograms:
    Histograms[histName].Write()
  
  f.Close()

if __name__== "__main__":
  main()

