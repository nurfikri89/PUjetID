INDIR="./input/DiMuonSkim_v2/"
OUTDIR="./results/"

python extract_fit.py  --input ${INDIR}  --output ${OUTDIR}/2016_WPLoose/  --year 2016 --wp Loose
python extract_fit.py  --input ${INDIR}  --output ${OUTDIR}/2016_WPMedium/ --year 2016 --wp Medium
python extract_fit.py  --input ${INDIR}  --output ${OUTDIR}/2016_WPTight/  --year 2016 --wp Tight
