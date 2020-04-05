#!/usr/bin/env python
import os,sys
import ROOT
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight_2016
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight_2017
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight_2018

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

from PUjetID.Skimmer.SkimmerDiMuon import SkimmerDiMuon_2016_mc
from PUjetID.Skimmer.SkimmerDiMuon import SkimmerDiMuon_2016_data
from PUjetID.Skimmer.SkimmerDiMuon import SkimmerDiMuon_2017_mc
from PUjetID.Skimmer.SkimmerDiMuon import SkimmerDiMuon_2017_data
from PUjetID.Skimmer.SkimmerDiMuon import SkimmerDiMuon_2018_mc
from PUjetID.Skimmer.SkimmerDiMuon import SkimmerDiMuon_2018_data

print "RunSkimmerLocal.py START"

parser = argparse.ArgumentParser("")
parser.add_argument('-isMC','--isMC',           type=int, default=1 )
parser.add_argument('-era','--era',             type=str, default="")
parser.add_argument('-maxEvents','--maxEvents', type=int, default=-1)
parser.add_argument('-outDir','--outDir',       type=str, default=".")

args  = parser.parse_args()
isMC  = args.isMC
era   = args.era
maxEvents   = args.maxEvents
outDir = args.outDir

print "args = ", args
print "isMC = ", isMC 
print "era  = ", era
print "maxEvents  = ", maxEvents
print "outDir  = ", outDir

CMSXROOTD="root://xrootd-cms.infn.it/"
files=[]
if era == "2016":
  if isMC:
    files = [
      # CMSXROOTD+"/store/mc/RunIISummer16NanoAODv5/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7_ext1-v1/60000/6EE8EBFD-59F5-7742-ABAF-F4411F449075.root"
      "./MC16_DYJetsToLL_LO.root"
    ]
  else:
    files = [
      # CMSXROOTD+"/store/data/Run2016H/DoubleMuon/NANOAOD/Nano1June2019-v1/40000/7C7656AE-946A-C14F-9C66-53DB7F129C11.root"
      "./Data16H_DoubleMuon.root"
    ]

varTxtFileIn="./script/branches_in.txt"
varTxtFileOut="./script/branches_out.txt"

selection= "nMuon>=1 && Muon_pt[0]>17. && nJet >=1"

modules = []
jsonInput = None

CMSSW_BASE = os.getenv('CMSSW_BASE')

#
# Modules for jet pt resolution smearing on MC and get uncertainties
#
applyJetPtSmearing=True
if era == "2016":
  if isMC: 
    jetCorr_AK4_MC16 = createJMECorrector(isMC=True, dataYear="2016", runPeriod="", jesUncert="Total", redojec=False, jetType="AK4PFchs", applySmearing=applyJetPtSmearing)
elif era == "2017":
  if isMC: 
    jetCorr_AK4_MC17 = createJMECorrector(isMC=True, dataYear="2017", runPeriod="", jesUncert="Total", redojec=False, jetType="AK4PFchs", applySmearing=applyJetPtSmearing)
elif era == "2018":
  if isMC: 
    jetCorr_AK4_MC18 = createJMECorrector(isMC=True, dataYear="2018", runPeriod="", jesUncert="Total", redojec=False, jetType="AK4PFchs", applySmearing=applyJetPtSmearing)

#
# Configure additional selections and modules for each year
#
if era == "2016":
  selection += " && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"
  if isMC: 
    modules=[puWeight_2016(), jetCorr_AK4_MC16(), SkimmerDiMuon_2016_mc()]
  else:              
    modules=[SkimmerDiMuon_2016_data()]
    jsonInput=CMSSW_BASE+"/src/PUjetID/Skimmer/data/lumi/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
elif era == "2017":
  selection += " && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"
  if isMC: 
    modules=[puWeight_2017(), jetCorr_AK4_MC17(), SkimmerDiMuon_2017_mc()]
  else:              
    modules=[SkimmerDiMuon_2017_data()]
    jsonInput=CMSSW_BASE+"/src/PUjetID/Skimmer/data/lumi/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
elif era == "2018":
  selection += " && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"
  if isMC: 
    modules=[puWeight_2018(), jetCorr_AK4_MC18(), SkimmerDiMuon_2018_mc()]
  else:              
    modules=[SkimmerDiMuon_2018_data()]
    jsonInput=CMSSW_BASE+"/src/PUjetID/Skimmer/data/lumi/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"

#
#
#
maxEntries=None
if maxEvents > 0:
  maxEntries=maxEvents
  print "Maximum Number of Events to run over: ", maxEvents

p=PostProcessor(
  outDir, 
  files,
  cut=selection,
  branchsel=varTxtFileIn,
  outputbranchsel=varTxtFileOut,
  modules=modules,
  provenance=False,
  fwkJobReport=False,
  histFileName=outDir+"/histo.root",
  histDirName="cutflow",
  jsonInput=jsonInput if not(isMC) else None,
  maxEntries=maxEntries
)
p.run()

print "RunSkimmerLocal.py DONE"
