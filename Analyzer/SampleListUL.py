import collections

class Sample:
  def __init__(self, name="", crabFiles=[], ntupleFiles=[]):
    self.name  = name
    self.crabFiles = crabFiles 
    self.ntupleFiles = ntupleFiles 

version="DiLeptonSkim_JMEnanoUL_v0p1"

EOSURL="root://eoscms.cern.ch/"
EOSDIR="/eos/cms/store/group/phys_jetmet/nbinnorj/"
CRABDIR="JetPUId_"+version+"/CRABOUTPUT/"
NTUPDIR="JetPUId_"+version+"/ntuples_skim/"
Samples = collections.OrderedDict()

################################################
#
# 2016
#
################################################

################################################
#
# 2017
#
################################################
Samples["MCUL17_DY_MG"] = Sample(
  name="MCUL17_DY_MG",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/JetPUId_MCUL17JMEnanoV1_"+version+"/*/*/tree_*.root",
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MCUL17_DY_MG.root"
  ]
)
Samples["MCUL17_DY_AMCNLO"] = Sample(
  name="MCUL17_DY_AMCNLO",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/JetPUId_MCUL17JMEnanoV1_"+version+"/*/*/tree_*.root",
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MCUL17_DY_AMCNLO.root"
  ]
)
Samples["DataUL17B_DoubleMuon"] = Sample(
  name="DataUL17B_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017B-DataUL17JMEnanoV1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_DataUL17B_DoubleMuon.root"
  ]
)
Samples["DataUL17C_DoubleMuon"] = Sample(
  name="DataUL17C_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017C-DataUL17JMEnanoV1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_DataUL17C_DoubleMuon.root"
  ]
)
Samples["DataUL17D_DoubleMuon"] = Sample(
  name="DataUL17D_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017D-DataUL17JMEnanoV1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_DataUL17D_DoubleMuon.root"
  ]
)
Samples["DataUL17E_DoubleMuon"] = Sample(
  name="DataUL17E_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017E-DataUL17JMEnanoV1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_DataUL17E_DoubleMuon.root"
  ]
)
Samples["DataUL17F_DoubleMuon"] = Sample(
  name="DataUL17F_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017F-DataUL17JMEnanoV1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_DataUL17F_DoubleMuon.root"
  ]
)
################################################
#
# 2018
#
################################################

