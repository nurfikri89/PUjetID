# Standard importts
import os,sys,socket,argparse
import os
import ROOT
import math
from array import array
import numpy as np


ROOT.gROOT.SetBatch(True)

# RooFit
ROOT.gSystem.Load("libRooFit.so")
ROOT.gSystem.Load("libRooFitCore.so")
ROOT.gROOT.SetStyle("Plain") # Not sure this is needed
ROOT.gSystem.SetIncludePath( "-I$ROOFITSYS/include/" )



'''
The general idea is to extract the efficiency and mistag rate of the PU ID based on a fit to the dphi(Z,jet) distribution. 
4 dphi(Z,jet) distributions are fitted simultaneously: 
-Passing or failing jets with good/bad  pt balance with the Z boson.

The fit uses up to 8 histograms (1 signal and 1 PU template per fitted distribution):
- h_dphi_genunmatched_PASS/FAIL: distribution for jets not matched to a gen jet and failing/passing the PU ID working point under study. At the moment these templates are not used and replaced by a flat distribution.
- h_dphi_genmatched_PASS/FAIL: Same for jets matched to a gen jet 
- Same plots with the suffix "badbalance": similar templates, obtained using Z+jets events where the pt(Z)/pt(j) balance is bad. 
'''

def MakeDPhiFit(
        h_dphi_genunmatched_PASS,h_dphi_genmatched_PASS,h_dphi_genunmatched_FAIL,h_dphi_genmatched_FAIL,h_dphi_PASS,h_dphi_FAIL, 
        h_dphi_genunmatched_PASS_badbalance,h_dphi_genmatched_PASS_badbalance,h_dphi_genunmatched_FAIL_badbalance,h_dphi_genmatched_FAIL_badbalance,h_dphi_PASS_badbalance,h_dphi_FAIL_badbalance, 
        output, pt, eta, binning, isData=False):


    print "Performing fits to extract efficiency and mistag rate" 
    print("entries in histos "+str(h_dphi_genunmatched_PASS.GetEntries())+","+str(h_dphi_genmatched_PASS.GetEntries())+","+str(h_dphi_genunmatched_FAIL.GetEntries())+","+str(h_dphi_genmatched_FAIL.GetEntries())+","+str(h_dphi_PASS.GetEntries())+","+str(h_dphi_FAIL.GetEntries()))
    print(pt+eta) 
    
    #Declare the observable and effcy/mistag
    dphiZjet = ROOT.RooRealVar("dphiZjet","#Delta#phi(Z,jet)/#pi",0., 2.) ;
    effcy = ROOT.RooRealVar("effcy","effcy",0.9, 0.,1.) ;
    mistag = ROOT.RooRealVar("mistag","mistag",0.1, 0.,1.) ;


    ################# What follows concerns the first 4 templates (good jet/Z pt balance) #################
    #Total nb of events, of signal (=real jets) events , of PU events
    nbtot =  ROOT.RooRealVar("nbtot","nbtot",h_dphi_PASS.Integral() + h_dphi_FAIL .Integral());
    nbtotsig =  ROOT.RooRealVar("nbtotsig","nbtotsig", 1., h_dphi_PASS.Integral() + h_dphi_FAIL .Integral() );
    nbtotpu = ROOT.RooFormulaVar("nbtotpu","nbtot-nbtotsig",ROOT.RooArgList(nbtot,nbtotsig));

    #Nb of events from each category passing/failing the PU ID 
    n_SIG_PASS = ROOT.RooFormulaVar("n_SIG_PASS","effcy*nbtotsig",ROOT.RooArgList(effcy,nbtotsig));
    n_PU_PASS = ROOT.RooFormulaVar("n_PU_PASS","mistag*nbtotpu",ROOT.RooArgList(mistag,nbtotpu)); 
    n_SIG_FAIL = ROOT.RooFormulaVar("n_SIG_FAIL","(1-effcy)*nbtotsig",ROOT.RooArgList(effcy,nbtotsig));
    n_PU_FAIL = ROOT.RooFormulaVar("n_PU_FAIL","(1-mistag)*nbtotpu",ROOT.RooArgList(mistag,nbtotpu));

    #Import the data histograms
    dh_dphiZjet_PASS = ROOT.RooDataHist("dh_dphiZjet_PASS"  ,"dh_dphiZjet_PASS"  ,ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_PASS)) ;
    dh_dphiZjet_FAIL = ROOT.RooDataHist("dh_dphiZjet_FAIL"  ,"dh_dphiZjet_FAIL"  ,ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_FAIL)) ;

    #Define the pdf: 
    #First import the histos templates
    dh_template_SIG_PASS  = ROOT.RooDataHist("dh_template_SIG_PASS",  "dh_template_SIG_PASS" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genmatched_PASS)) ;
    dh_template_SIG_FAIL  = ROOT.RooDataHist("dh_template_SIG_FAIL",  "dh_template_SIG_FAIL" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genmatched_FAIL)) ;
    dh_template_PU_PASS  = ROOT.RooDataHist("dh_template_PU_PASS",  "dh_template_PU_PASS" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genunmatched_PASS)) ;
    dh_template_PU_FAIL  = ROOT.RooDataHist("dh_template_PU_FAIL",  "dh_template_PU_FAIL" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genunmatched_FAIL)) ;

    #Now convert them to PDF:
    pdf_template_SIG_PASS  = ROOT.RooHistPdf("pdf_template_SIG_PASS",  "pdf_template_SIG_PASS" , ROOT.RooArgSet(dphiZjet),dh_template_SIG_PASS);
    pdf_template_SIG_FAIL  = ROOT.RooHistPdf("pdf_template_SIG_FAIL",  "pdf_template_SIG_FAIL" , ROOT.RooArgSet(dphiZjet),dh_template_SIG_FAIL);
    pdf_template_PU_PASS  = ROOT.RooHistPdf("pdf_template_PU_PASS",  "pdf_template_PU_PASS" , ROOT.RooArgSet(dphiZjet),dh_template_PU_PASS);
    pdf_template_PU_FAIL  = ROOT.RooHistPdf("pdf_template_PU_FAIL",  "pdf_template_PU_FAIL" , ROOT.RooArgSet(dphiZjet),dh_template_PU_FAIL);

    #The PU template is taken to be a flat (pol0) distribution
    pol0_PU_PASS = ROOT.RooPolynomial("pol0_PU_PASS","pol0",dphiZjet, ROOT.RooArgList());
    pol0_PU_FAIL = ROOT.RooPolynomial("pol0_PU_FAIL","pol0",dphiZjet, ROOT.RooArgList());


    #Smears the signal with a Gaussian to allow for different phi resolution between data and simulation. 
    gauss_mean_PASS  = ROOT.RooRealVar("mean_PASS","mean",0,-0.05,0.05)
    gauss_sigma_PASS = ROOT.RooRealVar("sigma_PASS","sigma gauss",0.02,0.001,0.2)
    gauss_PASS       = ROOT.RooGaussian("gauss_PASS","gauss", dphiZjet ,gauss_mean_PASS,gauss_sigma_PASS) 
    tmpxg_SIG_PASS = ROOT.RooFFTConvPdf("tmpxg_SIG_PASS","template x gauss" ,dphiZjet, pdf_template_SIG_PASS , gauss_PASS)
    gauss_mean_FAIL  = ROOT.RooRealVar("mean_FAIL","mean",0,-0.05,0.05)
    gauss_sigma_FAIL = ROOT.RooRealVar("sigma_FAIL","sigma gauss",0.02,0.001,0.2)
    gauss_FAIL       = ROOT.RooGaussian("gauss_FAIL","gauss", dphiZjet ,gauss_mean_FAIL,gauss_sigma_FAIL) 
    tmpxg_SIG_FAIL = ROOT.RooFFTConvPdf("tmpxg_SIG_FAIL","template x gauss" ,dphiZjet, pdf_template_SIG_FAIL , gauss_FAIL)

    #Smears the PU template template with a Gaussian to allow for different phi resolution between data and simulation.  Not needed if the template is a flat distribution.  
    gauss_mean_PUPASS  = ROOT.RooRealVar("mean_PUPASS","mean",0,-0.05,0.05)
    gauss_sigma_PUPASS = ROOT.RooRealVar("sigma_PUPASS","sigma gauss",0.02,0.001,0.2)
    gauss_PUPASS       = ROOT.RooGaussian("gauss_PUPASS","gauss", dphiZjet ,gauss_mean_PUPASS,gauss_sigma_PUPASS) 
    tmpxg_PU_PASS = ROOT.RooFFTConvPdf("tmpxg_PU_PASS","template x gauss" ,dphiZjet, pdf_template_PU_PASS , gauss_PUPASS)
    gauss_mean_PUFAIL  = ROOT.RooRealVar("mean_PUFAIL","mean",0,-0.05,0.05)
    gauss_sigma_PUFAIL = ROOT.RooRealVar("sigma_PUFAIL","sigma gauss",0.02,0.001,0.2)
    gauss_PUFAIL       = ROOT.RooGaussian("gauss_PUFAIL","gauss", dphiZjet ,gauss_mean_PUFAIL,gauss_sigma_PUFAIL) 
    tmpxg_PU_FAIL = ROOT.RooFFTConvPdf("tmpxg_PU_FAIL","template x gauss" ,dphiZjet, pdf_template_PU_FAIL , gauss_PUFAIL)


    #Convert to extended pdf 
    extpdf_SIG_PASS    = ROOT.RooExtendPdf("extpdf_SIG_PASS"   , "extpdf_SIG_PASS"   , tmpxg_SIG_PASS   , n_SIG_PASS) 
    extpdf_SIG_FAIL    = ROOT.RooExtendPdf("extpdf_SIG_FAIL"   , "extpdf_SIG_FAIL"   , tmpxg_SIG_FAIL   , n_SIG_FAIL) 
    extpdf_PU_PASS    = ROOT.RooExtendPdf("extpdf_PU_PASS"   , "extpdf_PU_PASS"   ,  pol0_PU_PASS , n_PU_PASS)
    extpdf_PU_FAIL    = ROOT.RooExtendPdf("extpdf_PU_FAIL"   , "extpdf_PU_FAIL"   ,  pol0_PU_FAIL , n_PU_FAIL)
    
    #PU+SIG PDF
    extpdf_SIGandPU_PASS = ROOT.RooAddPdf("extpdf_SIGandPU_PASS", "Signal+PU PDF (PASS)", ROOT.RooArgList(extpdf_SIG_PASS,extpdf_PU_PASS),ROOT.RooArgList(n_SIG_PASS,n_PU_PASS));
    extpdf_SIGandPU_FAIL = ROOT.RooAddPdf("extpdf_SIGandPU_FAIL", "Signal+PU PDF (FAIL)", ROOT.RooArgList(extpdf_SIG_FAIL,extpdf_PU_FAIL),ROOT.RooArgList(n_SIG_FAIL,n_PU_FAIL));

    
    ################# Same procedure for templates with bad balance ################# 
    #Total nb of events, of signal (=real jets) events , of PU events       
    nbtot_badbalance =  ROOT.RooRealVar("nbtot_badbalance","nbtot_badbalance",h_dphi_PASS_badbalance.Integral() + h_dphi_FAIL_badbalance .Integral());
    nbtotsig_badbalance =  ROOT.RooRealVar("nbtotsig_badbalance","nbtotsig_badbalance", 1., h_dphi_PASS_badbalance.Integral() + h_dphi_FAIL_badbalance .Integral() );
    nbtotpu_badbalance = ROOT.RooFormulaVar("nbtotpu_badbalance","nbtot_badbalance-nbtotsig_badbalance",ROOT.RooArgList(nbtot_badbalance,nbtotsig_badbalance));
    #Nb of events from each category passing/failing the PU ID
    n_SIG_PASS_badbalance = ROOT.RooFormulaVar("n_SIG_PASS_badbalance","effcy*nbtotsig_badbalance",ROOT.RooArgList(effcy,nbtotsig_badbalance));
    n_PU_PASS_badbalance = ROOT.RooFormulaVar("n_PU_PASS_badbalance","mistag*nbtotpu_badbalance",ROOT.RooArgList(mistag,nbtotpu_badbalance));
    n_SIG_FAIL_badbalance = ROOT.RooFormulaVar("n_SIG_FAIL_badbalance","(1-effcy)*nbtotsig_badbalance",ROOT.RooArgList(effcy,nbtotsig_badbalance));
    n_PU_FAIL_badbalance = ROOT.RooFormulaVar("n_PU_FAIL_badbalance","(1-mistag)*nbtotpu_badbalance",ROOT.RooArgList(mistag,nbtotpu_badbalance));
    
    #Import the data histograms  
    dh_dphiZjet_PASS_badbalance = ROOT.RooDataHist("dh_dphiZjet_PASS_badbalance"  ,"dh_dphiZjet_PASS_badbalance"  ,ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_PASS_badbalance)) ;
    dh_dphiZjet_FAIL_badbalance = ROOT.RooDataHist("dh_dphiZjet_FAIL_badbalance"  ,"dh_dphiZjet_FAIL_badbalance"  ,ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_FAIL_badbalance)) ;
    #Define the pdf:                   
    #First import the histos templates
    dh_template_SIG_PASS_badbalance  = ROOT.RooDataHist("dh_template_SIG_PASS_badbalance",  "dh_template_SIG_PASS_badbalance" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genmatched_PASS_badbalance)) ;
    dh_template_SIG_FAIL_badbalance  = ROOT.RooDataHist("dh_template_SIG_FAIL_badbalance",  "dh_template_SIG_FAIL_badbalance" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genmatched_FAIL_badbalance)) ;
    dh_template_PU_PASS_badbalance  = ROOT.RooDataHist("dh_template_PU_PASS_badbalance",  "dh_template_PU_PASS_badbalance" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genunmatched_PASS_badbalance)) ;
    dh_template_PU_FAIL_badbalance  = ROOT.RooDataHist("dh_template_PU_FAIL_badbalance",  "dh_template_PU_FAIL_badbalance" , ROOT.RooArgList(dphiZjet),ROOT.RooFit.Import(h_dphi_genunmatched_FAIL_badbalance)) ;
    
    #Now convert them to PDF:
    pdf_template_SIG_PASS_badbalance  = ROOT.RooHistPdf("pdf_template_SIG_PASS_badbalance",  "pdf_template_SIG_PASS_badbalance" , ROOT.RooArgSet(dphiZjet),dh_template_SIG_PASS_badbalance);
    pdf_template_SIG_FAIL_badbalance  = ROOT.RooHistPdf("pdf_template_SIG_FAIL_badbalance",  "pdf_template_SIG_FAIL_badbalance" , ROOT.RooArgSet(dphiZjet),dh_template_SIG_FAIL_badbalance);
    pdf_template_PU_PASS_badbalance  = ROOT.RooHistPdf("pdf_template_PU_PASS_badbalance",  "pdf_template_PU_PASS_badbalance" , ROOT.RooArgSet(dphiZjet),dh_template_PU_PASS_badbalance);
    pdf_template_PU_FAIL_badbalance  = ROOT.RooHistPdf("pdf_template_PU_FAIL_badbalance",  "pdf_template_PU_FAIL_badbalance" , ROOT.RooArgSet(dphiZjet),dh_template_PU_FAIL_badbalance);
     #The PU template is taken to be a flat (pol0) distribution   
    pol0_PU_PASS_badbalance = ROOT.RooPolynomial("pol0_PU_PASS_badbalance","pol0",dphiZjet, ROOT.RooArgList());
    pol0_PU_FAIL_badbalance = ROOT.RooPolynomial("pol0_PU_FAIL_badbalance","pol0",dphiZjet, ROOT.RooArgList());
    
    #Smears the signal with a Gaussian to allow for different phi resolution between data and simulation.  
    gauss_mean_PASS_badbalance  = ROOT.RooRealVar("mean_PASS_badbalance","mean",0,-0.05,0.05)
    gauss_sigma_PASS_badbalance = ROOT.RooRealVar("sigma_PASS_badbalance","sigma gauss",0.02,0.001,0.2)
    gauss_PASS_badbalance       = ROOT.RooGaussian("gauss_PASS_badbalance","gauss", dphiZjet ,gauss_mean_PASS_badbalance,gauss_sigma_PASS_badbalance)
    tmpxg_SIG_PASS_badbalance = ROOT.RooFFTConvPdf("tmpxg_SIG_PASS_badbalance","template x gauss" ,dphiZjet, pdf_template_SIG_PASS_badbalance , gauss_PASS_badbalance)
    
    #Smears the PU template template with a Gaussian to allow for different phi resolution between data and simulation.  Not needed if the template is a flat distribution. 
    gauss_mean_FAIL_badbalance  = ROOT.RooRealVar("mean_FAIL_badbalance","mean",0,-0.05,0.05)
    gauss_sigma_FAIL_badbalance = ROOT.RooRealVar("sigma_FAIL_badbalance","sigma gauss",0.02,0.001,0.2)
    gauss_FAIL_badbalance       = ROOT.RooGaussian("gauss_FAIL_badbalance","gauss", dphiZjet ,gauss_mean_FAIL_badbalance,gauss_sigma_FAIL_badbalance)
    tmpxg_SIG_FAIL_badbalance = ROOT.RooFFTConvPdf("tmpxg_SIG_FAIL_badbalance","template x gauss" ,dphiZjet, pdf_template_SIG_FAIL_badbalance , gauss_FAIL_badbalance)
    extpdf_SIG_PASS_badbalance    = ROOT.RooExtendPdf("extpdf_SIG_PASS_badbalance"   , "extpdf_SIG_PASS"   , tmpxg_SIG_PASS_badbalance   , n_SIG_PASS_badbalance)
    extpdf_SIG_FAIL_badbalance    = ROOT.RooExtendPdf("extpdf_SIG_FAIL_badbalance"   , "extpdf_SIG_FAIL"   , tmpxg_SIG_FAIL_badbalance   , n_SIG_FAIL_badbalance)

    
    #Convert to extended pdf 
    extpdf_PU_PASS_badbalance    = ROOT.RooExtendPdf("extpdf_PU_PASS_badbalance"   , "extpdf_PU_PASS"   ,  pol0_PU_PASS_badbalance , n_PU_PASS_badbalance)
    extpdf_PU_FAIL_badbalance    = ROOT.RooExtendPdf("extpdf_PU_FAIL_badbalance"   , "extpdf_PU_FAIL"   ,  pol0_PU_FAIL_badbalance , n_PU_FAIL_badbalance)
    extpdf_SIGandPU_PASS_badbalance = ROOT.RooAddPdf("extpdf_SIGandPU_PASS_badbalance", "Signal+PU PDF (PASS)", ROOT.RooArgList(extpdf_SIG_PASS_badbalance,extpdf_PU_PASS_badbalance),ROOT.RooArgList(n_SIG_PASS_badbalance,n_PU_PASS_badbalance));
    extpdf_SIGandPU_FAIL_badbalance = ROOT.RooAddPdf("extpdf_SIGandPU_FAIL_badbalance", "Signal+PU PDF (FAIL)", ROOT.RooArgList(extpdf_SIG_FAIL_badbalance,extpdf_PU_FAIL_badbalance),ROOT.RooArgList(n_SIG_FAIL_badbalance,n_PU_FAIL_badbalance));
    
    
    #Now we are ready to perform the simultaneous fit to all distributions. 
    
    sample = ROOT.RooCategory("sample","sample") ;
    sample.defineType("PASSsample") ;
    sample.defineType("FAILsample") ;
    sample.defineType("PASSsample_badbalance") ;
    sample.defineType("FAILsample_badbalance") ;
    
    combData = ROOT.RooDataHist("allevents","PASS+FAIL",
                                ROOT.RooArgList(dphiZjet),ROOT.RooFit.Index(sample),
                                ROOT.RooFit.Import("PASSsample",dh_dphiZjet_PASS),
                                ROOT.RooFit.Import("FAILsample",dh_dphiZjet_FAIL) ,
                                ROOT.RooFit.Import("PASSsample_badbalance",dh_dphiZjet_PASS_badbalance),
                                ROOT.RooFit.Import("FAILsample_badbalance",dh_dphiZjet_FAIL_badbalance)  
    );
    
    simultpdf = ROOT.RooSimultaneous("simultpdf","simultaneous pdf",sample) ;
    simultpdf.addPdf(extpdf_SIGandPU_PASS,"PASSsample") ;
    simultpdf.addPdf(extpdf_SIGandPU_FAIL,"FAILsample") ;
    simultpdf.addPdf(extpdf_SIGandPU_PASS_badbalance,"PASSsample_badbalance") ;
    simultpdf.addPdf(extpdf_SIGandPU_FAIL_badbalance,"FAILsample_badbalance") ;
    
    simultpdf.fitTo(combData,ROOT.RooFit.Save())
    simultpdf.fitTo(combData,ROOT.RooFit.Save())

    
    ROOT.gStyle.SetTitleStyle(0)
    ROOT.gStyle.SetTitleBorderSize(0)

    #Plots the fits in various frames. 
    framePASS        = dphiZjet.frame(ROOT.RooFit.Title("Passing events"))
    if isData:
        combData.plotOn(framePASS,ROOT.RooFit.Cut("sample==sample::PASSsample"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.FillStyle(0)) ;
    else:
        combData.plotOn(framePASS,ROOT.RooFit.Cut("sample==sample::PASSsample"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2),ROOT.RooFit.FillStyle(0)) ;
    
    simultpdf.plotOn(framePASS,ROOT.RooFit.Slice(sample,"PASSsample"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData));
    simultpdf.plotOn(framePASS,ROOT.RooFit.Slice(sample,"PASSsample"),ROOT.RooFit.Components("extpdf_PU_PASS"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData),ROOT.RooFit.LineStyle(ROOT.kDashed));
    framePASS.SetMaximum(framePASS.GetMaximum()*1.25)


    frameFAIL        = dphiZjet.frame(ROOT.RooFit.Title("Failing events"))
    if isData:
        combData.plotOn(frameFAIL,ROOT.RooFit.Cut("sample==sample::FAILsample"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.FillStyle(0)) ;
    else:
        combData.plotOn(frameFAIL,ROOT.RooFit.Cut("sample==sample::FAILsample"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2),ROOT.RooFit.FillStyle(0)) ;

    simultpdf.plotOn(frameFAIL,ROOT.RooFit.Slice(sample,"FAILsample"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData));
    simultpdf.plotOn(frameFAIL,ROOT.RooFit.Slice(sample,"FAILsample"),ROOT.RooFit.Components("extpdf_PU_FAIL"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData),ROOT.RooFit.LineStyle(ROOT.kDashed));    
    frameFAIL.SetMaximum(frameFAIL.GetMaximum()*1.25)


    framePASS_badbalance        = dphiZjet.frame(ROOT.RooFit.Title("Passing events"))
    if isData:
        combData.plotOn(framePASS_badbalance,ROOT.RooFit.Cut("sample==sample::PASSsample_badbalance"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.FillStyle(0)) ;
    else:
        combData.plotOn(framePASS_badbalance,ROOT.RooFit.Cut("sample==sample::PASSsample_badbalance"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2),ROOT.RooFit.FillStyle(0)) ;
    
    simultpdf.plotOn(framePASS_badbalance,ROOT.RooFit.Slice(sample,"PASSsample_badbalance"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData));
    simultpdf.plotOn(framePASS_badbalance,ROOT.RooFit.Slice(sample,"PASSsample_badbalance"),ROOT.RooFit.Components("extpdf_PU_PASS_badbalance"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData),ROOT.RooFit.LineStyle(ROOT.kDashed));
    framePASS_badbalance.SetMaximum(framePASS_badbalance.GetMaximum()*1.25)


    frameFAIL_badbalance        = dphiZjet.frame(ROOT.RooFit.Title("Failing events"))
    if isData:
        combData.plotOn(frameFAIL_badbalance,ROOT.RooFit.Cut("sample==sample::FAILsample_badbalance"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.FillStyle(0)) ;
    else:
        combData.plotOn(frameFAIL_badbalance,ROOT.RooFit.Cut("sample==sample::FAILsample_badbalance"),ROOT.RooFit.MarkerSize(0.7),ROOT.RooFit.MarkerStyle(20),ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2),ROOT.RooFit.FillStyle(0)) ;

    simultpdf.plotOn(frameFAIL_badbalance,ROOT.RooFit.Slice(sample,"FAILsample_badbalance"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData));
    simultpdf.plotOn(frameFAIL_badbalance,ROOT.RooFit.Slice(sample,"FAILsample_badbalance"),ROOT.RooFit.Components("extpdf_PU_FAIL_badbalance"),ROOT.RooFit.ProjWData(ROOT.RooArgSet(sample),combData),ROOT.RooFit.LineStyle(ROOT.kDashed));
    frameFAIL_badbalance.SetMaximum(frameFAIL_badbalance.GetMaximum()*1.25)



    
    
    # Add chi2 info
    chi2_text = ROOT.TPaveText(0.15,0.72,0.15,0.88,"NBNDC")
    chi2_text.SetTextAlign(11)
    chi2_text.AddText("#chi^{2} fit = %s" %round(framePASS.chiSquare(6),2))
    chi2_text.AddText("Eff "+"= {} #pm {}".format(round(effcy.getVal(),3), round(effcy.getError(),3)))
    chi2_text.AddText("Mistag "+"= {} #pm {}".format(round(mistag.getVal(),3), round(mistag.getError(),3)) )
    chi2_text.AddText("Sigma PASS "+"= {} #pm {}".format(round(gauss_sigma_PASS.getVal(),3), round(gauss_sigma_PASS.getError(),3)) )
    chi2_text.AddText("Sigma FAIL "+"= {} #pm {}".format(round(gauss_sigma_FAIL.getVal(),3), round(gauss_sigma_FAIL.getError(),3)) )
    chi2_text.SetTextSize(0.03)
    chi2_text.SetTextColor(2)
    chi2_text.SetShadowColor(0)
    chi2_text.SetFillColor(0)
    chi2_text.SetLineColor(0)
    framePASS.addObject(chi2_text)
    frameFAIL.addObject(chi2_text)


    chi2_text_badbalance = ROOT.TPaveText(0.15,0.72,0.15,0.88,"NBNDC")
    chi2_text_badbalance.SetTextAlign(11)
    chi2_text_badbalance.AddText("#chi^{2} fit = %s" %round(framePASS.chiSquare(6),2))
    chi2_text_badbalance.AddText("Eff "+"= {} #pm {}".format(round(effcy.getVal(),3), round(effcy.getError(),3)))
    chi2_text_badbalance.AddText("Mistag "+"= {} #pm {}".format(round(mistag.getVal(),3), round(mistag.getError(),3)) )
    chi2_text_badbalance.AddText("Sigma PASS "+"= {} #pm {}".format(round(gauss_sigma_PASS_badbalance.getVal(),3), round(gauss_sigma_PASS_badbalance.getError(),3)) )
    chi2_text_badbalance.AddText("Sigma FAIL "+"= {} #pm {}".format(round(gauss_sigma_FAIL_badbalance.getVal(),3), round(gauss_sigma_FAIL_badbalance.getError(),3)) )
    chi2_text_badbalance.SetTextSize(0.03)
    chi2_text_badbalance.SetTextColor(2)
    chi2_text_badbalance.SetShadowColor(0)
    chi2_text.SetFillColor(0)
    chi2_text_badbalance.SetLineColor(0)
    framePASS_badbalance.addObject(chi2_text_badbalance)
    frameFAIL_badbalance.addObject(chi2_text_badbalance)


    cfitPASS = ROOT.TCanvas("cfitPASS","cfitPASS",600,600)
    cfitPASS.SetLogx(False)
    framePASS.Draw()

    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.3*cfitPASS.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right                                                     

    if isData:        
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", Data")
    else:
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", MC")
    latex2.Draw("same")

    framePASS.Print()
 
    legend = ROOT.TLegend(0.60,0.75,0.88,0.88)
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw("same")
 

    cfitFAIL = ROOT.TCanvas("cfitFAIL","cfitFAIL",600,600)
    cfitFAIL.SetLogx(False)
    frameFAIL.Draw()
    if isData:        
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", Data")
    else:
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", MC")

    latex2.Draw("same")
    frameFAIL.Print()
    legend.Draw("same")


    cfitPASS_badbalance = ROOT.TCanvas("cfitPASS_badbalance","cfitPASS_badbalance",600,600)
    cfitPASS_badbalance.SetLogx(False)
    framePASS_badbalance.Draw()
    if isData:        
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", Data")
    else:
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", MC")

    latex2.Draw("same")
    framePASS_badbalance.Print()
    legend.Draw("same")


    cfitFAIL_badbalance = ROOT.TCanvas("cfitFAIL_badbalance","cfitFAIL_badbalance",600,600)
    cfitFAIL_badbalance.SetLogx(False)
    frameFAIL_badbalance.Draw()
    if isData:        
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", Data")
    else:
        latex2.DrawLatex(0.89, 0.93,pt.split("To")[0]+" GeV < pt < "+pt.split("To")[1]+" GeV, "+eta.split("To")[0].replace("p",".")+" < #eta_{jet} < "+eta.split("To")[1].replace("p",".")+ ", MC")

    latex2.Draw("same")
    frameFAIL_badbalance.Print()
    legend.Draw("same")




    fit_filename = "fit_"+pt+"_"+eta
    #if not os.path.exists(fit_plot_directory): os.makedirs(fit_plot_directory)
    if isData:
        cfitPASS.SaveAs(os.path.join(output, fit_filename+"_PASS_Data.pdf"))
        cfitPASS.SaveAs(os.path.join(output, fit_filename+"_PASS_Data.png"))
        cfitFAIL.SaveAs(os.path.join(output, fit_filename+"_FAIL_Data.pdf"))
        cfitFAIL.SaveAs(os.path.join(output, fit_filename+"_FAIL_Data.png"))
        cfitPASS_badbalance.SaveAs(os.path.join(output, fit_filename+"_PASS_badbalance_Data.pdf"))
        cfitPASS_badbalance.SaveAs(os.path.join(output, fit_filename+"_PASS_badbalance_Data.png"))
        cfitFAIL_badbalance.SaveAs(os.path.join(output, fit_filename+"_FAIL_badbalance_Data.pdf"))
        cfitFAIL_badbalance.SaveAs(os.path.join(output, fit_filename+"_FAIL_badbalance_Data.png"))


    else:
        cfitPASS.SaveAs(os.path.join(output, fit_filename+"_PASS.pdf"))
        cfitPASS.SaveAs(os.path.join(output, fit_filename+"_PASS.png"))
        cfitFAIL.SaveAs(os.path.join(output, fit_filename+"_FAIL.pdf"))
        cfitFAIL.SaveAs(os.path.join(output, fit_filename+"_FAIL.png"))
        cfitPASS_badbalance.SaveAs(os.path.join(output, fit_filename+"_PASS_badbalance.pdf"))
        cfitPASS_badbalance.SaveAs(os.path.join(output, fit_filename+"_PASS_badbalance.png"))
        cfitFAIL_badbalance.SaveAs(os.path.join(output, fit_filename+"_FAIL_badbalance.pdf"))
        cfitFAIL_badbalance.SaveAs(os.path.join(output, fit_filename+"_FAIL_badbalance.png"))

    del cfitPASS, cfitFAIL, cfitPASS_badbalance, cfitFAIL_badbalance


    return effcy.getVal(), effcy.getError(), mistag.getVal(), mistag.getError()



