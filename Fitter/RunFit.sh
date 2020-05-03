#
# Directory path containing all the histogram rootfiles
#
INDIR="./input/DiMuonSkim_v3/"
#
# Directory path for the output of the fits
#
OUTDIR="./results_v3/"

python extract_fit.py  --input ${INDIR}  --output ${OUTDIR}/2016_WPLoose/  --year 2016 --wp Loose
python extract_fit.py  --input ${INDIR}  --output ${OUTDIR}/2016_WPMedium/ --year 2016 --wp Medium
python extract_fit.py  --input ${INDIR}  --output ${OUTDIR}/2016_WPTight/  --year 2016 --wp Tight
