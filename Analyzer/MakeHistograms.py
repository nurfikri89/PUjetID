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
    FileList += [EOSUSER+f for f in glob.glob(files)]
  
  # Creating std::vector as filelist holder to be plugged into RDataFrame
  vec = ROOT.vector('string')()

  for f in FileList:
    vec.push_back(f)

  # Read all files into RDataFrame
  df = ROOT.ROOT.RDataFrame(treeName, vec)
  numOfEvents = df.Count()
  print("Number of events in sample: %s " %numOfEvents.GetValue())

  #############################################
  #
  # Define variables
  #
  #############################################
  # Define evtWeight variable
  if "Data" in sample_name:
    df = df.Define("evtWeight","1.0")
  else: #For MC
    df = df.Define("evtWeight","genWeight")
  # Define name for event weight
  weightName = "evtWeight"

  #############################################
  #
  # Define Filters
  #
  #############################################
  df_filters  = OrderedDict()
  df_filters["passOS"] = df.Filter("mu0_charge * mu1_charge < 0.0")
  df_filters["passOS_passNJets1"] = df_filters["passOS"].Filter("nJetSel==1")

  ##############################################
  #
  # Define the cut levels that we want to make 
  # histograms
  #
  #############################################
  cutLevels = []
  cutLevels += [
    "passOS",
    "passOS_passNJets1",
  ]

  ##############################################
  #
  # Make the histograms
  #
  #############################################
  # Create histogram dictionary
  Histograms = {}
  
  #
  # Loop over cutLevels
  #
  for cutLevel in cutLevels:
    #
    # Loop over histograms
    #
    for varName in VariableList.Variables:
      var = VariableList.Variables[varName]
      #
      # Some exceptions (why???)
      #
      if "jet0" in varName:
        if "passNJets1" not in cutLevel:
          continue
      #
      # Define full name for histogram
      #
      histoNameFinal  = "h_%s_%s" %(cutLevel,varName)
      Histograms[histoNameFinal] = df_filters[cutLevel].Histo1D((histoNameFinal, histoNameFinal+";"+var.xAxisName, var.nbins, var.xmin, var.xmax), var.varNameInTree,weightName)
      print ("Creating histo: %s" %histoNameFinal)

  ##############################################
  #
  # Save histograms in output rootfile
  #
  #############################################
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

  # combine all data histos into one root file
  os.system('hadd -f histos/Histo_Data16.root histos/Histo_Data16*_DoubleMuon.root')

  timer.Stop()
  timer.Print()
  print("==============================")

if __name__== "__main__":
  for sample_name in SampleList.Samples:
    main(sample_name)

