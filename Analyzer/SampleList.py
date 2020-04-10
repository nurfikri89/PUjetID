import collections

class Sample:
  def __init__(self, name="", crabFiles=[], ntupleFiles=[]):
    self.name  = name
    self.crabFiles = crabFiles 
    self.ntupleFiles = ntupleFiles 

version="DiMuonSkim_v2"
EOSURL="root://eoscms.cern.ch/"
EOSDIR="/eos/cms/store/group/phys_jetmet/nbinnorj/"
CRABDIR="JetPUId_"+version+"/CRABOUTPUT/"
NTUPDIR="JetPUId_"+version+"/ntuples_skim_njet1/"
Samples = collections.OrderedDict()

################################################
#
# 2016
#
################################################
Samples["MC16_DY_MG"] = Sample(
  name="MC16_DY_MG",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/JetPUId_MC16NanoAODv6_ext1_"+version+"/*/*/tree_*.root",
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/JetPUId_MC16NanoAODv6_ext2_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MC16_DY_MG.root"
  ]
)
Samples["MC16_DY_AMCNLO"] = Sample(
  name="MC16_DY_AMCNLO",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/JetPUId_MC16NanoAODv6_ext2_"+version+"/*/*/tree_*.root",
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MC16_DY_AMCNLO.root"
  ]
)
Samples["Data16B_DoubleMuon"] = Sample(
  name="Data16B_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016B_ver1-Data16NanoAODv6_ver1-v1_"+version+"/*/*/tree_*.root",
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016B_ver2-Data16NanoAODv6_ver2-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data16B_DoubleMuon.root"
  ]
)
Samples["Data16C_DoubleMuon"] = Sample(
  name="Data16C_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016C-Data16NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data16C_DoubleMuon.root"
  ]
)
Samples["Data16D_DoubleMuon"] = Sample(
  name="Data16D_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016D-Data16NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data16D_DoubleMuon.root"
  ]
)
Samples["Data16E_DoubleMuon"] = Sample(
  name="Data16E_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016E-Data16NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data16E_DoubleMuon.root"
  ]
)
Samples["Data16F_DoubleMuon"] = Sample(
  name="Data16F_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016F-Data16NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data16F_DoubleMuon.root"
  ]
)
Samples["Data16G_DoubleMuon"] = Sample(
  name="Data16G_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016G-Data16NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data16G_DoubleMuon.root"
  ]
)
Samples["Data16H_DoubleMuon"] = Sample(
  name="Data16H_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2016H-Data16NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data16H_DoubleMuon.root"
  ]
)
################################################
#
# 2017
#
################################################
Samples["MC17_DY_MG"] = Sample(
  name="MC17_DY_MG",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/JetPUId_MC17NanoAODv6_"+version+"/*/*/tree_*.root",
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/JetPUId_MC17NanoAODv6_ext1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MC17_DY_MG.root"
  ]
)
Samples["MC17_DY_AMCNLO"] = Sample(
  name="MC17_DY_AMCNLO",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/JetPUId_MC17NanoAODv6_new_pmx_"+version+"/*/*/tree_*.root",
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/JetPUId_MC17NanoAODv6_new_pmx_ext1_"+version+"/*/*/tree_*.root",
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MC17_DY_AMCNLO.root"
  ]
)
Samples["Data17B_DoubleMuon"] = Sample(
  name="Data17B_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017B-Data17NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data17B_DoubleMuon.root"
  ]
)
Samples["Data17C_DoubleMuon"] = Sample(
  name="Data17C_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017C-Data17NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data17C_DoubleMuon.root"
  ]
)
Samples["Data17D_DoubleMuon"] = Sample(
  name="Data17D_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017D-Data17NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data17D_DoubleMuon.root"
  ]
)
Samples["Data17E_DoubleMuon"] = Sample(
  name="Data17E_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017E-Data17NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data17E_DoubleMuon.root"
  ]
)
Samples["Data17F_DoubleMuon"] = Sample(
  name="Data17F_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2017F-Data17NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data17F_DoubleMuon.root"
  ]
)
################################################
#
# 2018
#
################################################
Samples["MC18_DY_MG"] = Sample(
  name="MC18_DY_MG",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/JetPUId_MC18NanoAODv6_"+version+"/*/*/tree_*.root",
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MC18_DY_MG.root"
  ]
)
Samples["MC18_DY_AMCNLO"] = Sample(
  name="MC18_DY_AMCNLO",
  crabFiles=[
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/JetPUId_MC18NanoAODv6_"+version+"/*/*/tree_*.root",
    EOSDIR+CRABDIR+"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/JetPUId_MC18NanoAODv6_ext2_"+version+"/*/*/tree_*.root",
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_MC18_DY_AMCNLO.root"
  ]
)
Samples["Data18A_DoubleMuon"] = Sample(
  name="Data18A_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2018A-Data18NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data18A_DoubleMuon.root"
  ]
)
Samples["Data18B_DoubleMuon"] = Sample(
  name="Data18B_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2018B-Data18NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data18B_DoubleMuon.root"
  ]
)
Samples["Data18C_DoubleMuon"] = Sample(
  name="Data18C_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2018C-Data18NanoAODv6-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data18C_DoubleMuon.root"
  ]
)
Samples["Data18D_DoubleMuon"] = Sample(
  name="Data18D_DoubleMuon",
  crabFiles=[
    EOSDIR+CRABDIR+"DoubleMuon/JetPUId_Run2018D-Data18NanoAODv6_ver2-v1_"+version+"/*/*/tree_*.root"
  ],
  ntupleFiles=[
    EOSDIR+NTUPDIR+"ntuple_Data18D_DoubleMuon.root"
  ]
)

