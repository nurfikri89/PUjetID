MAX_EVENTS=50000
#
#
python RunSkimmerLocal.py \
--era="2016" \
--maxEvents=${MAX_EVENTS} \
--outDir="./MC16_DYJetsToLL_NLO" \
--isMC=1 \
--dataStream="MC"
#
#
python RunSkimmerLocal.py \
--era="2016" \
--maxEvents=${MAX_EVENTS} \
--outDir="./Data16_DoubleMuon" \
--isMC=0 \
--dataStream="DoubleMuon"
#
#
python RunSkimmerLocal.py \
--era="2016" \
--maxEvents=${MAX_EVENTS} \
--outDir="./Data16_DoubleEG" \
--isMC=0 \
--dataStream="DoubleEG"
