import sys
import os
import glob
import argparse
from collections import OrderedDict 

import ROOT
import VariableList
import SampleList

import datetime

ROOT.gROOT.SetBatch()
ROOT.gROOT.LoadMacro("./Helpers.h")

def main(sample_name):

  FileList = []
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
  ak4Systematics = []
  if "MC" in sample_name:
    isMC = True
    # ak4Systematics=[
    #   "jesTotalUp",
    #   "jesTotalDown",
    #   "jerUp"
    # ]

  #############################################
  #
  # Define columns
  #
  #############################################
  df = df.Define("passOS","lep0_charge * lep1_charge < 0.0")
  df = df.Define("passNJetSel","(nJetSel>=1)&&(nJetSelPt30Eta5p0<=1)&&(nJetSelPt20Eta2p4<=1)")
  if isMC:
    for syst in ak4Systematics:
      df = df.Define("passNJetSel_"+syst,"("+sys+"_nJetSel>=1)&&("+sys+"_nJetSelPt30Eta5p0<=1)&&("+sys+"_nJetSelPt20Eta2p4<=1)")

  #############################################
  #
  # Define Filters
  #
  #############################################
  df_filters = OrderedDict()
  df_filters["passOS"] = df.Filter("passOS")
  df_filters["passNJetSel"] = df_filters["passOS"].Filter("passNJetSel")
  if isMC:
    for syst in ak4Systematics:
      df_filters["passNJetSel_"+syst] = df_filters["passOS"].Filter("passNJetSel_"+syst)

  #############################################
  #
  # Snapshot tree
  #
  # TODO: Lazy snapshot seems to be not working
  # No output rootfile produced
  #############################################
  # 
  # snapshotOptions  = ROOT.ROOT.RDF.RSnapshotOptions()
  # snapshotOptions.fLazy = True
  #
  # Save at EOS
  #
  prefix=SampleList.EOSURL
  prefix+=SampleList.EOSDIR
  prefix+=SampleList.NTUPDIR
  #
  #
  #
  initialCount = df.Count()
  #
  # Save events with exactly one jet
  #
  outTreeName="Events"
  outTreeFileName = "%sntuple_%s.root" %(prefix,sample_name)
  print "Save tree %s in file %s" %(outTreeName,outTreeFileName)
  df_filters["passNJetSel"].Snapshot(outTreeName, outTreeFileName) 
  #
  # Do the same for MC with systematics
  #
  if isMC:
    for syst in ak4Systematics:
      outTreeName="Events_"+syst
      outTreeFileName = "%sntuple_%s_%s.root" %(prefix,sample_name,syst)
      print "Save tree %s in file %s" %(outTreeName,outTreeFileName)
      df_filters["passNJetSel_"+syst].Snapshot(outTreeName, outTreeFileName)

  print "Initial Events in Tree: ", initialCount.GetValue()

if __name__== "__main__":
  time_start = datetime.datetime.now()
  print("SkimNtuple.py::START::Time("+str(time_start)+")")

  parser = argparse.ArgumentParser("")
  parser.add_argument('-s', '--sample', type=str,  default="")
  parser.add_argument('-c', '--cores',  type=int,  default=4)

  args = parser.parse_args()
  print "sample = %s" %(args.sample)
  print "ncores = %d" %(args.cores)
 
  ROOT.ROOT.EnableImplicitMT(args.cores)
  main(args.sample)
 
  time_end = datetime.datetime.now()
  elapsed = time_end - time_start
  elapsed_str = str(datetime.timedelta(seconds=elapsed.seconds))
  print("SkimNtuple.py::DONE::Sample("+args.sample+")::Time("+str(time_end)+")::Elapsed("+elapsed_str+")")
