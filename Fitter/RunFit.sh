#
# Directory path containing all the histogram rootfiles
#
INDIR="./input/DiLeptonSkim_v4p1/"

#
# Directory path for the output of the fits
#
OUTDIR="./results_v4p1/"


function RunFitter {
  python extract_fit.py --input ${1} --output ${2}/${3}_WPLoose/  --year ${3} --wp Loose
  python extract_fit.py --input ${1} --output ${2}/${3}_WPMedium/ --year ${3} --wp Medium
  python extract_fit.py --input ${1} --output ${2}/${3}_WPTight/  --year ${3} --wp Tight
}

YEAR="2016"
RunFitter ${INDIR} ${OUTDIR} ${YEAR}

YEAR="2017"
RunFitter ${INDIR} ${OUTDIR} ${YEAR}

YEAR="2018"
RunFitter ${INDIR} ${OUTDIR} ${YEAR}


function RunFitterNLO {
  python extract_fit.py --useNLO --input ${1} --output ${2}/${3}_WPLoose/  --year ${3} --wp Loose
  python extract_fit.py --useNLO --input ${1} --output ${2}/${3}_WPMedium/ --year ${3} --wp Medium
  python extract_fit.py --useNLO --input ${1} --output ${2}/${3}_WPTight/  --year ${3} --wp Tight
}

# YEAR="2016"
# RunFitterNLO ${INDIR} ${OUTDIR} ${YEAR}

# YEAR="2017"
# RunFitterNLO ${INDIR} ${OUTDIR} ${YEAR}

# YEAR="2018"
# RunFitterNLO ${INDIR} ${OUTDIR} ${YEAR}


function RunFitterHerwig {
  python extract_fit.py --useHerwig --input ${1} --output ${2}/${3}_WPLoose/  --year ${3} --wp Loose
  python extract_fit.py --useHerwig --input ${1} --output ${2}/${3}_WPMedium/ --year ${3} --wp Medium
  python extract_fit.py --useHerwig --input ${1} --output ${2}/${3}_WPTight/  --year ${3} --wp Tight
}

# YEAR="2016"
# RunFitterHerwig ${INDIR} ${OUTDIR} ${YEAR}

# YEAR="2017"
# RunFitterHerwig ${INDIR} ${OUTDIR} ${YEAR}

# YEAR="2018"
# RunFitterHerwig ${INDIR} ${OUTDIR} ${YEAR}