import sys
import os
import glob
import ROOT
from collections import OrderedDict 
import VariableList
import SampleList
ROOT.gROOT.SetBatch()
ROOT.gROOT.LoadMacro("./Helpers.h")

#
# Only on lxplus7
# source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.18.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh
#
EOSURL=SampleList.EOSURL
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
    FileList += [EOSURL+f for f in glob.glob(files)]
  
  # Creating std::vector as filelist holder to be plugged into RDataFrame
  vec = ROOT.vector('string')()

  for f in FileList:
    vec.push_back(f)

  # Read all files into RDataFrame
  df = ROOT.ROOT.RDataFrame(treeName, vec)
  isMC = False
  if "MC" in sample_name:
    isMC = True

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

  df = df.Define("jet0_dimuon_dphi_norm","DeltaPhiNorm(jet0_dimuon_dphi)")
  df = df.Define("jet0_dimuon_ptbalance","dimuon_pt/jet0_pt")
  if isMC:
    df = df.Define("passGenMatch","jet0_gen_match")
  #############################################
  #
  # Define Filters
  #
  #############################################
  df_filters  = OrderedDict()
  df_filters["passOS"] = df.Filter("mu0_charge * mu1_charge < 0.0")
  df_filters["passNJets1"] = df_filters["passOS"].Filter("nJetSel==1")

  #
  # Define jet0 eta bins
  #
  etaBins = OrderedDict()
  etaBins["eta0p0To1p479"] = "(fabs(jet0_eta) > 0.0)   && (fabs(jet0_eta) <= 1.479)"
  etaBins["eta1p479To2p4"] = "(fabs(jet0_eta) > 1.479) && (fabs(jet0_eta) <= 2.0)"
  etaBins["eta2p0To2p5"]   = "(fabs(jet0_eta) > 2.0)   && (fabs(jet0_eta) <= 2.5)"
  etaBins["eta2p5To2p75"]  = "(fabs(jet0_eta) > 2.5)   && (fabs(jet0_eta) <= 2.75)"
  etaBins["eta2p75To3p0"]  = "(fabs(jet0_eta) > 2.75)  && (fabs(jet0_eta) <= 3.00)"
  etaBins["eta3p0To5p0"]   = "(fabs(jet0_eta) > 3.0)   && (fabs(jet0_eta) <= 5.0)"

  #
  # Define jet0 pt bins
  #
  ptBins = OrderedDict()
  ptBins["pt20To30"]  = "(jet0_pt > 20.) && (jet0_pt <= 30.)"
  ptBins["pt30To40"]  = "(jet0_pt > 30.) && (jet0_pt <= 40.)"
  ptBins["pt40To50"]  = "(jet0_pt > 40.) && (jet0_pt <= 50.)"
  ptBins["pt50To60"]  = "(jet0_pt > 50.) && (jet0_pt <= 60.)"

  #
  # apply jet0 eta and pt cuts at the same time
  #
  binNames = []
  for eta in etaBins:
    for pt in ptBins:
      cutNameStr = "passNJets1_jet0_"+ eta + "_" + pt
      filterStr  = etaBins[eta] + " && " + ptBins[pt]
      df_filters[cutNameStr] =  df_filters["passNJets1"].Filter(filterStr)
      binNames.append(cutNameStr)
      #
      # Gen Matching requirement
      # FIKRI: We don't need these histograms for the dphi fits.
      #
      if isMC:
         #pass
	 cutNameStr = "passNJets1_jet0_"+ eta + "_" + pt +"_passGenMatch"
         filterStr  = etaBins[eta] + " && " + ptBins[pt] + " && (passGenMatch)"
         df_filters[cutNameStr] =  df_filters["passNJets1"].Filter(filterStr)
         binNames.append(cutNameStr)
         #fail
         cutNameStr = "passNJets1_jet0_"+ eta + "_" + pt +"_failGenMatch"
         filterStr  = etaBins[eta] + " && " + ptBins[pt] + " && (!passGenMatch)"
         df_filters[cutNameStr] =  df_filters["passNJets1"].Filter(filterStr)
         binNames.append(cutNameStr)
  
  #
  # Define PU Id cuts
  #
  puIDCuts = OrderedDict()
  puIDCuts["passPUIDLoose"]  = "(jet0_puId == 4)"
  puIDCuts["passPUIDMedium"] = "(jet0_puId == 6)"
  puIDCuts["passPUIDTight"]  = "(jet0_puId == 7)"
  puIDCuts["failPUIDLoose"]  = "(jet0_puId != 4)"
  puIDCuts["failPUIDMedium"] = "(jet0_puId != 6)"
  puIDCuts["failPUIDTight"]  = "(jet0_puId != 7)"

  #
  # Define pt balance cuts
  #
  ptBalanceCuts = OrderedDict()
  ptBalanceCuts["badBal"]  = "jet0_dimuon_ptbalance<0.5"
  ptBalanceCuts["goodBal"] = "(jet0_dimuon_ptbalance>=0.5) && (jet0_dimuon_ptbalance<1.5)"

  cutNames=[]
  for binName in binNames:
    #
    # apply ptBalance and puID at the same time
    #
    for ptBalCut in ptBalanceCuts:
      for puIDCut in puIDCuts:
        cutNameStr = binName + "_" + ptBalCut + "_" + puIDCut
        filterStr  = ptBalanceCuts[ptBalCut] + " && " + puIDCuts[puIDCut]
        df_filters[cutNameStr] = df_filters[binName].Filter(filterStr)
        cutNames.append(cutNameStr)

  ##############################################
  #
  # Define the cut levels that we want to make 
  # histograms
  #
  #############################################
  cutLevels = []
  cutLevels += cutNames

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
      # Some exceptions (why??? FIKRI: It only makes sense to make jet0 related histograms after requiring >=1 jets)
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

  numOfEvents = df.Count()
  print("Number of events in sample: %s " %numOfEvents.GetValue())
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

  timer.Stop()
  timer.Print()
  print("==============================")

if __name__== "__main__":
  #
  # Run over all samples
  #
  for sample_name in SampleList.Samples:
    main(sample_name)
  #
  # combine all data histos into one root file
  #
  os.system('hadd -f histos/Histo_Data16.root histos/Histo_Data16*_DoubleMuon.root')
