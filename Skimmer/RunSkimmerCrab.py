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

print "RunSkimmerCrab.py START"

parser = argparse.ArgumentParser("")
parser.add_argument('-jobNum', '--jobNum', type=int, default=1 ) #NOTE: This will be given by condor on the grid. not by us
parser.add_argument('-isMC',   '--isMC',   type=int, default=1 )
parser.add_argument('-era',    '--era',    type=str, default="")

args  = parser.parse_args()
isMC  = args.isMC
era   = args.era

print "args = ", args
print "isMC = ", isMC 
print "era  = ", era

varTxtFileIn="branches_in.txt"
varTxtFileOut="branches_out.txt"

selection= "nMuon>=1 && Muon_pt[0]>17. && nJet>=1"

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
  selection += " && (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ>0)"
  if isMC: 
    modules=[puWeight_2016(), jetCorr_AK4_MC16(), SkimmerDiMuon_2016_mc()]
  else:              
    modules=[SkimmerDiMuon_2016_data()]
    jsonInput=CMSSW_BASE+"/src/PUjetID/Skimmer/data/lumi/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
elif era == "2017":
  selection += " && (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8>0)"
  if isMC: 
    modules=[puWeight_2017(), jetCorr_AK4_MC17(), SkimmerDiMuon_2017_mc()]
  else:              
    modules=[SkimmerDiMuon_2017_data()]
    jsonInput=CMSSW_BASE+"/src/PUjetID/Skimmer/data/lumi/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
elif era == "2018":
  selection += " && (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8>0)"
  if isMC: 
    modules=[puWeight_2018(), jetCorr_AK4_MC18(), SkimmerDiMuon_2018_mc()]
  else:              
    modules=[SkimmerDiMuon_2018_data()]
    jsonInput=CMSSW_BASE+"/src/PUjetID/Skimmer/data/lumi/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"

# 
# This takes care of converting the input files from CRAB
#
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

p=PostProcessor(
  ".", 
  inputFiles(),
  cut=selection,
  branchsel=varTxtFileIn,
  outputbranchsel=varTxtFileOut,
  modules=modules,
  provenance=True,
  fwkJobReport=True,
  jsonInput=jsonInput if not(isMC) else None,
)
p.run()

print "RunSkimmerCrab.py DONE"
os.system("ls -lR")

