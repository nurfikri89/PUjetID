
# python SkimNtuples.py --sample MC16_DY_MG --cores 4
# python SkimNtuples.py --sample MC16_DY_AMCNLO --cores 4
# python SkimNtuples.py --sample Data16B_DoubleMuon --cores 4
# python SkimNtuples.py --sample Data16C_DoubleMuon --cores 4
# python SkimNtuples.py --sample Data16D_DoubleMuon --cores 4
# python SkimNtuples.py --sample Data16E_DoubleMuon --cores 4
# python SkimNtuples.py --sample Data16F_DoubleMuon --cores 4
# python SkimNtuples.py --sample Data16G_DoubleMuon --cores 4
# python SkimNtuples.py --sample Data16H_DoubleMuon --cores 4

python MakeHistograms.py --sample MC16_DY_MG --cores 4
python MakeHistograms.py --sample MC16_DY_AMCNLO --cores 4
python MakeHistograms.py --sample Data16B_DoubleMuon --cores 4
python MakeHistograms.py --sample Data16C_DoubleMuon --cores 4
python MakeHistograms.py --sample Data16D_DoubleMuon --cores 4
python MakeHistograms.py --sample Data16E_DoubleMuon --cores 4
python MakeHistograms.py --sample Data16F_DoubleMuon --cores 4
python MakeHistograms.py --sample Data16G_DoubleMuon --cores 4
python MakeHistograms.py --sample Data16H_DoubleMuon --cores 4
