import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

import math
import array

class SkimmerDiMuon(Module):
  def __init__(self, isMC, era):
    self.era = era
    self.isMC = isMC
    self.writeHistFile=True
    self.maxNSelJetsSaved=2

  def beginJob(self, histFile, histDirName):
    Module.beginJob(self, histFile, histDirName)
    self.h_cutflow_uw = ROOT.TH1F('h_cutflow_uw','h_cutflow_uw', 15, 0, 15)
    self.h_cutflow_uw.GetXaxis().SetBinLabel(1,"NoSelection")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(2,"passPreselTrig")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(3,"passPreselNMuon")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(4,"pass2LooseMuons")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(5,"pass2TightMuons")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(6,"passTrigMatch")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(7,"passKinCuts")
    self.h_cutflow_uw.GetXaxis().SetBinLabel(8,"passZBosonMass")
    self.addObject(self.h_cutflow_uw)

    self.h_cutflow_w  = ROOT.TH1F('h_cutflow_w', 'h_cutflow_w',  15, 0, 15)
    self.h_cutflow_w.GetXaxis().SetBinLabel(1,"NoSelection")
    self.h_cutflow_w.GetXaxis().SetBinLabel(2,"passPreselTrig")
    self.h_cutflow_w.GetXaxis().SetBinLabel(3,"passPreselNMuon")
    self.h_cutflow_w.GetXaxis().SetBinLabel(4,"pass2LooseMuons")
    self.h_cutflow_w.GetXaxis().SetBinLabel(5,"pass2TightMuons")
    self.h_cutflow_w.GetXaxis().SetBinLabel(6,"passTrigMatch")
    self.h_cutflow_w.GetXaxis().SetBinLabel(7,"passKinCuts")
    self.h_cutflow_w.GetXaxis().SetBinLabel(8,"passZBosonMass")
    self.addObject(self.h_cutflow_w)

  def endJob(self):
    Module.endJob(self)
    print "SkimmerDiMuon module ended successfully"
    pass
      
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree     
    self.out.branch("mu0_pt",      "F")
    self.out.branch("mu0_eta",     "F")
    self.out.branch("mu0_phi",     "F")
    self.out.branch("mu0_mass",    "F")
    self.out.branch("mu0_charge",  "I")
    self.out.branch("mu1_pt",      "F")
    self.out.branch("mu1_eta",     "F")
    self.out.branch("mu1_phi",     "F")
    self.out.branch("mu1_mass",    "F")
    self.out.branch("mu1_charge",  "I")
    self.out.branch("dimuon_pt",   "F")
    self.out.branch("dimuon_eta",  "F")
    self.out.branch("dimuon_phi",  "F")
    self.out.branch("dimuon_mass", "F")
    self.out.branch("nJetSel",     "I")
    for i in xrange(0,self.maxNSelJetsSaved):
      self.out.branch("jet"+str(i)+"_pt",         "F")
      self.out.branch("jet"+str(i)+"_eta",        "F")
      self.out.branch("jet"+str(i)+"_phi",        "F")
      self.out.branch("jet"+str(i)+"_mass",       "F")
      self.out.branch("jet"+str(i)+"_jetId",      "I")
      self.out.branch("jet"+str(i)+"_puId",       "I")
      self.out.branch("jet"+str(i)+"_qgl",        "F")
      self.out.branch("jet"+str(i)+"_nConst",     "I")
      self.out.branch("jet"+str(i)+"_chEmEF",     "F")
      self.out.branch("jet"+str(i)+"_chHEF",      "F")
      self.out.branch("jet"+str(i)+"_neEmEF",     "F")
      self.out.branch("jet"+str(i)+"_neHEF",      "F")
      self.out.branch("jet"+str(i)+"_muEF",       "F")
      self.out.branch("jet"+str(i)+"_dimuon_dphi","F")
      if(self.isMC):
        self.out.branch("jet"+str(i)+"_partflav",     "I")
        self.out.branch("jet"+str(i)+"_hadflav",      "I")
        self.out.branch("jet"+str(i)+"_gen_match",    "B")
        self.out.branch("jet"+str(i)+"_gen_pt",       "F")
        self.out.branch("jet"+str(i)+"_gen_eta",      "F")
        self.out.branch("jet"+str(i)+"_gen_phi",      "F")
        self.out.branch("jet"+str(i)+"_gen_mass",     "F")
        self.out.branch("jet"+str(i)+"_gen_partflav", "I")
        self.out.branch("jet"+str(i)+"_gen_hadflav",  "I")

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    print "File closed successfully"
    pass

  def RegisterCut(self, cutName, weight):
    self.h_cutflow_uw.Fill(cutName,1)
    self.h_cutflow_w.Fill(cutName, weight)
          
  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""

    evtWeight = 1.0
    if self.isMC:
      evtWeight = event.genWeight

    self.RegisterCut("NoSelection", evtWeight)

    #######################
    #
    # Pre-selection
    #
    #######################
    passPreselTrig=False

    if self.era == "2016":
      passPreselTrig = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ
    elif self.era == "2017":
      passPreselTrig = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8
    elif self.era == "2018":
      passPreselTrig = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8
    
    if not(passPreselTrig): return False
    self.RegisterCut("passPreselTrig", evtWeight)

    passPreselNMuon = event.nMuon >= 2
    if not (passPreselNMuon): return False
    self.RegisterCut("passPreselNMuon", evtWeight)

    #######################
    #
    # Di-muon selection
    #
    #######################
    muons = Collection(event, "Muon")
  
    #
    # Loose selection
    #
    muonsLoose  = [x for x in muons 
      if x.pt > 10. and x.looseId and abs(x.eta) < 2.4 and x.pfIsoId >= 2
    ]
    muonsLoose.sort(key=lambda x:x.pt,reverse=True)

    #
    # Check if event has EXACTLY 2 Loose muons
    #
    pass2LooseMuons = len(muonsLoose) == 2
    if not pass2LooseMuons: return False
    self.RegisterCut("pass2LooseMuons", evtWeight)

    #
    # Tight selection
    #
    muonsTight  = [x for x in muonsLoose 
      if x.tightId and x.pfIsoId >= 4
    ] 

    #
    # Check if event has EXACTLY 2 Tight muons
    #
    pass2TightMuons = len(muonsTight) == 2
    if not pass2TightMuons: return False
    self.RegisterCut("pass2TightMuons", evtWeight)
    
    # 
    # Trigger matching
    #
    passMuon0TrigMatch = False
    passMuon1TrigMatch = False
    trigObjs = Collection(event, "TrigObj")
    for obj in trigObjs:
      if not(obj.id == 13):
        continue
      if(muonsTight[0].DeltaR(obj) < 0.1): 
        passMuon0TrigMatch = True
      if(muonsTight[1].DeltaR(obj) < 0.1): 
        passMuon1TrigMatch = True

    if not (passMuon0TrigMatch and passMuon1TrigMatch): return False
    self.RegisterCut("passTrigMatch", evtWeight)

    # 
    # Require each muon pt to be higher than the trigger thresholds
    #
    if(muonsTight[0].pt < 20 or muonsTight[1].pt < 10):
      return False
    self.RegisterCut("passKinCuts", evtWeight)

    #
    # Reconstruct Z-boson 
    #
    zcand_p4 = muonsTight[0].p4() + muonsTight[1].p4()

    #
    # Z-boson mass cut
    #
    if not (zcand_p4.M() > 70. and zcand_p4.M() < 110.):
      return False
    self.RegisterCut("passZBosonMass", evtWeight)

    #######################
    #
    # Jets selection
    #
    #######################
    jets    = Collection(event, "Jet")

    jetsSel = [x for x in jets 
      if x.pt > 20. and abs(x.eta) < 5. and x.DeltaR(muonsTight[0]) > 0.4 and x.DeltaR(muonsTight[1]) > 0.4
    ]
    jetsSel.sort(key=lambda x:x.pt,reverse=True)
    nJetSel=len(jetsSel)
    
    #
    # Match genjets to the selected reco jets
    #
    if self.isMC:
      genJets = Collection(event, "GenJet")
      pair = matchObjectCollection(jetsSel, genJets, dRmax=0.4)

    # now fill branches
    self.out.fillBranch("mu0_pt",       muonsTight[0].pt)
    self.out.fillBranch("mu0_eta",      muonsTight[0].eta)
    self.out.fillBranch("mu0_phi",      muonsTight[0].phi)
    self.out.fillBranch("mu0_mass",     muonsTight[0].mass)
    self.out.fillBranch("mu0_charge",   muonsTight[0].charge)
    self.out.fillBranch("mu1_pt",       muonsTight[1].pt)
    self.out.fillBranch("mu1_eta",      muonsTight[1].eta)
    self.out.fillBranch("mu1_phi",      muonsTight[1].phi)
    self.out.fillBranch("mu1_mass",     muonsTight[1].mass)
    self.out.fillBranch("mu1_charge",   muonsTight[1].charge)
    self.out.fillBranch("dimuon_pt",    zcand_p4.Pt())
    self.out.fillBranch("dimuon_eta",   zcand_p4.Eta())
    self.out.fillBranch("dimuon_phi",   zcand_p4.Phi())
    self.out.fillBranch("dimuon_mass",  zcand_p4.M())
    self.out.fillBranch("nJetSel",      nJetSel)
    #
    # Reset branch. 
    # NOTE:FIKRI: This is stupid. Surely can be simplified.
    #
    for i in xrange(0, self.maxNSelJetsSaved):
      self.out.fillBranch("jet"+str(i)+"_pt",     -9.)
      self.out.fillBranch("jet"+str(i)+"_eta",    -9.)
      self.out.fillBranch("jet"+str(i)+"_phi",    -9.)
      self.out.fillBranch("jet"+str(i)+"_mass",   -9.)
      self.out.fillBranch("jet"+str(i)+"_jetId",  -9)
      self.out.fillBranch("jet"+str(i)+"_puId",   -9)
      self.out.fillBranch("jet"+str(i)+"_qgl",    -9.)
      self.out.fillBranch("jet"+str(i)+"_nConst", -9)
      self.out.fillBranch("jet"+str(i)+"_chEmEF", -9.)
      self.out.fillBranch("jet"+str(i)+"_chHEF",  -9.)
      self.out.fillBranch("jet"+str(i)+"_neEmEF", -9.)
      self.out.fillBranch("jet"+str(i)+"_neHEF",  -9.)
      self.out.fillBranch("jet"+str(i)+"_muEF",   -9.)
      self.out.fillBranch("jet"+str(i)+"_dimuon_dphi",-9.)
      if self.isMC:
        self.out.fillBranch("jet"+str(i)+"_partflav",-9)
        self.out.fillBranch("jet"+str(i)+"_hadflav", -9)
        self.out.fillBranch("jet"+str(i)+"_gen_match", False)
        self.out.fillBranch("jet"+str(i)+"_gen_pt",      -9.)
        self.out.fillBranch("jet"+str(i)+"_gen_eta",     -9.)
        self.out.fillBranch("jet"+str(i)+"_gen_phi",     -9.)
        self.out.fillBranch("jet"+str(i)+"_gen_mass",    -9.)
        self.out.fillBranch("jet"+str(i)+"_gen_partflav", -9)
        self.out.fillBranch("jet"+str(i)+"_gen_hadflav",  -9)
    #
    # Store the jets
    #
    for i, jet in enumerate(jetsSel):
      if i >= self.maxNSelJetsSaved: break
      self.out.fillBranch("jet"+str(i)+"_pt",     jet.pt)
      self.out.fillBranch("jet"+str(i)+"_eta",    jet.eta)
      self.out.fillBranch("jet"+str(i)+"_phi",    jet.phi)
      self.out.fillBranch("jet"+str(i)+"_mass",   jet.mass)
      self.out.fillBranch("jet"+str(i)+"_jetId",  jet.jetId)
      self.out.fillBranch("jet"+str(i)+"_puId",   jet.puId)
      self.out.fillBranch("jet"+str(i)+"_qgl",    jet.qgl)
      self.out.fillBranch("jet"+str(i)+"_nConst", jet.nConstituents)
      self.out.fillBranch("jet"+str(i)+"_chEmEF", jet.chEmEF)
      self.out.fillBranch("jet"+str(i)+"_chHEF",  jet.chHEF)
      self.out.fillBranch("jet"+str(i)+"_neEmEF", jet.neEmEF)
      self.out.fillBranch("jet"+str(i)+"_neHEF",  jet.neHEF)
      self.out.fillBranch("jet"+str(i)+"_muEF",   jet.muEF)
      self.out.fillBranch("jet"+str(i)+"_dimuon_dphi",zcand_p4.DeltaPhi(jet.p4()))
      if self.isMC:
        self.out.fillBranch("jet"+str(i)+"_partflav",jet.partonFlavour)
        self.out.fillBranch("jet"+str(i)+"_hadflav", jet.hadronFlavour)
        genJet = pair[jet]
        if not (genJet==None):
          self.out.fillBranch("jet"+str(i)+"_gen_match", True)
          self.out.fillBranch("jet"+str(i)+"_gen_pt",   genJet.pt)
          self.out.fillBranch("jet"+str(i)+"_gen_eta",  genJet.eta)
          self.out.fillBranch("jet"+str(i)+"_gen_phi",  genJet.phi)
          self.out.fillBranch("jet"+str(i)+"_gen_mass", genJet.mass)
          self.out.fillBranch("jet"+str(i)+"_gen_partflav", genJet.partonFlavour)
          self.out.fillBranch("jet"+str(i)+"_gen_hadflav",  genJet.hadronFlavour)
    #
    # The event pass selection
    #
    return True

SkimmerDiMuon_2016_data = lambda : SkimmerDiMuon(isMC=False, era="2016") 
SkimmerDiMuon_2016_mc   = lambda : SkimmerDiMuon(isMC=True,  era="2016") 
#
SkimmerDiMuon_2017_data = lambda : SkimmerDiMuon(isMC=False, era="2017") 
SkimmerDiMuon_2017_mc   = lambda : SkimmerDiMuon(isMC=True,  era="2017") 
#
SkimmerDiMuon_2018_data = lambda : SkimmerDiMuon(isMC=False, era="2018") 
SkimmerDiMuon_2018_mc   = lambda : SkimmerDiMuon(isMC=True,  era="2018") 
