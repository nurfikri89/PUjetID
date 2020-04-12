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

## Produce histograms for template fits

All the scripts required to make the histogram templates are in the [**Analyzer**](./Analyzer) directory.

>**:exclamation:IMPORTANT** You need to use ROOT version ```6.18``` or later. You can setup the environment 
to version ```6.18.04``` by sourcing the [```sourceRecentROOT.sh```](./Analyzer/sourceRecentROOT.py) 
bash script. The bash script will also unset the CMSSW runtime environment if you had done ```cmsenv```earlier. 
This ensures there are no conflicts between the ROOT version that you have just set up and the version in CMSSW.

Producing the histograms is a two-step process. The steps are:

1. Make skimmed ntuples for skimmed NanoAODs by using the [```SkimNtuples.py```](./Analyzer/SkimNtuples.py) script. This will make the histogram making step faster. Example to run the script can be found in [```RunLocal_SkimNtuples.sh```](./Analyzer/RunLocal_SkimNtuples.sh).

2. Make histograms by running over the ntuples with the [```MakeHistograms.py```](./Analyzer/MakeHistograms.py) script. Example to run the script can be found in [```RunLocal_MakeHistograms.sh```](./Analyzer/RunLocal_MakeHistograms.sh) bash script.

The histograms will be saved in the ```histos``` directory. Run [```haddHistos.sh```](./Analyzer/RunLocal_MakeHistograms.sh) to merge all Data histograms for each year. The paths to the skimmed NanoAODs and skimmed ntuples are specified 
in[```SampleList.py```](./Analyzer/SampleList.py).



