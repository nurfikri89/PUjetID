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
      "/store/mc/RunIISummer16NanoAODv6/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext2-v1/100000/9706CDAC-CBF7-DA42-B1F1-E199B81A704A.root"
    ]
  else:
    if isDoubleMuonData:
      files = [
        "/store/data/Run2016H/DoubleMuon/NANOAOD/Nano25Oct2019-v1/40000/8753C889-831B-2A48-AE53-E3EA7910458A.root",
      ]
    elif isDoubleElecData:
      files = [
        "/store/data/Run2016H/DoubleEG/NANOAOD/Nano25Oct2019-v1/260000/82D01E91-EC37-C64D-813B-2439F19BDA5B.root",
      ]

CMSXROOTD="root://xrootd-cms.infn.it/"
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
