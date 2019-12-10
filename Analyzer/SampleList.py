import collections

class Sample:
  def __init__(self, name="", files=[]):
    self.name  = name
    self.files = files 

version="DiMuonSkim_v0"
EOSUSER="root://eosuser.cern.ch/"
EOSDIR="/eos/user/n/nbinnorj/CRABOUTPUT_JetPUId_"+version+"/"

Samples = collections.OrderedDict()

Samples["MC16_DY_MG"] = Sample(
  name="MC16_DY_MG",
  files=[
    EOSDIR+"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/JetPUId_MC16NanoAODv5_ext1-v1_"+version+"/*/*/tree_*.root",
    EOSDIR+"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/JetPUId_MC16NanoAODv5_ext2-v1_"+version+"/*/*/tree_*.root"
  ]
)

Samples["MC16_DY_AMCNLO"] = Sample(
  name="MC16_DY_AMCNLO",
  files=[
    EOSDIR+"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/JetPUId_MC16NanoAODv5_ext2-v1_"+version+"/*/*/tree_*.root",
  ]
)

Samples["Data16B_DoubleMuon"] = Sample(
  name="Data16B_DoubleMuon",
  files=[
    EOSDIR+"DoubleMuon/JetPUId_Run2016B_ver1-Data16NanoAODv5_ver1-v1_"+version+"/*/*/tree_*.root",
    EOSDIR+"DoubleMuon/JetPUId_Run2016B_ver2-Data16NanoAODv5_ver2-v1_"+version+"/*/*/tree_*.root"
  ]
)

Samples["Data16C_DoubleMuon"] = Sample(
  name="Data16C_DoubleMuon",
  files=[
    EOSDIR+"DoubleMuon/JetPUId_Run2016C-Data16NanoAODv5-v1_"+version+"/*/*/tree_*.root"
  ]
)

Samples["Data16D_DoubleMuon"] = Sample(
  name="Data16D_DoubleMuon",
  files=[
    EOSDIR+"DoubleMuon/JetPUId_Run2016D-Data16NanoAODv5-v1_"+version+"/*/*/tree_*.root"
  ]
)

Samples["Data16E_DoubleMuon"] = Sample(
  name="Data16E_DoubleMuon",
  files=[
    EOSDIR+"DoubleMuon/JetPUId_Run2016E-Data16NanoAODv5-v1_"+version+"/*/*/tree_*.root"
  ]
)

Samples["Data16F_DoubleMuon"] = Sample(
  name="Data16F_DoubleMuon",
  files=[
    EOSDIR+"DoubleMuon/JetPUId_Run2016F-Data16NanoAODv5-v1_"+version+"/*/*/tree_*.root"
  ]
)

Samples["Data16G_DoubleMuon"] = Sample(
  name="Data16G_DoubleMuon",
  files=[
    EOSDIR+"DoubleMuon/JetPUId_Run2016G-Data16NanoAODv5-v1_"+version+"/*/*/tree_*.root"
  ]
)

Samples["Data16H_DoubleMuon"] = Sample(
  name="Data16H_DoubleMuon",
  files=[
    EOSDIR+"DoubleMuon/JetPUId_Run2016H-Data16NanoAODv5-v1_"+version+"/*/*/tree_*.root"
  ]
)