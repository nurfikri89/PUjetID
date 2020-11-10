from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import os
import math
import array
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

class PUIDCalculator(Module):
  def __init__(self, era, jetBranchName):
    self.era = era
    self.jetBranchName = jetBranchName
    self.lenVar = "n"+self.jetBranchName
    self.minJetPt = 15.
    self.tmvaWeightsPath = os.environ['CMSSW_BASE']+"/src/PUjetID/Skimmer/data/mvaWeights/"
    #
    # TMVA BDT weights
    #
    self.tmvaWeightFilenames = []
    # UL 2017 training weights
    if self.era == "UL2017":
      self.tmvaWeightFilenames = [
        self.tmvaWeightsPath+"pileupJetId_UL17_Eta0p0To2p5_chs_BDT.weights.xml",
        self.tmvaWeightsPath+"pileupJetId_UL17_Eta2p5To2p75_chs_BDT.weights.xml",
        self.tmvaWeightsPath+"pileupJetId_UL17_Eta2p75To3p0_chs_BDT.weights.xml",
        self.tmvaWeightsPath+"pileupJetId_UL17_Eta3p0To5p0_chs_BDT.weights.xml",
      ]
    #
    #
    #
    self.eta_bins = [
      "Eta0p0To2p5",
      "Eta2p5To2p75",
      "Eta2p75To3p0",
      "Eta3p0To5p0"
    ]
    #
    # Define variables to be provided to TMVA::Reader
    #
    self.tmva_v_nvtx       = array.array("f", [-999.])
    self.tmva_v_beta       = array.array("f", [-999.])
    self.tmva_v_dR2Mean    = array.array("f", [-999.])
    self.tmva_v_frac01     = array.array("f", [-999.])
    self.tmva_v_frac02     = array.array("f", [-999.])
    self.tmva_v_frac03     = array.array("f", [-999.])
    self.tmva_v_frac04     = array.array("f", [-999.])
    self.tmva_v_majW       = array.array("f", [-999.])
    self.tmva_v_minW       = array.array("f", [-999.])
    self.tmva_v_jetR       = array.array("f", [-999.])
    self.tmva_v_jetRchg    = array.array("f", [-999.])
    self.tmva_v_nParticles = array.array("f", [-999.])
    self.tmva_v_nCharged   = array.array("f", [-999.])
    self.tmva_v_ptD        = array.array("f", [-999.])
    self.tmva_v_pull       = array.array("f", [-999.])
    # NOTE: It is important that this list follows
    # the order of the variables as in the tmva weights
    # files
    self.tmva_variables = [
      ("nvtx" ,       self.tmva_v_nvtx),
      ("beta",        self.tmva_v_beta),
      ("dR2Mean",     self.tmva_v_dR2Mean),
      ("frac01",      self.tmva_v_frac01),
      ("frac02",      self.tmva_v_frac02),
      ("frac03",      self.tmva_v_frac03),
      ("frac04",      self.tmva_v_frac04),
      ("majW",        self.tmva_v_majW),
      ("minW",        self.tmva_v_minW),
      ("jetR",        self.tmva_v_jetR),
      ("jetRchg",     self.tmva_v_jetRchg),
      ("nParticles",  self.tmva_v_nParticles),
      ("nCharged",    self.tmva_v_nCharged),
      ("ptD",         self.tmva_v_ptD),
      ("pull",        self.tmva_v_pull),
    ]
    self.tmva_s_jetPt  = array.array("f", [-999])
    self.tmva_s_jetEta = array.array("f", [-999])
    self.tmva_spectators = [
      ("jetPt",  self.tmva_s_jetPt),
      ("jetEta", self.tmva_s_jetEta),
    ]

    self.tmva_readers = []
    if len(self.eta_bins) == len(self.tmvaWeightFilenames):
      #
      # For each etaBin, setup a TMVA::Reader
      #
      for i, eta_bin in enumerate(self.eta_bins):
        #
        # Initialize TMVA::Reader
        #
        self.tmva_readers.append(ROOT.TMVA.Reader("!Color:!Silent"))
        #
        # Add spectator variables
        #
        for spec_name, spec_address in self.tmva_spectators:
          self.tmva_readers[i].AddSpectator(spec_name, spec_address)
        #
        # Add training variables
        #
        for var_name, var_address in self.tmva_variables: 
          # For the last eta bin, we don't use the following
          # variables.
          if eta_bin == "Eta3p0To5p0":
            if var_name == "beta": continue
            if var_name == "jetRchg": continue
            if var_name == "nCharged": continue
          self.tmva_readers[i].AddVariable(var_name, var_address)
        #
        # Book BDT
        #
        self.tmva_readers[i].BookMVA("BDT", self.tmvaWeightFilenames[i])
    else:
      raise ValueError("ERROR: eta_bins length not the same as tmvaWeightFilenames length. Please check!")

  def beginJob(self,histFile=None,histDirName=None):
    Module.beginJob(self)

  def endJob(self):
    Module.endJob(self)
    print "PUIDCalculator module ended successfully"
    pass

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch("Jet_puIdDiscOTF","F",lenVar=self.lenVar) # OTF here means on-the-fly

  def analyze(self, event):

    jets = Collection(event, self.jetBranchName)
    
    #============================================================
    #
    #
    #
    #============================================================
    jets_puIdDiscOTF = []

    for iJet, jet in enumerate(jets):
      jet_pt = jet.pt
      jet_eta = jet.eta
      jet_puIdDiscOTF = -9.
      
      #
      # Let us just calculate BDT for jets with pt > 15 GeV.
      # In NanoAOD JME, there are a LOT of low pt jets.
      #
      if jet_pt > self.minJetPt:
        # Spectator variables
        self.tmva_s_jetPt[0]      = jet_pt
        self.tmva_s_jetEta[0]     = jet_eta
        # Training variables
        self.tmva_v_nvtx[0]       = event.PV_npvsGood
        self.tmva_v_beta[0]       = jet.puId_beta
        self.tmva_v_dR2Mean[0]    = jet.puId_dR2Mean
        self.tmva_v_frac01[0]     = jet.puId_frac01
        self.tmva_v_frac02[0]     = jet.puId_frac02
        self.tmva_v_frac03[0]     = jet.puId_frac03
        self.tmva_v_frac04[0]     = jet.puId_frac04
        self.tmva_v_majW[0]       = jet.puId_majW
        self.tmva_v_minW[0]       = jet.puId_minW
        self.tmva_v_jetR[0]       = jet.puId_jetR
        self.tmva_v_jetRchg[0]    = jet.puId_jetRchg
        self.tmva_v_nParticles[0] = jet.nConstituents
        self.tmva_v_nCharged[0]   = jet.puId_nCharged
        self.tmva_v_ptD[0]        = jet.puId_ptD
        self.tmva_v_pull[0]       = jet.puId_pull
        #
        # Determine which eta bin
        #
        etaBinIdx = -1
        if abs(jet_eta) > 0.00 and abs(jet_eta) <= 2.50:
          etaBinIdx = 0
        elif abs(jet_eta) > 2.50 and abs(jet_eta) <= 2.75:
          etaBinIdx = 1
        elif abs(jet_eta) > 2.75 and abs(jet_eta) <= 3.00:
          etaBinIdx = 2
        elif abs(jet_eta) > 3.00 and abs(jet_eta) <= 5.00:
          etaBinIdx = 3
        #
        # Calculate the BDT output and store the value
        #
        jet_puIdDiscOTF = self.tmva_readers[etaBinIdx].EvaluateMVA("BDT")
      else:
        jet_puIdDiscOTF = -9.
      #
      #
      #
      jets_puIdDiscOTF.append(jet_puIdDiscOTF)
    
    #
    # Save variable in TTree
    #
    self.out.fillBranch("Jet_puIdDiscOTF", jets_puIdDiscOTF)

    return True

PUIDCalculator_UL2017 = lambda : PUIDCalculator(era="UL2017", jetBranchName="Jet") 
