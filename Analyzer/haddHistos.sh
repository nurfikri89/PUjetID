#
# combine all data histos into one root file
#
hadd -f histos/Histo_Data16.root histos/Histo_Data16*_DoubleMuon.root
hadd -f histos/Histo_Data17.root histos/Histo_Data17*_DoubleMuon.root
hadd -f histos/Histo_Data18.root histos/Histo_Data18*_DoubleMuon.root
