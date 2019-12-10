import sys
import os
import glob
import ROOT
from collections import OrderedDict 
import VariableList
import SampleList
ROOT.gROOT.SetBatch()
#
# Only on lxplus7
# source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.18.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh
#
EOSUSER="root://eosuser.cern.ch/"
treeName="Events"

ROOT.ROOT.EnableImplicitMT(8)

def main(sample_name):
  timer = ROOT.TStopwatch()
  timer.Start()
  print("==============================")
  print("Running %s" %sample_name)

  FileList = []
  for files in SampleList.Samples[sample_name].files:
    # print("Processing %s" %files)
    FileList += glob.glob(files)
  
  # Creating std::vector as filelist holder to be plugged into RDataFrame
  vec = ROOT.vector('string')()

  for f in FileList:
    vec.push_back(f)

  # Read all files into RDataFrame
  df = ROOT.ROOT.RDataFrame(treeName, vec)
  numOfEvents = df.Count()
  print("Number of events in sample: %s " %numOfEvents.GetValue())
  
  # Create histogram dictionary
  Histograms = {}

  #making histogram
  for varName in VariableList.Variables:
    var = VariableList.Variables[varName]
    print ("Creating %s histogram." %var.varNameInTree)
    Histograms[var.varNameInTree] = df.Histo1D((var.varNameInTree, var.varNameInTree, var.nbins, var.xmin, var.xmax), var.varNameInTree)
    # h_filtered = df_filtered.Histo1D((var.varNameInTree, var.varNameInTree, var.nbins, var.xmin, var.xmax), var.varNameInTree)
  
  #
  # Create histos directory
  #
  outDir = './histos/'
  if not(os.path.isdir(outDir)):
    os.mkdir(outDir)

  # Open a new ROOT file to store TH1
  outFileName = outDir+"Histo_"+sample_name+'.root'
  f = ROOT.TFile(outFileName, 'RECREATE')

  # Loop over the Histograms dictionary and store TH1 in ROOT file
  for histName in Histograms:
    Histograms[histName].Write()

  f.Close()
  print("Histos saved in %s" %outFileName)
  timer.Stop()
  timer.Print()
  print("==============================")

if __name__== "__main__":
  for sample_name in SampleList.Samples:
    main(sample_name)

