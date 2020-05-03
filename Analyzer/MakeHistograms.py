import sys
import os
import glob
import argparse
from collections import OrderedDict 
import datetime

import ROOT
import VariableList
import SampleList

ROOT.gROOT.SetBatch()
ROOT.gROOT.LoadMacro("./Helpers.h")

#
#
varNamesToPlot = [
  "jetSel0_dilep_dphi_norm"
]

def main(sample_name, useSkimNtuples):

  FileList = []

  if useSkimNtuples:
    print "Globbing File Paths:"
    for files in SampleList.Samples[sample_name].ntupleFiles:
      print files
      FileList += [SampleList.EOSURL+f for f in glob.glob(files)]
  else:
    print "Globbing File Paths:"
    for files in SampleList.Samples[sample_name].crabFiles:
      print files
      FileList += [SampleList.EOSURL+f for f in glob.glob(files)]
  
  # Creating std::vector as filelist holder to be plugged into RDataFrame
  vec = ROOT.vector('string')()

  for f in FileList:
    vec.push_back(f)

  # Read all files into RDataFrame
  df = ROOT.ROOT.RDataFrame("Events", vec)
  isMC = False
  if "MC" in sample_name:
    isMC = True

  #############################################
  #
  # Set columns in RDataFrame
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
  # Define columns
  #
  #############################################
  if not useSkimNtuples:
    df = df.Define("passOS","lep0_charge * lep1_charge < 0.0")
    df = df.Define("passNJetSel","(nJetSelPt30Eta5p0<=1)&&(nJetSelPt30Eta5p0<=1)")
    if isMC:
      for syst in ak4Systematics:
        df = df.Define("passNJetSel_"+syst,"("+sys+"_nJetSelPt30Eta5p0<=1)&&("+sys+"_nJetSelPt30Eta5p0<=1)") 

  df = df.Define("jetSel0_dilep_dphi_norm","DeltaPhiNorm(jetSel0_dilep_dphi)")
  df = df.Define("jetSel0_dilep_ptbalance","dilep_pt/jetSel0_pt")
  if isMC:
    df = df.Define("passGenMatch","jetSel0_gen_match")
  #############################################
  #
  # Define Filters
  #
  #############################################
  df_filters  = OrderedDict()
  df_filters["passOS"] = df.Filter("passOS")
  df_filters["passNJetSel"] = df_filters["passOS"].Filter("passNJetSel")
  #
  # Define jetSel0 eta bins
  #
  etaBins = OrderedDict()
  # Abs(eta)
  etaBins["abseta0p0To1p479"] = "(fabs(jetSel0_eta) > 0.0)   && (fabs(jetSel0_eta) <= 1.479)"
  etaBins["abseta1p479To2p0"] = "(fabs(jetSel0_eta) > 1.479) && (fabs(jetSel0_eta) <= 2.0)"
  etaBins["abseta2p0To2p5"]   = "(fabs(jetSel0_eta) > 2.0)   && (fabs(jetSel0_eta) <= 2.5)"
  etaBins["abseta2p5To2p75"]  = "(fabs(jetSel0_eta) > 2.5)   && (fabs(jetSel0_eta) <= 2.75)"
  etaBins["abseta2p75To3p0"]  = "(fabs(jetSel0_eta) > 2.75)  && (fabs(jetSel0_eta) <= 3.00)"
  etaBins["abseta3p0To5p0"]   = "(fabs(jetSel0_eta) > 3.0)   && (fabs(jetSel0_eta) <= 5.0)"
  # positive eta
  etaBins["eta0p0Topos1p479"]    = "(jetSel0_eta > 0.0)    && (jetSel0_eta <= 1.479)"
  etaBins["etapos1p479Topos2p0"] = "(jetSel0_eta > 1.479)  && (jetSel0_eta <= 2.0)"
  etaBins["etapos2p0Topos2p5"]   = "(jetSel0_eta > 2.0)    && (jetSel0_eta <= 2.5)"
  etaBins["etapos2p5Topos2p75"]  = "(jetSel0_eta > 2.5)    && (jetSel0_eta <= 2.75)"
  etaBins["etapos2p75Topos3p0"]  = "(jetSel0_eta > 2.75)   && (jetSel0_eta <= 3.00)"
  etaBins["etapos3p0Topos5p0"]   = "(jetSel0_eta > 3.0)    && (jetSel0_eta <= 5.0)"
  # negative eta
  etaBins["etaneg1p479To0p0"]    = "(jetSel0_eta < 0.0)    && (jetSel0_eta >= -1.479)"
  etaBins["etaneg2p0Toneg1p479"] = "(jetSel0_eta < -1.479) && (jetSel0_eta >= -2.0)"
  etaBins["etaneg2p5Toneg2p0"]   = "(jetSel0_eta < -2.0)   && (jetSel0_eta >= -2.5)"
  etaBins["etaneg2p75Toneg2p5"]  = "(jetSel0_eta < -2.5)   && (jetSel0_eta >= -2.75)"
  etaBins["etaneg3p0Toneg2p75"]  = "(jetSel0_eta < -2.75)  && (jetSel0_eta >= -3.00)"
  etaBins["etaneg5p0Toneg3p0"]   = "(jetSel0_eta < -3.0)   && (jetSel0_eta >= -5.0)"

  #
  # Define jetSel0 pt bins
  #
  ptBins = OrderedDict()
  ptBins["pt20To30"]  = "(jetSel0_pt > 20.) && (jetSel0_pt <= 30.)"
  ptBins["pt30To40"]  = "(jetSel0_pt > 30.) && (jetSel0_pt <= 40.)"
  ptBins["pt40To50"]  = "(jetSel0_pt > 40.) && (jetSel0_pt <= 50.)"
  ptBins["pt50To60"]  = "(jetSel0_pt > 50.) && (jetSel0_pt <= 60.)"

  #
  # apply jetSel0 eta and pt cuts at the same time
  #
  binNames = []
  for eta in etaBins:
    for pt in ptBins:
      cutNameStr = "passNJetSel_jetSel0_"+ eta + "_" + pt
      filterStr  = etaBins[eta] + " && " + ptBins[pt]
      df_filters[cutNameStr] =  df_filters["passNJetSel"].Filter(filterStr)
      binNames.append(cutNameStr)
      #
      # Gen Matching requirement
      #
      if isMC:
        #
        # Pass
        #
        cutNameStr = "passNJetSel_jetSel0_"+ eta + "_" + pt +"_passGenMatch"
        filterStr  = etaBins[eta] + " && " + ptBins[pt] + " && (passGenMatch)"
        df_filters[cutNameStr] =  df_filters["passNJetSel"].Filter(filterStr)
        binNames.append(cutNameStr)
        #
        # Fail
        #
        cutNameStr = "passNJetSel_jetSel0_"+ eta + "_" + pt +"_failGenMatch"
        filterStr  = etaBins[eta] + " && " + ptBins[pt] + " && (!passGenMatch)"
        df_filters[cutNameStr] =  df_filters["passNJetSel"].Filter(filterStr)
        binNames.append(cutNameStr)

  #
  # Define PU Id cuts
  # Guide on how to read the puID bitmap variable: 
  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID#miniAOD_and_nanoAOD
  #
  puIDCuts = OrderedDict()
  puIDCuts["passPUIDLoose"]  = "(jetSel0_puId & (1 << 2))"
  puIDCuts["passPUIDMedium"] = "(jetSel0_puId & (1 << 1))"
  puIDCuts["passPUIDTight"]  = "(jetSel0_puId & (1 << 0))"
  puIDCuts["failPUIDLoose"]  = "!(jetSel0_puId & (1 << 2))"
  puIDCuts["failPUIDMedium"] = "!(jetSel0_puId & (1 << 1))"
  puIDCuts["failPUIDTight"]  = "!(jetSel0_puId & (1 << 0))"

  #
  # Define pt balance cuts
  #
  ptBalanceCuts = OrderedDict()
  ptBalanceCuts["badBal"]  = "jetSel0_dilep_ptbalance<0.5"
  ptBalanceCuts["goodBal"] = "(jetSel0_dilep_ptbalance>=0.5) && (jetSel0_dilep_ptbalance<1.5)"

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
  Histograms = OrderedDict()
  #
  # Loop over cutLevels
  #
  for cutLevel in cutLevels:
    #
    # Loop over variables to plot
    #
    for varName in varNamesToPlot:
      var = VariableList.Variables[varName]
      #
      # Some exceptions 
      #
      if "jetSel0" in varName and "passNJetSel" not in cutLevel: continue
      #
      # Define full name for histogram
      #
      histoNameFinal  = "h_%s_%s" %(cutLevel,varName)
      print histoNameFinal
      histoInfo = (histoNameFinal, histoNameFinal+";"+var.xAxis+";"+var.yAxis, var.nbins, var.xmin, var.xmax)
      Histograms[histoNameFinal] = df_filters[cutLevel].Histo1D(histoInfo, var.varNameInTree, weightName)
      # print ("Creating histo: %s" %histoNameFinal)

  print("Number of histos: %s " %len(Histograms))
  numOfEvents = df.Count()
  print("Number of events in sample: %s " %numOfEvents.GetValue())

  ##############################################
  #
  # Save histograms in output rootfile
  #
  #############################################
  #
  # Create directory for output
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

if __name__== "__main__":
  time_start = datetime.datetime.now()
  print("MakeHistograms.py::START::Time("+str(time_start)+")")

  parser = argparse.ArgumentParser("")
  parser.add_argument('--sample',         dest='sample',         type=str,  default="")
  parser.add_argument('--cores',          dest='cores',          type=int,  default=4)
  parser.add_argument('--useSkimNtuples', dest='useSkimNtuples', action='store_true')

  args = parser.parse_args()
  print "sample = %s" %(args.sample)
  print "ncores = %d" %(args.cores)
  print "useSkimNtuples = %r" %(args.useSkimNtuples)

  ROOT.ROOT.EnableImplicitMT(args.cores)
  main(args.sample,args.useSkimNtuples)

  time_end = datetime.datetime.now()
  elapsed = time_end - time_start
  elapsed_str = str(datetime.timedelta(seconds=elapsed.seconds))
  print("MakeHistograms.py::DONE::Sample("+args.sample+")::Time("+str(time_end)+")::Elapsed("+elapsed_str+")")
