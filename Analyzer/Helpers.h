float AbsDeltaPhi(float phi1, float phi2){
  float _phi1 = 0.0;
  float _phi2 = 0.0;
  if(phi1 > 0.0) _phi1 = phi1;
  if(phi1 < 0.0) {
    _phi1 = phi1 + (2*TMath::Pi());
  }
  if(phi2 > 0.0) _phi2 = phi2;
  if(phi2 < 0.0) {
    _phi2 = phi2 + (2*TMath::Pi());
  }
  return fabs(_phi1-_phi2);
}
float DeltaPhiNorm(float dphi){
  float _dphi = 0.0;
  if(dphi > 0.0) _dphi = dphi;
  if(dphi < 0.0) {
    _dphi = dphi + (2*TMath::Pi());
  }
  return _dphi/TMath::Pi();
}
//
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_6_17/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py#L44
//
bool PUJetID_106XUL17Cut_WPTight(float pt, float eta, float disc){
   
  if (pt > 0.0 && pt < 10.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50) return disc > 0.77;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75) return disc > 0.38;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00) return disc > -0.31;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00) return disc > -0.21;
  }
  else if (pt >= 10.0 && pt < 20.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.77;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > 0.38;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.31;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.21;
  }
  else if (pt >= 20.0 && pt < 30.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.90;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > 0.60;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.12;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.13;
  }
  else if (pt >= 30.0 && pt < 40.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.96;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > 0.82;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > 0.20;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > 0.09;
  }
  else if (pt >= 40.0 && pt < 50.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.98;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > 0.92;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > 0.47;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > 0.29;
  }
  else return true;

  return true;
}
//
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_6_17/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py#L44
//
bool PUJetID_106XUL17Cut_WPMedium(float pt, float eta, float disc){
   
  if (pt > 0.0 && pt < 10.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50) return disc > 0.26;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75) return disc > -0.33;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00) return disc > -0.54;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00) return disc > -0.37;
  }
  else if (pt >= 10.0 && pt < 20.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.26;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.33;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.54;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.37;
  }
  else if (pt >= 20.0 && pt < 30.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.68;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.04;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.43;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.30;
  }
  else if (pt >= 30.0 && pt < 40.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.90;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > 0.36;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.16;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.09;
  }
  else if (pt >= 40.0 && pt < 50.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.96;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > 0.61;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > 0.14;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > 0.12;
  }
  else return true;

  return true;
}
//
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_6_17/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py#L44
//
bool PUJetID_106XUL17Cut_WPLoose(float pt, float eta, float disc){
   
  if (pt > 0.0 && pt < 10.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50) return disc > -0.95;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75) return disc > -0.72;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00) return disc > -0.68;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00) return disc > -0.47;
  }
  else if (pt >= 10.0 && pt < 20.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.95;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.72;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.68;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.47;
  }
  else if (pt >= 20.0 && pt < 30.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.88;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.55;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.60;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.43;
  }
  else if (pt >= 30.0 && pt < 40.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.63;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.18;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.43;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.24;
  }
  else if (pt >= 40.0 && pt < 50.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.19;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.22;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.13;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.03;
  }
  else return true;

  return true;
}


//
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_2_22/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py
//
bool PUJetID_80XCut_WPTight(float pt, float eta, float disc){
   
  if (pt > 0.0 && pt < 10.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50) return disc > 0.69;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75) return disc > -0.35;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00) return disc > -0.26;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00) return disc > -0.21;
  }
  else if (pt >= 10.0 && pt < 20.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.69;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.35;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.26;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.21;
  }
  else if (pt >= 20.0 && pt < 30.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.69;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.35;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.26;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.21;
  }
  else if (pt >= 30.0 && pt < 50.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.86;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.10;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.05;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.01;
  }
  else return true;

  return true;
}
//
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_2_22/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py
//
bool PUJetID_80XCut_WPMedium(float pt, float eta, float disc){
   
  if (pt > 0.0 && pt < 10.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.18;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.55;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.42;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.36;
  }
  else if (pt >= 10.0 && pt < 20.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.18;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.55;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.42;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.36;
  }
  else if (pt >= 20.0 && pt < 30.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.18;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.55;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.42;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.36;
  }
  else if (pt > 30.0 && pt <= 50.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > 0.61;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.35;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.23;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.17;
  }
  else return true;

  return true;
}
//
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_2_22/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py
//
bool PUJetID_80XCut_WPLoose(float pt, float eta, float disc){
  if (pt > 0.0 && pt < 10.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.97;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.68;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.53;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.47;
  }
  else if (pt >= 10.0 && pt < 20.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.97;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.68;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.53;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.47;
  }
  else if (pt >= 20.0 && pt < 30.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.97;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.68;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.53;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.47;
  }
  else if (pt >= 30.0 && pt < 50.0){
    if      (std::abs(eta) >= 0.00 && std::abs(eta) < 2.50)  return disc > -0.89;
    else if (std::abs(eta) >= 2.50 && std::abs(eta) < 2.75)  return disc > -0.52;
    else if (std::abs(eta) >= 2.75 && std::abs(eta) < 3.00)  return disc > -0.38;
    else if (std::abs(eta) >= 3.00 && std::abs(eta) < 5.00)  return disc > -0.30;
  }
  else return true;

  return true;
}
