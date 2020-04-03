#
# creat batchlog directory
#
mkdir -p BatchLog
#
# copy file and change WORKDIR string in the file to path to current directory
#
cp ./batchscripts/MakeHistoAtBatch.sh .
REPLACE="${PWD}"
sed -i "s|REPLACEME|${REPLACE}|g" ./MakeHistoAtBatch.sh
#
#
#
cp ./batchscripts/MakeHistoAtBatch.sh.sub .
