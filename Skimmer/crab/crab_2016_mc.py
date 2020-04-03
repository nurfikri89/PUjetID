import sys
import crab_common 
import helpers

crab_common.config.JobType.maxJobRuntimeMin = 600

crab_common.config.JobType.scriptArgs = [
'isMC=1',
'era=2016',
]

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
    # Have to make unique requestName. 
    #
    primaryName   = dataset.split('/')[1].split("_")[0:4]
    primaryName   = "_".join(primaryName)
    primaryName   = primaryName.replace("_13TeV","")
    #
    # TO DO: Fix This
    #
    secondaryName = dataset.split('/')[2]
    secondaryName = secondaryName.replace("RunIISummer16NanoAODv6-","MC16NanoAODv6")#RENAME CAMPAIGN. CHECK ITS UPDATED
    secondaryName = secondaryName.replace("_Nano25Oct2019","") #RENAME CAMPAIGN. CHECK ITS UPDATE
    secondaryName = secondaryName.replace("_102X_mcRun2_asymptotic_v7","") #REMOVE GT. CHECK ITS UPDATED
    secondaryName = secondaryName.replace("PUMoriond17","")  #CHECK
    secondaryName = secondaryName.replace("-v1","")# 
    secondaryName = secondaryName.replace("-v2","")# Remove any version indication.There should only be one valid version for MC samples
    #
    requestName = primaryName + "_" + secondaryName
    requestName = crab_common.reqNamePrefix +"_" + requestName + "_" + crab_common.version
    crab_common.config.General.requestName   = requestName
    #  
    outputDatasetTag = crab_common.reqNamePrefix +"_" + secondaryName + "_" + crab_common.version
    crab_common.config.Data.outputDatasetTag = outputDatasetTag 
    #
    print "requestName: ", requestName 
    print "outputDatasetTag: ", outputDatasetTag
    crabCommand('submit', config = crab_2016_common.config)
    print ""
