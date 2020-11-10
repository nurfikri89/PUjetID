import sys
import crab_common 
import helpers

crab_common.config.JobType.maxJobRuntimeMin = 600

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

  from CRABAPI.RawCommand import crabCommand
  for i, dataset in enumerate(samplelist):
    print "%d/%d:Sending CRAB job: %s" % (i+1,len(samplelist), dataset)
    crab_common.config.Data.inputDataset = dataset
    #
    #
    #
    crab_common.config.JobType.scriptArgs = [
      'era=UL2017',#CHECK
      'isMC=1',
      'dataStream=MC',
    ]
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
    secondaryName = secondaryName.replace("algomez-","")#CHECK
    secondaryName = secondaryName.replace("RunIISummer19UL17JMEnanoV1","MCUL17JMEnanoV1")#CHECK
    secondaryName = secondaryName.replace("-106X_mc2017_realistic_v6","")#CHECK
    secondaryName = secondaryName.replace("-v1","")#CHECK
    secondaryName = secondaryName.replace("-v2","")#CHECK
    secondaryName = secondaryName.replace("-1c822544b349959fbcd74e91edede2d7","")#CHECK
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
    crabCommand('submit', config = crab_common.config)
    print ""