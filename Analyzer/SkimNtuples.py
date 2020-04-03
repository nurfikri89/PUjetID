import sys
import os
import glob
import argparse
from collections import OrderedDict 

import ROOT
import VariableList
import SampleList

ROOT.gROOT.SetBatch()
ROOT.gROOT.LoadMacro("./Helpers.h")

def main(sample_name):

  FileList = []
  for files in SampleList.Samples[sample_name].crabFiles:
    FileList += [SampleList.EOSURL+f for f in glob.glob(files)]
  
  # Creating std::vector as filelist holder to be plugged into RDataFrame
  vec = ROOT.vector('string')()

  for f in FileList:
    vec.push_back(f)
  
  # Read all files into RDataFrame
  df = ROOT.ROOT.RDataFrame("Events", vec)

  #############################################
  #
  # Define Filters
  #
  #############################################
  df_filters = OrderedDict()
  df_filters["passOS"] = df.Filter("mu0_charge * mu1_charge < 0.0")
  df_filters["passNJets1"] = df_filters["passOS"].Filter("nJetSel==1")

  #############################################
  #
  # Snapshot tree
  #
  #############################################
  #
  # Save at EOS
  #
  prefix=SampleList.EOSURL
  prefix+=SampleList.EOSJME
  prefix+=SampleList.NTUPDIR

  outTreeFileName = "%s/ntuple_%s.root" %(prefix,sample_name)
  print "Save ntuple at: ", outTreeFileName
  #
  # Save events with exactly one jet
  #
  df_filters["passNJets1"].Snapshot("Events", outTreeFileName)

if __name__== "__main__":
  timer = ROOT.TStopwatch()
  timer.Start()
  print("==============================")
  parser = argparse.ArgumentParser("")
  parser.add_argument('-s', '--sample', type=str,  default="")
  parser.add_argument('-c', '--cores',  type=int,  default=4)

  args = parser.parse_args()
  print "sample = %s" %(args.sample)
  print "ncores = %d" %(args.cores)

  ROOT.ROOT.EnableImplicitMT(args.cores)
  main(args.sample)

  timer.Stop()
  timer.Print()
  print("==============================")





