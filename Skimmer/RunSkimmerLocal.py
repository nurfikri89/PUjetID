#!/usr/bin/env python
import os,sys
import ROOT
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

print "RunSkimmerLocal.py START"

parser = argparse.ArgumentParser("")
parser.add_argument('--era',              type=str, default="")
parser.add_argument('--maxEvents',        type=int, default=-1)
parser.add_argument('--outDir',           type=str, default=".")
parser.add_argument('--isMC',             type=int ,default=0)
parser.add_argument('--dataStream',       type=str ,default="")

args        = parser.parse_args()
era         = args.era
maxEvents   = args.maxEvents
outDir      = args.outDir
isMC        = args.isMC
dataStream  = args.dataStream

print "args = ", args
print "era  = ", era
print "isMC = ", isMC 
print "dataStream = ", dataStream

isDoubleElecData=False
isDoubleMuonData=False

if "DoubleEG" in dataStream:
  isDoubleElecData = True
if "EGamma" in dataStream:
  isDoubleElecData = True
if "DoubleMuon" in dataStream:
  isDoubleMuonData = True

print "isDoubleElecData = ", isDoubleElecData
print "isDoubleMuonData = ", isDoubleMuonData

if isMC and (isDoubleElecData or isDoubleMuonData):
  raise Exception('isMC flag cannot be set to true with isDoubleMuonData or isDoubleElecData. Please check! (isMC={},isDoubleMuonData={},isDoubleElecData={})'.format(isMC,isDoubleMuonData,isDoubleElecData))

files=[]
if era == "2016":
  if isMC:
    files = [
      "/store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/120000/0643F6C0-C42B-564C-A9BD-161948BBFB81.root"
    ]
  else:
    if isDoubleMuonData:
      files = [
        "/store/data/Run2016H/DoubleMuon/NANOAOD/02Apr2020-v1/250000/24C37CC0-C415-5F43-96A6-F5D37E30B79B.root",
      ]
    elif isDoubleElecData:
      files = [
        "/store/data/Run2016H/DoubleEG/NANOAOD/02Apr2020-v1/250000/47FD42C2-6583-D941-95F4-1BFF0061C7D5.root",
      ]
  CMSXROOTD="root://xrootd-cms.infn.it/"
  files = [CMSXROOTD+file for file in files]
elif era == "UL2017":
  if isMC:
    files = [
      "/eos/cms/store/group/phys_jetmet/JMEnanoV01/UL17/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer19UL17JMEnanoV1-106X_mc2017_realistic_v6-v2/201026_101150/0000/step1_NANO_1.root"
    ]
  else:
    if isDoubleMuonData:
      files = [
        "/eos/cms/store/group/phys_jetmet/JMEnanoV01/UL17/DoubleMuon/Run2017B-09Aug2019_UL2017-v1_JMEnanoV1/201026_100435/0000/step1_NANO_1.root",
      ]
    elif isDoubleElecData:
      files = []
  CMSXROOTD="root://eoscms.cern.ch/"
  files = [CMSXROOTD+file for file in files]

varTxtFileIn="./script/branches_in.txt"
varTxtFileOut="./script/branches_out.txt"

from RunSkimmerHelper import *
#
# Get JSON
#
CMSSW_BASE = os.getenv('CMSSW_BASE')
jsonInput = None
if not isMC:
  jsonInput = CMSSW_BASE+GetJSON(era)
#
# Get selection string
#
selection = GetSelection(era)
#
# Get list of modules modules
#
modules = GetModules(era,isMC,dataStream)

print "\n"
print "Just printout what we will give to the PostProcessor"
print "JSON      : ", jsonInput
print "SELECTION : ", selection
print "MODULES   : ", modules

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
  jsonInput=jsonInput if not(isMC) else None,
  maxEntries=maxEntries
)
p.run()

print "RunSkimmerLocal.py DONE"