def main():

    parser = argparse.ArgumentParser(description='Extract PU ID effcy/mistag rate and scale factors')
    #Optional arguments
    parser.add_argument("-o", "--output", dest="output", help="output folder name", type=str)
    parser.add_argument("-y", "--year",   dest="year",   help="data year", type=str)
    parser.add_argument("-c", "--channel",dest="channel",help="MuMu or EE", type=str)
    parser.add_argument("-b", "--binning",dest="binning",help="zpt or jetpt", type=str)
    parser.add_argument("-wp", "--workingpoint",dest="workingpoint",help="L or M or T", type=str)
    args = parser.parse_args()    
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetMarkerSize(0.5)
    ROOT.gStyle.SetOptLogx()
    
    inputfolder = "/afs/cern.ch/work/t/tsarkar/private/PUJetIDSF/PUJetIdStudies/CMSSW_10_2_15/src/FIT/MyFit/"

    data_filename = ""
    mc_filename = ""

    #Defines the data/MC file name to use depending on the considered channel and year
    if args.year == "2018":
        if args.channel == "MuMu":
            data_filename = inputfolder+"input_PUID_ZtoMuMu_2018Data.root"
            mc_filename    =  inputfolder+"input_PUID_ZtoMuMu_2018MC.root"
        elif args.channel == "EE":
            data_filename = inputfolder+"input_PUID_ZtoEE_2018Data.root"
            mc_filename    = inputfolder+"input_PUID_ZtoEE_2018MC.root"
        else:
            data_filename = inputfolder+"Histo_Data16.root"
            mc_filename    = inputfolder+"Histo_MC16_DY_MG.root"
    elif args.year == "2017":
        if args.channel == "MuMu":
            data_filename = inputfolder+"input_PUID_ZtoMuMu_2017Data.root"
            mc_filename    =  inputfolder+"input_PUID_ZtoMuMu_2017MC.root"
        elif args.channel == "EE":
            data_filename = inputfolder+"input_PUID_ZtoEE_2017Data.root"
            mc_filename    = inputfolder+"input_PUID_ZtoEE_2017MC.root"
        else:
            data_filename = inputfolder+"input_PUID_ZtoEEandMuMu_2017Data.root"
            mc_filename    = inputfolder+"input_PUID_ZtoEEandMuMu_2017MC.root"
    elif args.year == "2016":
        if args.channel == "MuMu":
            data_filename = inputfolder+"input_PUID_ZtoMuMu_2016Data.root"
            mc_filename    =  inputfolder+"input_PUID_ZtoMuMu_2016MC.root"
        elif args.channel == "EE":
            data_filename = inputfolder+"input_PUID_ZtoEE_2016Data.root"
            mc_filename    = inputfolder+"input_PUID_ZtoEE_2016MC.root"
        else:
            data_filename = inputfolder+"input_PUID_ZtoEEandMuMu_2016Data.root"
            mc_filename    = inputfolder+"input_PUID_ZtoEEandMuMu_2016MC.root"
            



    print "OPENING FILE", data_filename, "AND", mc_filename, args.binning
    f_data = ROOT.TFile(data_filename,"READ")
    f_mc   = ROOT.TFile(mc_filename,"READ")


