import sys
import os
import glob
import ROOT
from collections import OrderedDict 

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
  br = "dimuon_mass"
  cut1 = "dimuon_mass < 95 && dimuon_mass > 85"
  df_filtered = df.Filter(cut1)
  numOfEvents_filtered = df_filtered.Count()
  print("Number of filtered events: %s" %numOfEvents_filtered.GetValue())

  h = df.Histo1D(("Dimuon_mass", "Dimuon_mass", 80, 70, 110), br)
  h_filtered = df_filtered.Histo1D(("Dimuon_mass", "Dimuon_mass", 80, 70, 110), br)

  # Produce plot
  ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
  c = ROOT.TCanvas("c", "", 800, 800)
  c.SetLogx(); c.SetLogy()
  h.SetTitle("")
  h.GetXaxis().SetTitle("m_{#mu#mu} (GeV)"); h.GetXaxis().SetTitleSize(0.04)
  h.GetYaxis().SetTitle("N_{Events}"); h.GetYaxis().SetTitleSize(0.04)
  h.SetLineColor(ROOT.kRed+1)
  h_filtered.SetTitle("")
  h_filtered.GetXaxis().SetTitle("m_{#mu#mu} (GeV)"); h.GetXaxis().SetTitleSize(0.04)
  h_filtered.GetYaxis().SetTitle("N_{Events}"); h.GetYaxis().SetTitleSize(0.04)
  h_filtered.SetLineColor(ROOT.kBlue+1)
  h.Draw("HIST")
  h_filtered.Draw("HIST SAME")
  
  c.SaveAs("dimuon_spectrum.pdf")


if __name__== "__main__":
  main()

