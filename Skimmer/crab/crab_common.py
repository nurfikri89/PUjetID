from CRABClient.UserUtilities import config
config = config()
#
# Set version number (CHECK)
#
version="DiMuonSkim_v1"
#
# Set request name prefx
#
reqNamePrefix="JetPUId"
#
# Change this PATH where the crab directories are stored
# Example: config.General.workArea = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects/'
#
config.General.workArea        = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects/'
config.General.transferOutputs = True
config.General.transferLogs    = True
#
config.JobType.pluginName = 'Analysis'
config.JobType.psetName   = 'PSet.py'
config.JobType.scriptExe  = 'crab_script.sh'
#
config.JobType.inputFiles = [
'../script/branches_in.txt',
'../script/branches_out.txt',
'../RunSkimmerCrab.py',
]
#
config.JobType.sendPythonFolder  = True
config.JobType.outputFiles = ['tree.root','histo.root']
#
config.Data.splitting    = 'FileBased'
config.Data.unitsPerJob  = 1
config.Data.publication  = False
config.Data.allowNonValidInputDataset = True
config.JobType.allowUndistributedCMSSW = True
#
# Specify the outLFNDirBase and your storage site
#
#
# JetMET CMS EOS space at CERN
#
config.Data.outLFNDirBase  = '/store/group/phys_jetmet/CRABOUTPUT_JetPUId_'+version+'/'
config.Site.storageSite    = 'T2_CH_CERN'
#
# User CERNBox 
#
# config.Data.outLFNDirBase  = '/store/user/nbinnorj/CRABOUTPUT_JetPUId_'+version+'/'
# config.Site.storageSite    = 'T2_CH_CERNBOX'
#
config.Data.ignoreLocality = True
whitelist_sites=[
'T2_CH_CERN',
'T2_US_*',
'T2_UK_*',
'T2_DE_*',
'T2_FR_*',
]
config.Site.whitelist = whitelist_sites
