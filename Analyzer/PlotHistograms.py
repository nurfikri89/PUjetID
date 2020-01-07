import os
import ROOT
# from collections import OrderedDict 
# import VariableList
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

def main(DataFileName, MCFileName):
  # open histogram files
  histDataFile = ROOT.TFile.Open("./histos/"+DataFileName+".root", 'READ')
  histMCFile = ROOT.TFile.Open("./histos/"+MCFileName+".root", 'READ')

  # loop over every object inside the histogram files
  # for key in ROOT.gDirectory.GetListOfKeys():
  for key in histDataFile.GetListOfKeys():

    dataHisto = histDataFile.Get( key.GetName() )
    mcHisto = histMCFile.Get( key.GetName() )
    
    canvas = ROOT.TCanvas("c_"+MCFileName+"_"+key.GetName(), "", 800, 800)
    canvas.Clear()
  
    # normalize MC to data
    nEventsData = dataHisto.Integral(0, 5000)
    nEventsMC = mcHisto.Integral(0, 5000)
    mcHisto.Scale(nEventsData/nEventsMC)
  
    pad1 = ROOT.TPad ("pad1 "," pad1 " ,0 ,0.3 ,1 ,1)
    pad1.Draw ()
    pad1.cd ()
    pad1.SetBottomMargin(0)
  
    # plot MC vs data histogram
    mcHisto.SetTitle("")
    mcHisto.GetXaxis().SetLabelSize(0)
    mcHisto.GetXaxis().SetTitleSize(0)
    mcHisto.GetYaxis().SetTitleSize(0.05)
    mcHisto.GetYaxis().SetTitle("Number of events")
    mcHisto.GetYaxis().SetTitleOffset(1.0)
    mcHisto.SetLineWidth(2)
    mcHisto.SetLineColor(ROOT.kRed+1)
    mcHisto.Draw("hist")
  
    dataHisto.SetMarkerColor(ROOT.kBlack)
    dataHisto.SetMarkerStyle(20)
    dataHisto.Draw("p same")

    maxMC = mcHisto.GetMaximum()
    maxData = dataHisto.GetMaximum()

    if maxMC > maxData:
      mcHisto.SetMaximum(maxMC*1.2)
    else:
      mcHisto.SetMaximum(maxData*1.2)
  
    if "dimuon_mass" in key.GetName():
      mcHisto.SetMinimum(100)
      mcHisto.SetMaximum(mcHisto.GetMaximum()*50)
      pad1.SetLogy()
  
    legend = ROOT.TLegend(0.8 ,0.75 , 0.90 , 0.85)
    if MCFileName == "Histo_MC16_DY_AMCNLO":
      legend.AddEntry( mcHisto , "AMCNLO")
    elif MCFileName == "Histo_MC16_DY_MG":
      legend.AddEntry( mcHisto, "MG")
    legend.AddEntry( dataHisto , "2016 Data")
    legend.SetTextSize(0.02)
    legend.SetLineWidth(0)
    legend.Draw(" same ")

    canvas.cd()
    pad2 = ROOT.TPad(" pad2 "," pad2 " ,0 ,0.05 ,1 ,0.3)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.25)
    pad2.Draw()
    pad2.cd()
    
    # ratio plot
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

    if MCFileName == "Histo_MC16_DY_AMCNLO":
      outDir = './Data16_VS_AMCNLO/'
      if not(os.path.isdir(outDir)): os.mkdir(outDir)
      # canvas.Print( outDir+key.GetName()+".png")
      canvas.Print( outDir+key.GetName()+".pdf")

    elif MCFileName == "Histo_MC16_DY_MG":
      outDir = './Data16_VS_MG/'
      if not(os.path.isdir(outDir)): os.mkdir(outDir)
      # canvas.Print( outDir+key.GetName()+".png")
      canvas.Print( outDir+key.GetName()+".pdf")     
  
  histDataFile.Close()
  histMCFile.Close()

if __name__=="__main__":
  main("Histo_Data16","Histo_MC16_DY_MG")
  # main("Histo_Data16","Histo_MC16_DY_AMCNLO")
