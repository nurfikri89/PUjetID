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
    self.maxNSelJetsSaved=1
    #
    # List jet systematics
    #
    ak4Systematics=[
      "jesTotalUp",
      "jesTotalDown",
      "jerUp"
    ]
    self.jetSystsList = [""] # Nominal
    if self.isMC:
      self.jetSystsList.extend(ak4Systematics)

  def beginJob(self,histFile=None,histDirName=None):
    Module.beginJob(self)

  def endJob(self):
    Module.endJob(self)
    print "SkimmerDiMuon module ended successfully"
    pass

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    print "File closed successfully"
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch("dimuon_pt",   "F")
    self.out.branch("dimuon_eta",  "F")
    self.out.branch("dimuon_phi",  "F")
    self.out.branch("dimuon_mass", "F")
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
    #
    # Jet branches
    #
    for jetSyst in self.jetSystsList:
      jetSystPreFix = self.getJetSystBranchPrefix(jetSyst)
      self.out.branch(jetSystPreFix+"nJetSel", "I")
      for i in xrange(0,self.maxNSelJetsSaved):
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_pt",         "F") 
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_pt_nom",     "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_eta",        "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_phi",        "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_mass",       "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_mass_nom",   "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_jetId",      "I")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_puId",       "I")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_qgl",        "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_nConst",     "I")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_chEmEF",     "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_chHEF",      "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_neEmEF",     "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_neHEF",      "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_muEF",       "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_dimuon_dphi","F")
        if(self.isMC):
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_partflav",     "I")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_hadflav",      "I")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_gen_match",    "B")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_gen_pt",       "F")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_gen_eta",      "F")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_gen_phi",      "F")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_gen_mass",     "F")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_gen_partflav", "I")
          self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_gen_hadflav",  "I")

  def getJetSystBranchPrefix(self, jetSyst):
    jetSystPreFix = "" if jetSyst == "" else jetSyst+"_"
    return jetSystPreFix

  def getJetSystBranchPostfix(self, jetSyst):
    jetSystPreFix = "" if jetSyst == "" else "_"+jetSyst
    return jetSystPreFix

  def getJetPtAndMassForSyst(self, jetSyst):

    if self.isMC:
      jetPt   = "pt_nom"   if jetSyst == "" else "pt_"+jetSyst
      jetMass = "mass_nom" if jetSyst == "" else "mass_"+jetSyst
    else:
      jetPt   = "pt"   #NOTE: Not necessarily true. We're not making any corrections to jets in data.
      jetMass = "mass" #It has been applied at the NanoAOD production level.

    return jetPt, jetMass

  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""

    if self.passEventPreselection(event) is False:
      return False

    if self.passTriggerSelection(event) is False:
      return False

    if self.passZBosonSelection(event) is False:
      return False 

    self.fillZBosonBranches(event)
    
    #
    # Skip event and don't store in tree if this selection doesn't pass nominal
    # and any systematic shift
    #
    event.passJetSelNomSyst = False
    
    for jetSyst in self.jetSystsList:
      self.resetJetBranches(event, jetSyst)
      event.passJetSelNomSyst |= self.passJetSelection(event, jetSyst)
      self.fillJetBranches(event, jetSyst)

    if event.passJetSelNomSyst:
      return True
    else:
      return False

  def passEventPreselection(self, event):
    #######################
    #
    # Pre-selection
    #
    #######################

    if event.PV_npvsGood < 1:
      return False

    event.evtWeight = 1.0
    if self.isMC:
      event.evtWeight = event.genWeight

    # Event pass selection
    return True

  def passTriggerSelection(self, event):
    #######################
    #
    # Trigger selection
    #
    #######################

    event.passPreselTrig=False

    if self.era == "2016":
      event.passPreselTrig = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ
    elif self.era == "2017":
      event.passPreselTrig = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8
    elif self.era == "2018":
      event.passPreselTrig = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8
    
    if not(event.passPreselTrig): return False
    
    # Event pass selection
    return True

  def passZBosonSelection(self, event):
    #######################
    #
    # Di-muon selection
    #
    #######################
    event.passPreselNMuon = event.nMuon >= 2
    if not (event.passPreselNMuon): return False

    event.muonsAll = Collection(event, "Muon")
  
    #
    # Loose selection
    #
    event.muonsLoose  = [x for x in event.muonsAll 
      if x.pt > 10. and x.looseId and abs(x.eta) < 2.4 and x.pfIsoId >= 2
    ]
    event.muonsLoose.sort(key=lambda x:x.pt,reverse=True)

    #
    # Check if event has EXACTLY 2 Loose muons
    #
    event.pass2LooseMuons = len(event.muonsLoose) == 2
    if not event.pass2LooseMuons: return False

    #
    # Tight selection
    #
    event.muonsTight  = [x for x in event.muonsLoose 
      if x.tightId and x.pfIsoId >= 4 and x.isPFcand 
    ] 

    #
    # Check if event has EXACTLY 2 Tight muons
    #
    event.pass2TightMuons = len(event.muonsTight) == 2
    if not event.pass2TightMuons: return False
    
    # 
    # Trigger matching
    #
    event.passMuon0TrigMatch = False
    event.passMuon1TrigMatch = False
    event.trigObjsAll = Collection(event, "TrigObj")
    for obj in event.trigObjsAll:
      if not(obj.id == 13):
        continue
      if(event.muonsTight[0].DeltaR(obj) < 0.1): 
        event.passMuon0TrigMatch = True
      if(event.muonsTight[1].DeltaR(obj) < 0.1): 
        event.passMuon1TrigMatch = True

    if not (event.passMuon0TrigMatch and event.passMuon1TrigMatch): return False

    # 
    # Require each muon pt to be higher than the trigger thresholds
    #
    if(event.muonsTight[0].pt < 20 or event.muonsTight[1].pt < 10):
      return False

    #
    # Reconstruct Z-boson p4
    #
    event.zcand_p4 = event.muonsTight[0].p4() + event.muonsTight[1].p4()

    #
    # Z-boson mass cut
    #
    if not (event.zcand_p4.M() > 70. and event.zcand_p4.M() < 110.):
      return False
    
    # Event pass selection
    return True

  def passJetSelection(self, event, jetSyst=""):
    #######################
    #
    # Jets selection
    #
    #######################
    event.jetsAll = Collection(event, "Jet")

    #
    # Get the name of the jet pt and jet mass branches 
    # for nominal and systematic shifts
    #
    jetPtName, jetMassName = self.getJetPtAndMassForSyst(jetSyst)

    event.jetsSel = [x for x in event.jetsAll 
      if getattr(x, jetPtName) > 20. and abs(x.eta) < 5. and x.DeltaR(event.muonsTight[0]) > 0.4 and x.DeltaR(event.muonsTight[1]) > 0.4
    ]
    event.jetsSel.sort(key=lambda x:getattr(x, jetPtName), reverse=True)
    event.nJetSel=len(event.jetsSel)
    #
    # Check if event has at least one selected jets
    #
    event.passAtLeast1Jet = event.nJetSel >= 1
    if not event.passAtLeast1Jet: return False
    #
    # Match genjets to the selected reco jets
    #
    if self.isMC:
      event.genJetsAll = Collection(event, "GenJet")
      event.pair = matchObjectCollection(event.jetsSel, event.genJetsAll, dRmax=0.4)
    #
    # The event pass selection
    #
    return True

  def fillZBosonBranches(self, event):
    self.out.fillBranch("dimuon_pt",    event.zcand_p4.Pt())
    self.out.fillBranch("dimuon_eta",   event.zcand_p4.Eta())
    self.out.fillBranch("dimuon_phi",   event.zcand_p4.Phi())
    self.out.fillBranch("dimuon_mass",  event.zcand_p4.M())
    self.out.fillBranch("mu0_pt",       event.muonsTight[0].pt)
    self.out.fillBranch("mu0_eta",      event.muonsTight[0].eta)
    self.out.fillBranch("mu0_phi",      event.muonsTight[0].phi)
    self.out.fillBranch("mu0_mass",     event.muonsTight[0].mass)
    self.out.fillBranch("mu0_charge",   event.muonsTight[0].charge)
    self.out.fillBranch("mu1_pt",       event.muonsTight[1].pt)
    self.out.fillBranch("mu1_eta",      event.muonsTight[1].eta)
    self.out.fillBranch("mu1_phi",      event.muonsTight[1].phi)
    self.out.fillBranch("mu1_mass",     event.muonsTight[1].mass)
    self.out.fillBranch("mu1_charge",   event.muonsTight[1].charge)

  def resetJetBranches(self, event, jetSyst):
    #  reset jet branches
    jetSystPreFix = self.getJetSystBranchPrefix(jetSyst)

    self.out.fillBranch(jetSystPreFix+"nJetSel", -1)
    for i in xrange(0, self.maxNSelJetsSaved):
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt",      -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt_nom",  -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_eta",     -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_phi",     -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass",    -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass_nom",-9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_jetId",  -9)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_puId",   -9)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_qgl",    -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_nConst", -9)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chEmEF", -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chHEF",  -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neEmEF", -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neHEF",  -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_muEF",   -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_dimuon_dphi",-9.)
      if self.isMC:
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_partflav",-9)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_hadflav", -9)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_match", False)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_pt",      -9.)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_eta",     -9.)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_phi",     -9.)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_mass",    -9.)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_partflav", -9)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_hadflav",  -9)

  def fillJetBranches(self, event, jetSyst):
    # fill jet branches
    jetSystPreFix = self.getJetSystBranchPrefix(jetSyst)

    # Get the name of the jet pt and jet mass branches 
    # for nominal and systematic shifts
    jetPtName, jetMassName = self.getJetPtAndMassForSyst(jetSyst)

    self.out.fillBranch(jetSystPreFix+"nJetSel", event.nJetSel)
    for i, jet in enumerate(event.jetsSel):
      if i >= self.maxNSelJetsSaved: break
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt",      getattr(jet, jetPtName))
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt_nom",  getattr(jet, "pt_nom") if self.isMC else jet.pt)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_eta",     jet.eta)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_phi",     jet.phi)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass",    getattr(jet, jetMassName))
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass_nom",getattr(jet, "mass_nom") if self.isMC else jet.mass)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_jetId",   jet.jetId)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_puId",    jet.puId)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_qgl",     jet.qgl)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_nConst",  jet.nConstituents)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chEmEF",  jet.chEmEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chHEF",   jet.chHEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neEmEF",  jet.neEmEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neHEF",   jet.neHEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_muEF",    jet.muEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_dimuon_dphi",event.zcand_p4.DeltaPhi(jet.p4()))
      if self.isMC:
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_partflav",jet.partonFlavour)
        self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_hadflav", jet.hadronFlavour)
        genJet = event.pair[jet]
        if not (genJet==None):
          self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_match", True)
          self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_pt",   genJet.pt)
          self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_eta",  genJet.eta)
          self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_phi",  genJet.phi)
          self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_mass", genJet.mass)
          self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_partflav", genJet.partonFlavour)
          self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_gen_hadflav",  genJet.hadronFlavour)

SkimmerDiMuon_2016_data = lambda : SkimmerDiMuon(isMC=False, era="2016") 
SkimmerDiMuon_2017_data = lambda : SkimmerDiMuon(isMC=False, era="2017") 
SkimmerDiMuon_2018_data = lambda : SkimmerDiMuon(isMC=False, era="2018") 

SkimmerDiMuon_2016_mc   = lambda : SkimmerDiMuon(isMC=True,  era="2016") 
SkimmerDiMuon_2017_mc   = lambda : SkimmerDiMuon(isMC=True,  era="2017") 
SkimmerDiMuon_2018_mc   = lambda : SkimmerDiMuon(isMC=True,  era="2018") 
