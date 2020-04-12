#!/bin/bash
NCORES=4

SAMPLES=(
MC16_DY_MG
MC17_DY_MG
MC18_DY_MG
MC16_DY_AMCNLO
MC17_DY_AMCNLO
MC18_DY_AMCNLO
Data16B_DoubleMuon
Data16C_DoubleMuon
Data16D_DoubleMuon
Data16E_DoubleMuon
Data16F_DoubleMuon
Data16G_DoubleMuon
Data16H_DoubleMuon
Data17B_DoubleMuon
Data17C_DoubleMuon
Data17D_DoubleMuon
Data17E_DoubleMuon
Data17F_DoubleMuon
Data18A_DoubleMuon
Data18B_DoubleMuon
Data18C_DoubleMuon
Data18D_DoubleMuon
)
#
# Make skimmed ntuples
#
for SAMPLE in ${SAMPLES[@]}
do
  python SkimNtuples.py --sample $SAMPLE --cores $NCORES
done
