MAX_EVENTS=10000
#
#
#
python RunSkimmerLocal.py \
--era="2016" \
--isMC=1 \
--maxEvents=${MAX_EVENTS} \
--outDir="./MC2016_DYLL"
#
#
#
python RunSkimmerLocal.py \
--era="2016" \
--isMC=0 \
--maxEvents=${MAX_EVENTS} \
--outDir="./Data2016_DoubleMuon"