#    _eta= ["min5p000tomin3p000","min3p000tomin2p750","min2p750tomin2p500","min2p500tomin2p000","min2p000tomin1p479","min1p479to0p000","0p000to1p479","1p479to2p000","2p000to2p500","2p500to2p750","2p750to3p000","3p000to5p000"]
#    _pt    = ["15to20","20to25","25to30","30to40","40to50"]
   
    _eta= ["0p0To1p479","1p479To2p4","2p0To2p5", "2p5To2p75", "2p75To3p0", "3p0To5p0"]
    _pt= ["20To30","30To40","40To50","50To60" ] 	 

    ### first define bining
    xbins = []
    ybins = []
    for ptBin in _pt:
        xbins.append(float(ptBin.split("To")[0]))                                
        xbins.append(float(ptBin.split("To")[1]))                                
    for etaBin in _eta:
        ybins.append(float((etaBin.split("To")[0].replace("p","."))))               
        ybins.append(float((etaBin.split("To")[1].replace("p","."))))
    xbins.sort()
    ybins.sort()

    ## transform to numpy array for ROOT 
    xbinsT = np.array(xbins)
    ybinsT = np.array(ybins)
    ## just in case there are duplicates
    xbinsTab = np.unique(xbinsT)
    ybinsTab = np.unique(ybinsT)

    htitle = 'PU ID'
    hname  = 'PUID'
    workingpoint = args.workingpoint
    heffdata = ROOT.TH2F(hname,htitle+" Eff data, WP " +workingpoint+ ", "+args.year,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)
    heffmc   = ROOT.TH2F(hname,htitle+" Eff MC, WP " +workingpoint+ ", "+args.year,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)
    hmistagdata = ROOT.TH2F("hmistagdata"," Mistag Data, WP " +workingpoint+ ", "+args.year,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)
    hmistagmc   = ROOT.TH2F("hmistagmc"," Mistag MC, WP " +workingpoint+ ", "+args.year,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)

    heffdata.Sumw2()
    heffmc.Sumw2()
    hmistagdata.Sumw2()
    hmistagmc.Sumw2()

    
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat("4.2f")
    
    
    #Get all histos
    #Currently the files I use contain only the distribution of all and passing events => one needs to subtract the latter to the former to get the failing events distribution
    for i in range(0,len(_pt)):
        print _pt[i]
        for j in range(0,len(_eta)):

            folder            = args.binning+"_"+_pt[i].replace("To","_") 
