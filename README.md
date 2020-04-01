# Pileup JetID

Repository for training, validation and store the weights for pileup jet ID.
For more information please visit the twiki [PileupJetID](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID).

## For users

The latest version of the weights is [94X_weights_DYJets_inc_v2](https://github.com/cms-jet/PUjetID/tree/94X_weights_DYJets_inc_v2). More instructions in the README.md file of the branch.


## For developers

This is the _master_ branch, which only contains information about the package. 
 * [94X_weights_DYJets_inc_v2](https://github.com/cms-jet/PUjetID/tree/94X_weights_DYJets_inc_v2) is the latest version for 2018 data.
 * [fromJMEValidator](https://github.com/cms-jet/PUjetID/tree/fromJMEValidator) is the latest version for 2016 data.


### 0. Setup CMSSW release

Setup a CMSSW release:
```
mkdir PUJetIdStudies
cd PUJetIdStudies
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_15
cd CMSSW_10_2_15/src
cmsenv
```

### 1. Checkout packages and compile

Checkout this framework and [nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools):
```
git clone git@github.com:abuubaidah89/PUjetID.git PUjetID
git clone git@github.com:cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
```
and then compile:
```
scram b -j4
```

### 2. Producing skimmed NanoAOD

### 3. Make histograms from skimmed NanoAOD

Only on lxplus7, source to the following Root for compatibality with RDataFrame. It is also best to do this in a new shell (without running cmsenv) to avoid any complication:
```
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.18.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh
```
Run the MakeHistograms script:
```
cd PUJetID/Analyzer/
python MakeHistograms.py
```
Plot the histograms:
```
python PlotHistograms.py
```
