import sys
import os
import glob
import ROOT
from collections import OrderedDict 
# import VariableList
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

if len ( sys.argv ) != 2:
  print " USAGE : %s <input file >"%( sys.argv[0])
  sys.exit (1)

histFileName = sys.argv[1]
# plotFileName = sys.argv[2]
# print " Reading from ", histFileName , "and writing to", plotFileName

# outFile = ROOT.TFile.Open(plotFileName,"RECREATE")
histFile = ROOT.TFile.Open(histFileName, 'READ')

for key in ROOT.gDirectory.GetListOfKeys():
  mcHisto = histFile.Get( key.GetName() )

  canvas = ROOT.TCanvas("canvas", "", 800, 800)
  # canvas.SetLogx(); canvas.SetLogy()
  # canvas.Print( plotFileName +"[")
  mcHisto.Draw("h")
  canvas.Print( "pdf/"+key.GetName()+"plots.pdf")
  # canvas.Print(plotFileName+"]")
  # canvas.Print(plotFileName)
  # mcHisto.Draw("pe")
  # canvas.Write(outFile)

histFile.Close()
# outFile.Close()