#            h_dphi_genunmatched_ALL  = f_mc.Get("h_dphiZjets_genunmatched_ALLeta_"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
#            h_dphi_genmatched_ALL  = f_mc.Get("h_dphiZjets_genmatched_ALLeta_"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
#            h_dphi_mc_ALL  = f_mc.Get("h_dphiZjets_ALLeta_"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
#            h_dphi_data_ALL  = f_data.Get("h_dphiZjets_ALLeta_"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
#            h_dphi_genunmatched_PASS  = f_mc.Get("h_dphiZjets_genunmatched_"+workingpoint+"eta_"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
            h_dphi_genunmatched_PASS  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_failGenMatch_goodBal_passPUIDLoose_jet0_dimuon_dphi_norm")

#            h_dphi_genmatched_PASS  = f_mc.Get("h_dphiZjets_genmatched_"+workingpoint+"eta_"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
            h_dphi_genmatched_PASS  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_passGenMatch_goodBal_passPUIDLoose_jet0_dimuon_dphi_norm")
#            h_dphi_mc_PASS  = f_mc.Get("h_dphiZjets_"+workingpoint+"_eta"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
            h_dphi_mc_PASS  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_goodBal_passPUIDLoose_jet0_dimuon_dphi_norm")

#            h_dphi_data_PASS  = f_data.Get("h_dphiZjets_"+workingpoint+"_eta"+_eta[j]+"pt_"+_pt[i]+"_goodbalance")
            h_dphi_data_PASS  = f_data.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_goodBal_passPUIDLoose_jet0_dimuon_dphi_norm")

            h_dphi_genunmatched_FAIL  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_failGenMatch_goodBal_failPUIDLoose_jet0_dimuon_dphi_norm")

            h_dphi_genmatched_FAIL  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_passGenMatch_goodBal_failPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_mc_FAIL  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_goodBal_failPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_data_FAIL  = f_data.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_goodBal_failPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_genunmatched_FAIL.Add(h_dphi_genunmatched_PASS,-1)
            h_dphi_genmatched_FAIL.Add(h_dphi_genmatched_PASS,-1)
            h_dphi_mc_FAIL.Add(h_dphi_mc_PASS,-1)
            h_dphi_data_FAIL.Add(h_dphi_data_PASS,-1)

