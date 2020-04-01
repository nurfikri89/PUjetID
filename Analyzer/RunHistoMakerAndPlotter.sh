rm -rf Data16_VS_MG 
rm -rf histos 

python MakeHistograms.py
python PlotHistograms.py

rm -rf ~/EOS/www/Data16_VS_MG 
rm -rf ~/EOS/www/histos     
cp -r Data16_VS_MG ~/EOS/www/
cp -r histos ~/EOS/www/