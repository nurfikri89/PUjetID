import sys
import os
import glob
import ROOT
from collections import OrderedDict 
# import VariableList
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

# outFile = ROOT.TFile.Open(plotFileName,"RECREATE")
histDataFile = ROOT.TFile.Open('./histos/Histo_Data16.root', 'READ')
histMCFile = ROOT.TFile.Open('./histos/Histo_MC16_DY_AMCNLO.root', 'READ')

for key in ROOT.gDirectory.GetListOfKeys():
  dataHisto = histDataFile.Get( key.GetName() )
  mcHisto = histMCFile.Get( key.GetName() )
  canvas = ROOT.TCanvas("canvas_"+key.GetName(), "", 800, 800)
  canvas.Clear()

  # normalize MC to data
  nEventsData = dataHisto.Integral(0, 5000)
  nEventsMC = mcHisto.Integral(0, 5000)

  mcHisto.Scale(nEventsData/nEventsMC)

  pad1 = ROOT.TPad (" pad1 "," pad1 " ,0 ,0.3 ,1 ,1)
  pad1.Draw ()
  pad1.cd ()
  pad1.SetBottomMargin(0)

  # dataHisto.SetLineColor(ROOT.kBlack+1)
  # mcHisto.SetTitle("")
  mcHisto.GetXaxis().SetLabelSize(0)
  mcHisto.GetXaxis().SetTitleSize(0)
  mcHisto.GetYaxis().SetTitleSize(0.05)
  mcHisto.SetLineColor(ROOT.kRed+1)
  mcHisto.Draw("hist")

  dataHisto.SetMarkerColor(ROOT.kBlack)
  dataHisto.SetMarkerStyle(20)
  dataHisto.Draw("p same")

  if "dimuon_mass" in key.GetName():
  	mcHisto.SetMinimum(100)
  	mcHisto.SetMaximum(mcHisto.GetMaximum()*50)
  	pad1.SetLogy()

  canvas.cd()
  pad2 = ROOT.TPad(" pad2 "," pad2 " ,0 ,0.05 ,1 ,0.3)
  pad2.SetTopMargin(0)
  pad2.SetBottomMargin(0.25)
  pad2.Draw()
  pad2.cd()

  ratio = dataHisto.Clone()
  ratio.Divide(mcHisto)
  ratio.SetLineColor(ROOT.kBlack)
  ratio.SetTitle("")
  ratio.GetXaxis().SetLabelSize(0.12)
  ratio.GetXaxis().SetTitleSize(0.12)
  ratio.GetYaxis().SetLabelSize(0.1)
  ratio.GetYaxis().SetTitleSize(0.15)
  ratio.GetYaxis().SetTitle("Data/MC")
  ratio.GetYaxis().SetTitleOffset(0.3)
  ratio.GetYaxis().SetRangeUser(0.7,1.3)
  ratio.GetYaxis().SetNdivisions(207)
  ratio.Draw()
  pad2.Update()

  line = ROOT.TLine(pad2.GetUxmin(), 1, pad2.GetUxmax() ,1)
  line.SetLineColor(ROOT.kRed+1)
  line.SetLineWidth(2)
  line.Draw()
  ratio.Draw("same")

  canvas.Update()
  canvas.Print( "./png/"+key.GetName()+"plots.png")
  # canvas.Print( "./pdf/"+key.GetName()+"plots.pdf")

histDataFile.Close()
histMCFile.Close()
# outFile.Close()

