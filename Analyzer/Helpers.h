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
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_2_22/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py#L9
//
bool PUJetID_80XCut_WPTight(float pt, float eta, float disc){
   
  if (pt > 0.0 && pt <= 10.0){
    if (fabs(eta) <= 2.50) return disc > 0.69;
    else if (fabs(eta) <= 2.75) return disc > -0.35;
    else if (fabs(eta) <= 3.00) return disc > -0.26;
    else if (fabs(eta) <= 5.00) return disc > -0.21;
  }
  else if (pt > 10.0 && pt <= 20.0){
    if (fabs(eta) <= 2.50) return disc > 0.69;
    else if (fabs(eta) <= 2.75) return disc > -0.35;
    else if (fabs(eta) <= 3.00) return disc > -0.26;
    else if (fabs(eta) <= 5.00) return disc > -0.21;
  }
  else if (pt > 20.0 && pt <= 30.0){
    if (fabs(eta) <= 2.50) return disc > 0.69;
    else if (fabs(eta) <= 2.75) return disc > -0.35;
    else if (fabs(eta) <= 3.00) return disc > -0.26;
    else if (fabs(eta) <= 5.00) return disc > -0.21;
  }
  else if (pt > 30.0 && pt <= 50.0){
    if (fabs(eta) <= 2.50) return disc > 0.86;
    else if (fabs(eta) <= 2.75) return disc > -0.10;
    else if (fabs(eta) <= 3.00) return disc > -0.05;
    else if (fabs(eta) <= 5.00) return disc > -0.01;
  }
  else return true;

  return true;
}
//
// https://github.com/cms-sw/cmssw/blob/CMSSW_10_2_22/RecoJets/JetProducers/python/PileupJetIDCutParams_cfi.py#L21
//
bool PUJetID_80XCut_WPMedium(float pt, float eta, float disc){
   
  if (pt > 0.0 && pt <= 10.0){
    if (fabs(eta) <= 2.50) return disc > 0.18;
    else if (fabs(eta) <= 2.75) return disc > -0.55;
    else if (fabs(eta) <= 3.00) return disc > -0.42;
    else if (fabs(eta) <= 5.00) return disc > -0.36;
  }
  else if (pt > 10.0 && pt <= 20.0){
    if (fabs(eta) <= 2.50) return disc > 0.18;
    else if (fabs(eta) <= 2.75) return disc > -0.55;
    else if (fabs(eta) <= 3.00) return disc > -0.42;
    else if (fabs(eta) <= 5.00) return disc > -0.36;
  }
  else if (pt > 20.0 && pt <= 30.0){
    if (fabs(eta) <= 2.50) return disc > 0.18;
    else if (fabs(eta) <= 2.75) return disc > -0.55;
    else if (fabs(eta) <= 3.00) return disc > -0.42;
    else if (fabs(eta) <= 5.00) return disc > -0.36;
  }
  else if (pt > 30.0 && pt <= 50.0){
    if (fabs(eta) <= 2.50) return disc > 0.61;
    else if (fabs(eta) <= 2.75) return disc > -0.35;
    else if (fabs(eta) <= 3.00) return disc > -0.23;
    else if (fabs(eta) <= 5.00) return disc > -0.17;
  }
  else return true;

  return true;
}
bool PUJetID_80XCut_WPLoose(float pt, float eta, float disc){
  if (pt > 0.0 && pt <= 10.0){
    if (fabs(eta) <= 2.50) return disc > -0.97;
    else if (fabs(eta) <= 2.75) return disc > -0.68;
    else if (fabs(eta) <= 3.00) return disc > -0.53;
    else if (fabs(eta) <= 5.00) return disc > -0.47;
  }
  else if (pt > 10.0 && pt <= 20.0){
    if (fabs(eta) <= 2.50) return disc > -0.97;
    else if (fabs(eta) <= 2.75) return disc > -0.68;
    else if (fabs(eta) <= 3.00) return disc > -0.53;
    else if (fabs(eta) <= 5.00) return disc > -0.47;
  }
  else if (pt > 20.0 && pt <= 30.0){
    if (fabs(eta) <= 2.50) return disc > -0.97;
    else if (fabs(eta) <= 2.75) return disc > -0.68;
    else if (fabs(eta) <= 3.00) return disc > -0.53;
    else if (fabs(eta) <= 5.00) return disc > -0.47;
  }
  else if (pt > 30.0 && pt <= 50.0){
    if (fabs(eta) <= 2.50) return disc > -0.89;
    else if (fabs(eta) <= 2.75) return disc > -0.52;
    else if (fabs(eta) <= 3.00) return disc > -0.38;
    else if (fabs(eta) <= 5.00) return disc > -0.30;
  }
  else return true;

  return true;
}
