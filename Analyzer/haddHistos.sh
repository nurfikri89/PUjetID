#
# combine all data histos into one root file
#
HISTODIR="histos"

hadd -f ${HISTODIR}/Histo_DataUL17.root ${HISTODIR}/Histo_DataUL17*.root

# hadd -f ${HISTODIR}/Histo_Data16.root ${HISTODIR}/Histo_Data16*.root
# hadd -f ${HISTODIR}/Histo_Data17.root ${HISTODIR}/Histo_Data17*.root
# hadd -f ${HISTODIR}/Histo_Data18.root ${HISTODIR}/Histo_Data18*.root
