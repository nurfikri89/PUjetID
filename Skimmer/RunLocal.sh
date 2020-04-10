MAX_EVENTS=50000
#
#
#
python RunSkimmerLocal.py \
--era="2016" \
--isMC=1 \
--maxEvents=${MAX_EVENTS} \
--outDir="./MC16_DYJetsToLL_LO"
# 
# 
# 
python RunSkimmerLocal.py \
--era="2016" \
--isMC=0 \
--maxEvents=${MAX_EVENTS} \
--outDir="./Data16H_DoubleMuon"
