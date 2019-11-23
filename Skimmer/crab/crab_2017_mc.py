import sys
import crab_common 
import helpers

crab_common.config.General.requestName = crab_common.reqNamePrefix+'MC17_'+crab_common.version

crab_common.config.JobType.maxJobRuntimeMin = 360

crab_common.config.JobType.scriptArgs = [
'isMC=1',
'era=2017',
]

crab_common.config.Data.inputDataset     = '/WprimeToWZToWhadZlep_width0p1_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM' #Dummy
crab_common.config.Data.outputDatasetTag = crab_common.reqNamePrefix+'MC17_'+crab_common.version  # Dummy

if __name__ == '__main__':
  #
  # Read in txt file with list of samples
  #
  f = open(sys.argv[1]) 
  samplelist =  helpers.GetSampleList(f)
  print "Will send crab jobs for the following samples:"
  for dataset in samplelist:
    print dataset
  print "\n\n"

  from CRABClient.UserUtilities import getUsernameFromSiteDB
  from CRABAPI.RawCommand import crabCommand
  for i, dataset in enumerate(samplelist):
    print "%d/%d:Sending CRAB job: %s" % (i+1,len(samplelist), dataset)
    crab_common.config.Data.inputDataset = dataset
    #
    # Have to make unique requestName. pain in the ass really
    # Sample naming convention is a bit dumb and makes this more difficult.
    #
    primaryName   = dataset.split('/')[1].split("_")[0:4]
    primaryName   = "_".join(primaryName)
    primaryName   = primaryName.replace("_13TeV","")
    #
    secondaryName = dataset.split('/')[2]
    original="RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7"#CHECK
    simple="MC17NanoAODv5"#CHECK
    secondaryName = secondaryName.replace(original,simple)#CHECK
    original="RunIIFall17NanoAODv5-PU2017RECOSIMstep_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7_ext1-v1"#CHECK
    simple="MC17NanoAODv5"#CHECK
    secondaryName = secondaryName.replace(original,simple)#CHECK
    #
    requestName = primaryName + "_" + secondaryName
    requestName = crab_common.reqNamePrefix +"_" + requestName + "_" + crab_common.version
    crab_common.config.General.requestName   = requestName
    #  
    outputDatasetTag = crab_common.reqNamePrefix +"_" + secondaryName + "_" + crab_common.version
    crab_common.config.Data.outputDatasetTag = outputDatasetTag 
    #
    print requestName , " | ", outputDatasetTag, "\n"
    crabCommand('submit', config = crab_common.config)