#            h_dphi_genunmatched_ALL_badbalance  = f_mc.Get("h_dphiZjets_genunmatched_ALL_eta"+_eta[j]+"pt_"+_pt[i]+"_baddbalance")
#            h_dphi_genmatched_ALL_badbalance  = f_mc.Get("h_dphiZjets_genmatched_ALL_eta"+_eta[j]+"pt_"+_pt[i]+"_baddbalance")
#            h_dphi_mc_ALL_badbalance  = f_mc.Get("h_dphiZjets_ALL_eta"+_eta[j]+"pt_"+_pt[i]+"_baddbalance")
#            h_dphi_data_ALL_badbalance  = f_data.Get("h_dphiZjets_ALL_eta"+_eta[j]+"pt_"+_pt[i]+"_baddbalance")
            h_dphi_genunmatched_PASS_badbalance  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_failGenMatch_badBal_passPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_genmatched_PASS_badbalance  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_passGenMatch_badBal_passPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_mc_PASS_badbalance  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_badBal_passPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_data_PASS_badbalance  = f_data.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_badBal_passPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_genunmatched_FAIL_badbalance  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_failGenMatch_badBal_failPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_genmatched_FAIL_badbalance  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_passGenMatch_badBal_failPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_mc_FAIL_badbalance  = f_mc.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_badBal_failPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_data_FAIL_badbalance  = f_data.Get("h_passNJets1_jet0"+"_eta"+_eta[j]+"_pt"+_pt[i]+"_badBal_failPUIDLoose_jet0_dimuon_dphi_norm")
            h_dphi_genunmatched_FAIL_badbalance.Add(h_dphi_genunmatched_PASS_badbalance,-1)
            h_dphi_genmatched_FAIL_badbalance.Add(h_dphi_genmatched_PASS_badbalance,-1)
            h_dphi_mc_FAIL_badbalance.Add(h_dphi_mc_PASS_badbalance,-1)
            h_dphi_data_FAIL_badbalance.Add(h_dphi_data_PASS_badbalance,-1)

            
	


