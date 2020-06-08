import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

import math
import array

class SkimmerDiLepton(Module):
  def __init__(self, isMC, era, isDoubleElecData=False, isDoubleMuonData=False):
    self.era = era
    self.isMC = isMC
    self.maxNSelJetsSaved=1
    self.isDoubleElecData=False
    self.isDoubleMuonData=False
    if not(self.isMC):
      self.isDoubleElecData=isDoubleElecData
      self.isDoubleMuonData=isDoubleMuonData
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
    print "SkimmerDiLepton module ended successfully"
    pass

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    print "File closed successfully"
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch("dilep_pt",     "F")
    self.out.branch("dilep_eta",    "F")
    self.out.branch("dilep_phi",    "F")
    self.out.branch("dilep_mass",   "F")
    self.out.branch("lep0_pt",      "F")
    self.out.branch("lep0_eta",     "F")
    self.out.branch("lep0_phi",     "F")
    self.out.branch("lep0_mass",    "F")
    self.out.branch("lep0_charge",  "I")
    self.out.branch("lep0_pdgId",   "I")
    self.out.branch("lep1_pt",      "F")
    self.out.branch("lep1_eta",     "F")
    self.out.branch("lep1_phi",     "F")
    self.out.branch("lep1_mass",    "F")
    self.out.branch("lep1_charge",  "I")
    self.out.branch("lep1_pdgId",   "I")
    #
    # Jet branches
    #
    for jetSyst in self.jetSystsList:
      jetSystPreFix = self.getJetSystBranchPrefix(jetSyst)
      self.out.branch(jetSystPreFix+"nJetSel", "I")
      self.out.branch(jetSystPreFix+"nJetSelPt30Eta5p0", "I")
      self.out.branch(jetSystPreFix+"nJetSelPt20Eta2p4", "I")
      for i in xrange(0,self.maxNSelJetsSaved):
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_pt",         "F") 
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_pt_nom",     "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_pt_nano",    "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_eta",        "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_phi",        "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_mass",       "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_mass_nom",   "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_mass_nano",  "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_jetId",      "I")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_puId",       "I")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_qgl",        "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_nConst",     "I")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_chEmEF",     "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_chHEF",      "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_neEmEF",     "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_neHEF",      "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_muEF",       "F")
        self.out.branch(jetSystPreFix+"jetSel"+str(i)+"_dilep_dphi", "F")
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
    
    #
    # Check for trigger selection. Skip event if it doesn't
    # even pass one of them
    #
    passElTrig = self.passElectronTriggerSelection(event)
    passMuTrig = self.passMuonTriggerSelection(event)

    if passElTrig is False and passMuTrig is False:
      return False

    if self.passZBosonSelection(event) is False:
      return False 
    
    self.fillZBosonBranches(event)
    
    #
    # Skip event and don't store in tree if this selection doesn't pass nominal
    # and any systematic variations
    #
    event.passJetSelNomSyst = False

    for jetSyst in self.jetSystsList:
      self.resetJetBranches(event, jetSyst)
      if self.passJetSelection(event, jetSyst):
        event.passJetSelNomSyst |= True
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

  def passElectronTriggerSelection(self, event):
    ##############################
    #
    # Di-electron trigger selection
    #
    #############################
    event.passElectronTrig=False

    if self.era == "2016":
      if hasattr(event, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'):
        event.passElectronTrig |= event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ
    elif self.era == "2017":
      if hasattr(event, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'):
        event.passElectronTrig |= event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL
    elif self.era == "2018":
      if hasattr(event, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'):
        event.passElectronTrig |= event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL
    
    return True if event.passElectronTrig else False
      
  def passMuonTriggerSelection(self, event):
    #############################
    #
    # Di-muon trigger selection
    #
    ############################
    event.passMuonTrig=False

    if self.era == "2016":
      if hasattr(event, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'):
        event.passMuonTrig |= event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ
      if hasattr(event, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'):
        event.passMuonTrig |= event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL
      if hasattr(event, 'HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL'):
        event.passMuonTrig |= event.HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL
    elif self.era == "2017":
      if hasattr(event, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8'):
        event.passMuonTrig |= event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8
    elif self.era == "2018":
      if hasattr(event, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'):
        event.passMuonTrig |= event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8
    
    return True if event.passMuonTrig else False
 
  def passZBosonSelection(self, event):
    #######################
    #
    # Leptons pre-selection
    #
    #######################

    event.passPreselNMuon = event.nMuon >= 2
    event.passPreselNElectron = event.nElectron >= 2
    if not (event.passPreselNMuon or event.passPreselNElectron): return False

    #######################
    #
    # Muon selection
    #
    #######################
    event.muonsAll = Collection(event, "Muon")

    #
    # Veto muon selection
    #
    event.muonsVeto  = [x for x in event.muonsAll 
      if  x.pt > 10. and x.looseId and abs(x.eta) < 2.4 and x.pfIsoId >= 1 and x.isPFcand 
    ]
    event.muonsVeto.sort(key=lambda x:x.pt,reverse=True)

    #
    # Tight muon selection
    #
    event.muonsTight  = [x for x in event.muonsVeto 
      if x.pt > 20. and x.mediumPromptId and x.pfIsoId >= 4 
    ] 

    event.pass0VetoMuons  = len(event.muonsVeto)  == 0
    event.pass2VetoMuons  = len(event.muonsVeto)  == 2
    event.pass2TightMuons = len(event.muonsTight) == 2

    #######################
    #
    # Electron selection
    #
    #######################
    event.electronsAll = Collection(event, "Electron")

    #
    # Veto electron selection
    #
    event.electronsVeto  = [x for x in event.electronsAll 
      if x.pt > 10. and x.cutBased>=1 and abs(x.eta) < 2.4
    ]
    event.electronsVeto.sort(key=lambda x:x.pt,reverse=True)

    #
    # Tight electron selection
    #
    event.electronsTight  = [x for x in event.electronsVeto 
      if x.pt > 20. and x.mvaFall17V2Iso_WP90 
      and abs(x.deltaEtaSC+x.eta) < 2.5 
      and not(abs(x.deltaEtaSC+x.eta)>=1.4442) and (abs(x.deltaEtaSC+x.eta)<1.566) # ignore electrons in gap region
    ]

    event.pass0VetoElectrons  = len(event.electronsVeto)  == 0
    event.pass2VetoElectrons  = len(event.electronsVeto)  == 2
    event.pass2TightElectrons = len(event.electronsTight) == 2
    #####################################################
    #
    # Di-lepton (Z-boson) reconstruction and selection
    #
    ####################################################
    event.passLep0TrigMatch = False
    event.passLep1TrigMatch = False
    event.passLep0TrigThreshold = False
    event.passLep1TrigThreshold = False

    event.lep0_p4 = None
    event.lep1_p4 = None
    event.dilep_p4 = None
    event.lep0_pdgId  = None
    event.lep1_pdgId  = None
    event.lep0_charge = None
    event.lep1_charge = None
    #============================================
    #
    # Check if pass dimuon selection
    #
    #============================================
    if event.pass2TightMuons and event.pass2VetoMuons and event.pass0VetoElectrons: 
      # 
      # Trigger matching
      #
      event.trigObjsAll = Collection(event, "TrigObj")
      for obj in event.trigObjsAll:
        if not(obj.id == 13):
          continue
        if not(obj.filterBits&1): 
          continue   
        if not(obj.filterBits&16): 
          continue    
        if(event.muonsTight[0].DeltaR(obj) < 0.1): 
          event.passLep0TrigMatch = True
        if(event.muonsTight[1].DeltaR(obj) < 0.1): 
          event.passLep1TrigMatch = True
      # 
      # Offline cuts should be tighter than trigger thresholds.
      # Could probably already be tighter than it is stated here 
      # but just check it again just to be safe.
      #
      if event.muonsTight[0].pt > 20: event.passLep0TrigThreshold = True
      if event.muonsTight[1].pt > 10: event.passLep1TrigThreshold = True
      # 
      # Assign lepton p4
      #
      event.lep0_p4 = event.muonsTight[0].p4()
      event.lep1_p4 = event.muonsTight[1].p4()
      event.lep0_charge = event.muonsTight[0].charge
      event.lep1_charge = event.muonsTight[1].charge
      event.lep0_pdgId = event.muonsTight[0].pdgId
      event.lep1_pdgId = event.muonsTight[1].pdgId
    #============================================
    #
    # Check if pass dielectron selection
    #
    #============================================
    elif event.pass2TightElectrons and event.pass2VetoElectrons and event.pass0VetoMuons: 
      # 
      # Trigger matching
      #
      event.trigObjsAll = Collection(event, "TrigObj")
      for obj in event.trigObjsAll:
        if not(obj.id == 11):
          continue
        if not(obj.filterBits&1): 
          continue   
        if not(obj.filterBits&16): 
          continue  
        if(event.electronsTight[0].DeltaR(obj) < 0.1): 
          event.passLep0TrigMatch = True
        if(event.electronsTight[1].DeltaR(obj) < 0.1): 
          event.passLep1TrigMatch = True
      # 
      # Offline cuts should be tighter than trigger thresholds.
      # Could probably already be tighter than it is stated here 
      # but just check it again just to be safe.
      #
      if event.electronsTight[0].pt > 25: event.passLep0TrigThreshold = True
      if event.electronsTight[1].pt > 15: event.passLep1TrigThreshold = True
      # 
      # Assign lepton p4
      #
      event.lep0_p4 = event.electronsTight[0].p4()
      event.lep1_p4 = event.electronsTight[1].p4()
      event.lep0_charge = event.electronsTight[0].charge
      event.lep1_charge = event.electronsTight[1].charge
      event.lep0_pdgId = event.electronsTight[0].pdgId
      event.lep1_pdgId = event.electronsTight[1].pdgId
    #============================================
    #
    # Fail both channels
    #
    #============================================
    else:
      return False

    #============================================
    #
    # Apply trigger selection based on channel
    #
    #============================================
    event.passLepTrigSel = False
    #
    # Check trigger by channel
    #
    if abs(event.lep0_pdgId) == 13 and abs(event.lep1_pdgId) == 13:
      # For MC
      if self.isMC:
        event.passLepTrigSel = event.passMuonTrig 
      # For Data
      else:
        event.passLepTrigSel = event.passMuonTrig if self.isDoubleMuonData else False
    elif abs(event.lep0_pdgId) == 11 and abs(event.lep1_pdgId) == 11:
      # For MC
      if self.isMC:
        event.passLepTrigSel = event.passElectronTrig
      # For Data
      else:
        event.passLepTrigSel = event.passElectronTrig if self.isDoubleElecData else False

    if not event.passLepTrigSel: return False

    #
    # Each selected offline lepton should be matched to HLT-level object
    #
    if not(event.passLep0TrigMatch and event.passLep1TrigMatch): return False
      
    #
    # Offline pt cut should be higher than online pt threshold
    #
    if not(event.passLep0TrigThreshold and event.passLep1TrigThreshold): return False

    #=====================================================================================
    #
    # Reconstruct di-lepton p4 and select events wit di-lepton mass in Z-boson mass window
    #
    #======================================================================================
    event.dilep_p4 =  event.lep0_p4 + event.lep1_p4
    return True if event.dilep_p4.M() > 70. and event.dilep_p4.M() < 110. else False

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
      if abs(x.eta) < 5. and getattr(x, jetPtName) > 20. 
      and (x.jetId & (1<<1)) # 'Tight' WP for jet ID
      and x.DeltaR(event.lep0_p4) > 0.4 and x.DeltaR(event.lep1_p4) > 0.4 
    ]
    event.jetsSel.sort(key=lambda x:getattr(x, jetPtName), reverse=True)
    event.nJetSel=len(event.jetsSel)
    #
    # The event must at least have 1 jet anywhere for us to do the analysis
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
    # Check if event passes
    # 1. <= 1 jet with pt > 30. GeV, |eta| < 5.0
    # AND
    # 2. <= 1 jet with pt > 20. GeV, |eta| < 2.4
    # NOTE: Apply this at analysis level. Save flag
    #
    event.jetsSelPt30Eta5p0 = [x for x in event.jetsSel 
      if abs(x.eta) < 5. and getattr(x, jetPtName) > 30.
    ]
    event.nJetSelPt30Eta5p0=len(event.jetsSelPt30Eta5p0)

    event.jetsSelPt20Eta2p4 = [x for x in event.jetsSel 
      if abs(x.eta) < 2.4 and getattr(x, jetPtName) > 20.
    ]
    event.nJetSelPt20Eta2p4=len(event.jetsSelPt20Eta2p4)
    #
    # The event pass selection
    #
    return True

  def fillZBosonBranches(self, event):
    self.out.fillBranch("dilep_pt",      event.dilep_p4.Pt())
    self.out.fillBranch("dilep_eta",     event.dilep_p4.Eta())
    self.out.fillBranch("dilep_phi",     event.dilep_p4.Phi())
    self.out.fillBranch("dilep_mass",    event.dilep_p4.M())
    self.out.fillBranch("lep0_pt",       event.lep0_p4.Pt())
    self.out.fillBranch("lep0_eta",      event.lep0_p4.Eta())
    self.out.fillBranch("lep0_phi",      event.lep0_p4.Phi())
    self.out.fillBranch("lep0_mass",     event.lep0_p4.M())
    self.out.fillBranch("lep0_charge",   event.lep0_charge)
    self.out.fillBranch("lep0_pdgId",    event.lep0_pdgId)
    self.out.fillBranch("lep1_pt",       event.lep1_p4.Pt())
    self.out.fillBranch("lep1_eta",      event.lep1_p4.Eta())
    self.out.fillBranch("lep1_phi",      event.lep1_p4.Phi())
    self.out.fillBranch("lep1_mass",     event.lep1_p4.M())
    self.out.fillBranch("lep1_charge",   event.lep1_charge)
    self.out.fillBranch("lep1_pdgId",    event.lep1_pdgId)

  def resetJetBranches(self, event, jetSyst):
    #  reset jet branches
    jetSystPreFix = self.getJetSystBranchPrefix(jetSyst)

    self.out.fillBranch(jetSystPreFix+"nJetSel", -1)
    self.out.fillBranch(jetSystPreFix+"nJetSelPt30Eta5p0", -1)
    self.out.fillBranch(jetSystPreFix+"nJetSelPt20Eta2p4", -1)
    for i in xrange(0, self.maxNSelJetsSaved):
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt",      -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt_nom",  -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt_nano", -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_eta",     -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_phi",     -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass",    -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass_nom",-9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass_nano",-9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_jetId",  -9)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_puId",   -9)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_qgl",    -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_nConst", -9)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chEmEF", -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chHEF",  -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neEmEF", -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neHEF",  -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_muEF",   -9.)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_dilep_dphi",-9.)
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
    self.out.fillBranch(jetSystPreFix+"nJetSelPt30Eta5p0", event.nJetSelPt30Eta5p0)
    self.out.fillBranch(jetSystPreFix+"nJetSelPt20Eta2p4", event.nJetSelPt20Eta2p4)
    for i, jet in enumerate(event.jetsSel):
      if i >= self.maxNSelJetsSaved: break
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt",      getattr(jet, jetPtName))
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt_nom",  getattr(jet, "pt_nom") if self.isMC else jet.pt)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_pt_nano", jet.pt)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_eta",     jet.eta)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_phi",     jet.phi)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass",    getattr(jet, jetMassName))
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass_nom",getattr(jet, "mass_nom") if self.isMC else jet.mass)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_mass_nano",jet.mass)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_jetId",   jet.jetId)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_puId",    jet.puId)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_qgl",     jet.qgl)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_nConst",  jet.nConstituents)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chEmEF",  jet.chEmEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_chHEF",   jet.chHEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neEmEF",  jet.neEmEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_neHEF",   jet.neHEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_muEF",    jet.muEF)
      self.out.fillBranch(jetSystPreFix+"jetSel"+str(i)+"_dilep_dphi",event.dilep_p4.DeltaPhi(jet.p4()))
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

SkimmerDiLepton_2016_data_dielectron = lambda : SkimmerDiLepton(isMC=False, era="2016", isDoubleElecData=True) 
SkimmerDiLepton_2017_data_dielectron = lambda : SkimmerDiLepton(isMC=False, era="2017", isDoubleElecData=True) 
SkimmerDiLepton_2018_data_dielectron = lambda : SkimmerDiLepton(isMC=False, era="2018", isDoubleElecData=True) 

SkimmerDiLepton_2016_data_dimuon = lambda : SkimmerDiLepton(isMC=False, era="2016", isDoubleMuonData=True) 
SkimmerDiLepton_2017_data_dimuon = lambda : SkimmerDiLepton(isMC=False, era="2017", isDoubleMuonData=True) 
SkimmerDiLepton_2018_data_dimuon = lambda : SkimmerDiLepton(isMC=False, era="2018", isDoubleMuonData=True) 

SkimmerDiLepton_2016_mc   = lambda : SkimmerDiLepton(isMC=True,  era="2016") 
SkimmerDiLepton_2017_mc   = lambda : SkimmerDiLepton(isMC=True,  era="2017") 
SkimmerDiLepton_2018_mc   = lambda : SkimmerDiLepton(isMC=True,  era="2018") 
