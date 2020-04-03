# Pileup JetID


## Setup framework

Setup a CMSSW release:
```
mkdir PileUpJetIDSF
cd PileUpJetIDSF
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
```
Checkout [nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools):
```
git clone git@github.com:cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
```
Checkout this framework and switch to this branch:
```
git clone git@github.com:cms-jet/PUjetID.git PUjetID
cd PUjetID
git checkout eff_analysis_nano_run2
cd ${CMSSW_BASE}/src
```
and then compile:
```
scram b -j4
```

## Producing skimmed NanoAODs