#            h_ptbal           = f_mc.Get("h_PtRecoJetoverPtRecoZ_testsample_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning")
#            h_ptbal_pu        = f_mc.Get("h_PtRecoJetoverPtRecoZ_PU_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning")
#            h_ptbal_matched   = f_mc.Get("h_PtRecoJetoverPtRecoZ_GenMatchedJet_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning") 
#            h_ptbal_unmatched = f_mc.Get("h_PtRecoJetoverPtRecoZ_NoGenMatchedJet_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning")
#            h_pli             = f_mc.Get("h_PtGenJetoverPtGenZ_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning")
#            h_jer             = f_mc.Get("h_PtRecoJetoverPtGenJet_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning")
#            h_ptbaldata       = f_data.Get("h_PtRecoJetoverPtRecoZ_testsample_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning")
#            h_ptbal_pudata    = f_data.Get("h_PtRecoJetoverPtRecoZ_PU_pt"+_pt[i]+"_eta"+_eta[j]+"_"+args.binning+"binning")
            
            print "Hist passing ok" 
            eff_mc,eff_mc_err,mistag_mc,mistag_mc_err=MakeDPhiFit(
                h_dphi_genunmatched_PASS,h_dphi_genmatched_PASS,h_dphi_genunmatched_FAIL,h_dphi_genmatched_FAIL,h_dphi_mc_PASS,h_dphi_mc_FAIL, 
                h_dphi_genunmatched_PASS_badbalance,h_dphi_genmatched_PASS_badbalance,h_dphi_genunmatched_FAIL_badbalance,h_dphi_genmatched_FAIL_badbalance,h_dphi_mc_PASS_badbalance,h_dphi_mc_FAIL_badbalance, 
                args.output,_pt[i], _eta[j], args.binning)
            eff_data,eff_data_err,mistag_data,mistag_data_err=MakeDPhiFit(
                h_dphi_genunmatched_PASS,h_dphi_genmatched_PASS,h_dphi_genunmatched_FAIL,h_dphi_genmatched_FAIL,h_dphi_data_PASS,h_dphi_data_FAIL, 
                h_dphi_genunmatched_PASS_badbalance,h_dphi_genmatched_PASS_badbalance,h_dphi_genunmatched_FAIL_badbalance,h_dphi_genmatched_FAIL_badbalance,h_dphi_data_PASS_badbalance,h_dphi_data_FAIL_badbalance, 
                args.output,_pt[i], _eta[j], args.binning, isData=True)

                    
            heffmc.SetBinContent(i+1,j+1, round(float(eff_mc),4))
            heffmc.SetBinError  (i+1,j+1, round(float(eff_mc_err),4))

            heffdata.SetBinContent(i+1,j+1, round(float(eff_data),4))
            heffdata.SetBinError  (i+1,j+1, round(float(eff_data_err),4))
    
            hmistagmc.SetBinContent(i+1,j+1, round(float(mistag_mc),4))
            hmistagmc.SetBinError(i+1,j+1, round(float(mistag_mc_err),4))

            hmistagdata.SetBinContent(i+1,j+1, round(float(mistag_data),4))
            hmistagdata.SetBinError(i+1,j+1, round(float(mistag_data_err),4))
            print "Hist passing ok1" 
        
    xname = "Jet p_{T} [GeV]"

    heffmc.GetYaxis().SetTitle("Jet #eta")    
    heffmc.GetXaxis().SetTitle(xname)
    heffmc.GetXaxis().SetMoreLogLabels()

    heffdata.GetYaxis().SetTitle("Jet #eta")
    heffdata.GetXaxis().SetTitle(xname)
    heffdata.GetXaxis().SetMoreLogLabels()


    hmistagmc.GetYaxis().SetTitle("Jet #eta")
    hmistagmc.GetXaxis().SetTitle(xname)
    hmistagmc.GetXaxis().SetMoreLogLabels()

    hmistagdata.GetYaxis().SetTitle("Jet #eta")
    hmistagdata.GetXaxis().SetTitle(xname)
    hmistagdata.GetXaxis().SetMoreLogLabels()

    c2 = ROOT.TCanvas("c2","c2",600,600)
    heffmc.SetMinimum(0.4)
    heffmc.SetMaximum(1.0)
    heffmc.Draw("colztexterr")
