
NCORES=4

SAMPLES=(
MC16_DY_MG        
# MC16_DY_AMCNLO    
# Data16B_DoubleMuon
# Data16C_DoubleMuon
# Data16D_DoubleMuon
# Data16E_DoubleMuon
# Data16F_DoubleMuon
# Data16G_DoubleMuon
# Data16H_DoubleMuon
)


for SAMPLE in ${SAMPLES[@]}
do
  python SkimNtuples.py --sample $SAMPLE --cores $NCORES
  # python MakeHistograms.py  --sample $SAMPLE --cores $NCORES
done