#    c2.SaveAs(os.path.join(args.output, "h2_eff_mc_"+args.year+"_"+workingpoint+".pdf"))
    c2.SaveAs("h2_eff_mc_"+args.year+"_"+workingpoint+".pdf")
    c2.SaveAs(os.path.join(args.output, "h2_eff_mc_"+args.year+"_"+workingpoint+".png"))
    heffmc.SetName("h2_eff_mc"+args.year+"_"+workingpoint)
    heffmc.SaveAs(os.path.join(args.output, "h2_eff_mc"+args.year+"_"+workingpoint+".root"))


    c3 = ROOT.TCanvas("c3","c3",600,600)
    heffdata.SetMinimum(0.4)
    heffdata.SetMaximum(1.0)
    heffdata.Draw("colztexterr")
    c3.SaveAs(os.path.join(args.output, "h2_eff_data_"+args.year+"_"+workingpoint+".pdf"))
    c3.SaveAs(os.path.join(args.output, "h2_eff_data_"+args.year+"_"+workingpoint+".png"))
    heffdata.SetName("h2_eff_data"+args.year+"_"+workingpoint)
    heffdata.SaveAs(os.path.join(args.output, "h2_eff_data"+args.year+"_"+workingpoint+".root"))

    
    c4 = ROOT.TCanvas("c4","c4",600,600)
    heffdata.Sumw2()
    heffmc.Sumw2()
    heffdata.Divide(heffmc)
    heffdata.SetNameTitle("effsf","Efficiency SF, WP " +workingpoint+ ", "+args.year)
    heffdata.SetMaximum(1.05)
    heffdata.SetMinimum(0.75)
    heffdata.Draw("colztexterr")
    c4.SaveAs(os.path.join(args.output, "h2_eff_sf_"+args.year+"_"+workingpoint+".pdf"))
    c4.SaveAs(os.path.join(args.output, "h2_eff_sf_"+args.year+"_"+workingpoint+".png"))
    heffdata.SetName( "h2_eff_sf"+args.year+"_"+workingpoint)
    heffdata.SaveAs(os.path.join(args.output, "h2_eff_sf"+args.year+"_"+workingpoint+".root"))

    c6 = ROOT.TCanvas("c6","c6",600,600)
    hmistagmc.SetMinimum(0.0)
    hmistagmc.SetMaximum(0.5)
    hmistagmc.Draw("colztexterr")
    c6.SaveAs(os.path.join(args.output, "h2_mistag_mc_"+args.year+"_"+workingpoint+".pdf"))
    c6.SaveAs(os.path.join(args.output, "h2_mistag_mc_"+args.year+"_"+workingpoint+".png"))
    hmistagmc.SetName("h2_mistag_mc"+args.year+"_"+workingpoint)
    hmistagmc.SaveAs(os.path.join(args.output, "h2_mistag_mc"+args.year+"_"+workingpoint+".root"))

    c7 = ROOT.TCanvas("c7","c7",600,600)
    hmistagdata.SetMinimum(0.0)
    hmistagdata.SetMaximum(0.5)
    hmistagdata.Draw("colztexterr")
    c7.SaveAs(os.path.join(args.output, "h2_mistag_data_"+args.year+"_"+workingpoint+".pdf"))
    c7.SaveAs(os.path.join(args.output, "h2_mistag_data_"+args.year+"_"+workingpoint+".png"))
    hmistagdata.SetName("h2_mistag_data"+args.year+"_"+workingpoint)
    hmistagdata.SaveAs(os.path.join(args.output, "h2_mistag_data"+args.year+"_"+workingpoint+".root"))

    c8 = ROOT.TCanvas("c8","c8",600,600)
    hmistagdata.Sumw2()
    hmistagmc.Sumw2()
    hmistagdata.Divide(hmistagmc)
    hmistagdata.SetNameTitle("mistagsf","Mistag SF, WP " +workingpoint+ ", "+args.year)
    hmistagdata.SetMaximum(3.)
    hmistagdata.SetMinimum(0.5)
    hmistagdata.Draw("colztexterr")
    c8.SaveAs(os.path.join(args.output, "h2_mistag_sf_"+args.year+"_"+workingpoint+".pdf"))
    c8.SaveAs(os.path.join(args.output, "h2_mistag_sf_"+args.year+"_"+workingpoint+".png"))
    hmistagdata.SetName( "h2_mistag_sf"+args.year+"_"+workingpoint)
    hmistagdata.SaveAs(os.path.join(args.output, "h2_mistag_sf"+args.year+"_"+workingpoint+".root"))
        
    del c2, c3, c4, c6, c7, c8
    
if __name__ == '__main__':
    main()
